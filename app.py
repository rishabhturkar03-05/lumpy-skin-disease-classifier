import streamlit as st
from PIL import Image
import time
from engine import DiagnosticEngine

# 1. Page Configuration
st.set_page_config(page_title="LSD Diagnostic System", page_icon="🐄", layout="wide")

# Initialize Backend Engine
engine = DiagnosticEngine(model_path='best.pt')

# --- INITIALIZE SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'loading' not in st.session_state: st.session_state.loading = False
if 'threshold' not in st.session_state: st.session_state.threshold = 0.16 
if 'language' not in st.session_state: st.session_state.language = 'English'

def trigger_loading():
    st.session_state.loading = True

# --- MULTILINGUAL DICTIONARY ---
translations = {
    'English':{
        'title': 'LSD Diagnostic System', 'subtitle': 'Check your cattle for Disease in Seconds',
        'description': 'A state-of-the-art diagnostic platform leveraging Convolutional Neural Networks to assess Lumpy Skin Disease severity with high precision.',
        'launch_btn': 'Launch Scanner', 'developed_by': 'Developed by Team A2',
        'sidebar_title': 'LSD-AI Hub', 'sidebar_cap': 'Veterinary Diagnostics v2.0',
        'upload_prompt': '1. Upload Cattle Image', 'conf_thresh': 'Confidence Threshold',
        'start_scan': '▶ START DIAGNOSTIC SCAN', 'team_title': 'Team A2'
    },
    'Hindi': {
        'title': 'लम्पी स्किन रोग जांच', 'subtitle': 'नैदानिक पशु चिकित्सा विश्लेषिकी प्रणाली',
        'description': 'लंपी स्किन डिजीज (LSD) की गंभीरता का उच्च सटीकता के साथ आकलन करने के लिए एक अत्याधुनिक डायग्नोस्टिक प्लेटफॉर्म।',
        'launch_btn': 'स्कैनर लॉन्च करें', 'developed_by': 'टीम A2 द्वारा विकसित',
        'sidebar_title': 'LSD-AI हब', 'sidebar_cap': 'पशु चिकित्सा निदान v2.0',
        'upload_prompt': '1. मवेशी की छवि अपलोड करें', 'conf_thresh': 'विश्वास सीमा (Threshold)',
        'start_scan': '▶ डायग्नोस्टिक स्कैन शुरू करें', 'team_title': 'टीम A2'
    },
    'Marathi': {
        'title': 'लम्पी स्किन रोग तपासणी', 'subtitle': 'क्लिनिकल पशुवैद्यकीय विश्लेषण प्रणाली',
        'description': 'लंपी स्किन डिसीज (LSD) च्या तीव्रतेचे उच्च अचूकतेने मूल्यांकन करण्यासाठी एक अत्याधुनिक डायग्नोस्टिक प्लॅटफॉर्म.',
        'launch_btn': 'स्कॅनर लाँच करा', 'developed_by': 'टीम A2 द्वारे विकसित',
        'sidebar_title': 'LSD-AI हब', 'sidebar_cap': 'पशुवैद्यकीय निदान v2.0',
        'upload_prompt': '1. गुरांची प्रतिमा अपलोड करा', 'conf_thresh': 'विश्वास मर्यादा (Threshold)',
        'start_scan': '▶ डायग्नोस्टिक स्कॅन सुरू करा', 'team_title': 'टीम A2'
    }
}

lang = st.session_state.language
t = translations[lang]

# --- GLOBAL CSS: PASTORAL AIRY THEME ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    @keyframes fadeSunrise { 0% { opacity: 1; } 80% { opacity: 1; } 100% { opacity: 0; } }
    .sunrise-overlay { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: linear-gradient(to bottom, #FF8A4C 0%, #FFD166 60%, #EBF1FF 100%); z-index: 99999; animation: fadeSunrise 3s ease-out forwards; pointer-events: none; }
    @keyframes panSky { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    .stApp { background-color: #EBF1FF; background-image: linear-gradient(135deg, #FFFFFF, #F0F8FF); background-size: 150% 150%; animation: panSky 90s linear infinite; font-family: 'Plus Jakarta Sans', sans-serif; color: #1A202C; }
    .block-container { padding-top: 1rem; padding-bottom: 2rem; position: relative; z-index: 10; }
    header { visibility: hidden; }
    .neo-card { background: rgba(255, 255, 255, 0.7); border-radius: 20px; padding: 24px; box-shadow: 0 4px 15px rgba(112, 144, 176, 0.05); margin-bottom: 20px; border: 1px solid rgba(255, 255, 255, 0.8); height: 100%; position: relative; z-index: 10; }
    .purple-card { background: linear-gradient(135deg, #7B61FF 0%, #5A3FFF 100%); border-radius: 20px; padding: 20px; color: white; box-shadow: 0 6px 20px rgba(123, 97, 255, 0.2); margin-bottom: 15px; text-align: center; }
    .accent-green { background: rgba(0, 224, 150, 0.9); color: white; border-radius: 12px; padding: 12px; text-align: center; font-weight: bold; }
    .accent-orange { background: rgba(255, 138, 76, 0.9); color: white; border-radius: 12px; padding: 12px; text-align: center; font-weight: bold; }
    .accent-red { background: rgba(255, 90, 90, 0.9); color: white; border-radius: 12px; padding: 12px; text-align: center; font-weight: bold; }
    .app-title { font-size: 32px; font-weight: 800; color: #1B5E20; margin-bottom: 25px; letter-spacing: -0.5px; }
    .section-header { font-size: 14px; font-weight: 800; color: #7B61FF; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px; }
    div[data-testid="stFileUploader"] { background-color: #F7FAFC; border-radius: 16px; padding: 10px; border: 2px dashed #E2E8F0; }
    .stButton>button { border-radius: 12px; font-weight: bold; transition: all 0.3s ease; border: none; background-color: #7B61FF; color: white; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(123, 97, 255, 0.3); background-color: #5A3FFF; color: white; }
    [data-testid="stImage"] img { border-radius: 16px; box-shadow: 0 10px 40px rgba(112, 144, 176, 0.1); border: 4px solid white;}
    section[data-testid="stSidebar"] { border-right: 1px solid #E2E8F0; }
    section[data-testid="stSidebar"] div[data-testid="stBlock"] p, section[data-testid="stSidebar"] div[data-testid="stBlock"] h1, section[data-testid="stSidebar"] div[data-testid="stBlock"] h2, section[data-testid="stSidebar"] div[data-testid="stBlock"] h3, section[data-testid="stSidebar"] div[data-testid="stBlock"] h4 { color: #2D3748 !important; }
    div[data-testid="stSidebar"] div[data-testid="stCheckbox"] label p { color: #2D3748 !important; }
    .welcome-container { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 80vh; text-align: center; }
    .welcome-title { font-size: 72px; font-weight: 800; color: #1B5E20; letter-spacing: -1.5px; }
    .welcome-subtitle { font-size: 24px; color: #58A6FF; font-weight: 600; margin-bottom: 40px; }
    .grass-footer { position: fixed; bottom: 0; left: 0; width: 100vw; height: 12vh; background-image: url("https://images.unsplash.com/photo-1620067644265-d0590a93144d?q=80&w=2000"); background-size: 120px 100%; background-repeat: repeat-x; background-position: bottom; z-index: 5; }
    div[data-testid="stSelectbox"] label p { color: #2D3748 !important; font-weight: 800;}
    .loading-backdrop { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: #FFFFFF; z-index: 999999; display: flex; flex-direction: column; justify-content: center; align-items: center; }
    .scanner-ring { width: 100px; height: 100px; border-radius: 50%; border: 8px solid #E2E8F0; border-top: 8px solid #7B61FF; animation: spin 1s linear infinite; margin-bottom: 30px; box-shadow: 0 0 20px rgba(123, 97, 255, 0.1); }
    .pulse-text { color: #2D3748; font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 24px; letter-spacing: 1px; animation: pulseOpacity 1.2s infinite alternate; }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    @keyframes pulseOpacity { 0% { opacity: 0.4; } 100% { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="sunrise-overlay"></div>', unsafe_allow_html=True)

# --- PAGE LOGIC ---
if st.session_state.loading:
    st.markdown("""
    <div class="loading-backdrop">
        <div class="scanner-ring"></div>
        <div class="pulse-text">INITIALIZING NEURAL LAYERS...</div>
        <p style="color: #7B61FF; margin-top: 15px; font-weight: 600; font-size: 16px;">Connecting to Team A2 Architecture</p>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(3.5) 
    st.session_state.page = 'dashboard'
    st.session_state.loading = False
    st.rerun()

elif st.session_state.page == 'welcome':
    st.markdown('<div class="grass-footer"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="welcome-container">
        <div class="welcome-title">{t['title']}</div>
        <div class="welcome-subtitle">{t['subtitle']}</div>
        <div class="neo-card" style="max-width: 650px; color: #1A202C; font-size: 16px; margin-bottom: 30px; line-height: 1.6; height: auto;">
            {t['description']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        new_lang = st.selectbox("🌐 Select Language", ['English', 'Hindi', 'Marathi'], index=['English', 'Hindi', 'Marathi'].index(st.session_state.language))
        if new_lang != st.session_state.language:
            st.session_state.language = new_lang
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.button(t['launch_btn'], type="primary", use_container_width=True, on_click=trigger_loading)
        
    st.markdown(f"<div style='text-align: center; color: #1B5E20; margin-top: 40px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;'>{t['developed_by']}</div>", unsafe_allow_html=True)

elif st.session_state.page == 'dashboard':
    with st.sidebar:
        st.markdown(f"<h2 style='color: #1B5E20; font-weight: 800; margin-bottom: 0;'>{t['sidebar_title']}</h2>", unsafe_allow_html=True)
        st.caption(t['sidebar_cap'])
        st.markdown("<br>", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(t['upload_prompt'], type=["jpg", "jpeg", "png"])
        
        st.markdown("<hr style='border-top: 1px solid #E2E8F0; margin: 15px 0;'>", unsafe_allow_html=True)
        show_admin = st.checkbox("")
        if show_admin:
            st.session_state.threshold = st.slider(t['conf_thresh'], 0.05, 1.0, st.session_state.threshold, 0.01)
            st.caption(f"Current internal threshold memory: {st.session_state.threshold}")
            
        st.markdown("<br>", unsafe_allow_html=True)
        run_diag = st.button(t['start_scan'], type="primary", use_container_width=True)
        
        st.markdown("<hr style='border-top: 1px solid #E2E8F0; margin: 25px 0 15px 0;'>", unsafe_allow_html=True)
        st.markdown(f"<h4>{t['team_title']}</h4>", unsafe_allow_html=True)
        for name in ["Muskan", "Gauri", "Akanksha", "Rishabh", "Shravan"]:
            st.markdown(f"<p style='color: #718096; margin-bottom: 2px; font-weight: 600;'>• {name}</p>", unsafe_allow_html=True)

    st.markdown("<div class='app-title'>Diagnostic Hub</div>", unsafe_allow_html=True)
    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        st.markdown("<div class='section-header'>Original Source Data</div>", unsafe_allow_html=True)
        if uploaded_file:
            input_img = Image.open(uploaded_file)
            st.image(input_img, use_container_width=True)
        else:
            st.markdown("<div class='neo-card' style='text-align: center; padding: 10px; color: #4A5568;'>Awaiting visual input from sidebar...</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("<div class='section-header'>AI Pathological Mapping</div>", unsafe_allow_html=True)
        if uploaded_file and run_diag:
            try:
                res_img, num_lumps = engine.run_inference(input_img, st.session_state.threshold) 
                st.image(res_img, channels="BGR", use_container_width=True)
            except Exception as e:
                st.error(f"Error executing AI inference: {e}")
                num_lumps = None
        else:
            st.markdown("<div class='neo-card' style='text-align: center; padding: 10px; color: #4A5568;'>System idle. Initialize diagnostic sequence.</div>", unsafe_allow_html=True)
            num_lumps = None 
            
    st.markdown("<br>", unsafe_allow_html=True)
    col_report, col_act = st.columns([1, 2], gap="large")

    with col_report:
        st.markdown("<div class='section-header'>Diagnostic Report</div>", unsafe_allow_html=True)
        if num_lumps is not None:
            color = "#7EE787" if num_lumps <= 1 else ("#FFD166" if num_lumps < 10 else "#FF5A5A")
            status = "HEALTHY" if num_lumps <= 1 else ("MODERATE RISK" if num_lumps < 10 else "CRITICAL RISK")
            report_html = f"""
            <div class='neo-card'>
                <div class='purple-card'>
                    <h1 style='margin:0; font-size:42px;'>{num_lumps}</h1>
                    <p style='margin:0; font-size:12px; opacity:0.9;'>Detected Lesions</p>
                </div>
                <div class='accent-green' style='background:{color}; color:black;'>Status: {status}</div>
            </div>
            """
            st.markdown(report_html, unsafe_allow_html=True)
        else:
            st.markdown("<div class='neo-card'>Awaiting session data...</div>", unsafe_allow_html=True)

    with col_act:
        st.markdown("<div class='section-header'>Veterinary Action Plan</div>", unsafe_allow_html=True)
        if num_lumps is not None:
            advice = engine.get_medical_advice(num_lumps, st.session_state.language)
            text_color = "#1B5E20" if num_lumps <= 1 else ("#B7791F" if num_lumps < 10 else "#C53030")
            st.markdown(f"<div class='neo-card' style='border-left: 10px solid {text_color}; min-height:200px; display:flex; align-items:center;'><h2 style='color:{text_color}; padding:20px;'>{advice}</h2></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='neo-card'>Awaiting scan results...</div>", unsafe_allow_html=True)