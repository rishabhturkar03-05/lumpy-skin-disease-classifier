import streamlit as st
from PIL import Image
import time
import base64
from engine import DiagnosticEngine

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# 1. Page Configuration
st.set_page_config(page_title="LSD Diagnostic System", page_icon="🐄", layout="wide")

# Initialize Backend Engine
engine = DiagnosticEngine(model_path='best.pt')

# --- INITIALIZE SESSION STATE ---
if 'page' not in st.session_state: st.session_state.page = 'welcome'
if 'loading' not in st.session_state: st.session_state.loading = False
if 'threshold' not in st.session_state: st.session_state.threshold = 0.06
if 'language' not in st.session_state: st.session_state.language = 'English'

def trigger_loading():
    st.session_state.loading = True

# --- MULTILINGUAL DICTIONARY ---
translations = {
    'English':{
        'title': 'LSD Diagnostic System', 'subtitle': 'Check your cattle for Disease in Seconds',
        'description': 'A state-of-the-art diagnostic platform leveraging Convolutional Neural Networks to assess Lumpy Skin Disease severity with high precision.',
        'launch_btn': 'Launch Scanner', 'developed_by': 'Developed by Team A2',
        'sidebar_title': 'Animal Health Helper  ', 'sidebar_cap': '',
        'upload_prompt': '1. Upload Cattle Image', 'conf_thresh': 'Confidence Threshold',
        'start_scan': '▶ Check My Cattle ', 'team_title': 'Team A2',
        'sel_lang': '🌐 Select Language',
        'tab_up': '📁 Upload', 'tab_cam': '📷 Camera', 'cam_prompt': 'Take a live photo',
        'adv_set': '', 'main_title': 'Cattle Health Check',
        'src_data': 'Original Source Data', 'wait_in': 'Awaiting visual input from sidebar...',
        'dis_ana': 'Disease Analysis', 'sys_idle': 'System idle. Initialize diagnostic sequence.',
        'hlth_res': 'Health Result', 'det_les': 'Detected Lesions', 'stat_lbl': 'Status: ',
        'stat_h': 'HEALTHY', 'stat_m': 'MODERATE RISK', 'stat_c': 'CRITICAL RISK',
        'wait_sess': 'Awaiting session data...', 'what_do': 'What To Do', 'wait_scan': 'Awaiting scan results...',
        'feat_fast': 'Fast detection', 'feat_ai': 'AI-powered',
        'metric_res_title': 'Results in', 'metric_res_val': '3 seconds',
        'back_btn': '⬅️ Back to Home'
    },
    'Hindi': {
        'title': 'लम्पी स्किन रोग जांच', 'subtitle': 'नैदानिक पशु चिकित्सा विश्लेषिकी प्रणाली',
        'description': 'लंपी स्किन डिजीज (LSD) की गंभीरता का उच्च सटीकता के साथ आकलन करने के लिए एक अत्याधुनिक डायग्नोस्टिक प्लेटफॉर्म।',
        'launch_btn': 'स्कैनर लॉन्च करें', 'developed_by': 'टीम A2 द्वारा विकसित',
        'sidebar_title': 'Cattle Health Check', 'sidebar_cap': 'पशु चिकित्सा निदान ',
        'upload_prompt': '1. मवेशी की छवि अपलोड करें', 'conf_thresh': 'विश्वास सीमा (Threshold)',
        'start_scan': '▶ माझ्या जनावराची तपासणी करा', 'team_title': 'टीम A2',
        'sel_lang': '🌐 भाषा चुनें',
        'tab_up': '📁 अपलोड', 'tab_cam': '📷 कैमरा', 'cam_prompt': 'लाइव फोटो लें',
        'adv_set': '', 'main_title': 'मवेशी स्वास्थ्य जांच',
        'src_data': 'मूल स्रोत डेटा', 'wait_in': 'साइडबार से विज़ुअल इनपुट की प्रतीक्षा है...',
        'dis_ana': 'रोग विश्लेषण', 'sys_idle': 'सिस्टम निष्क्रिय है। डायग्नोस्टिक अनुक्रम प्रारंभ करें।',
        'hlth_res': 'स्वास्थ्य परिणाम', 'det_les': 'पाए गए घाव', 'stat_lbl': 'स्थिति: ',
        'stat_h': 'स्वस्थ', 'stat_m': 'मध्यम जोखिम', 'stat_c': 'गंभीर जोखिम',
        'wait_sess': 'सत्र डेटा की प्रतीक्षा है...', 'what_do': 'क्या करें', 'wait_scan': 'स्कैन परिणामों की प्रतीक्षा है...',
        'feat_fast': 'त्वरित पहचान', 'feat_ai': 'एआई-पावर्ड',
        'metric_res_title': 'परिणाम', 'metric_res_val': '3 सेकंड में',
        'back_btn': '⬅️ मुख्य पृष्ठ पर जाएं'
    },
    'Marathi': {
        'title': 'लम्पी स्किन रोग तपासणी', 'subtitle': 'क्लिनिकल पशुवैद्यकीय विश्लेषण प्रणाली',
        'description': 'लंपी स्किन डिसीज (LSD) च्या तीव्रतेचे उच्च अचूकतेने मूल्यांकन करण्यासाठी एक अत्याधुनिक डायग्नोस्टिक प्लॅटफॉर्म.',
        'launch_btn': 'स्कॅनर लाँच करा', 'developed_by': 'टीम A2 द्वारे विकसित',
        'sidebar_title': '', 'sidebar_cap': 'पशुवैद्यकीय निदान ',
        'upload_prompt': '1. गुरांची प्रतिमा अपलोड करा', 'conf_thresh': 'विश्वास मर्यादा (Threshold)',
        'start_scan': '▶ डायग्नोस्टिक स्कॅन सुरू करा', 'team_title': 'टीम A2',
        'sel_lang': '🌐 भाषा निवडा',
        'tab_up': '📁 अपलोड करा', 'tab_cam': '📷 कॅमेरा', 'cam_prompt': 'थेट फोटो काढा',
        'adv_set': '', 'main_title': 'गुरांच्या आरोग्याची तपासणी',
        'src_data': 'मूळ स्रोत डेटा', 'wait_in': 'साइडबारवरून दृश्य इनपुटची प्रतीक्षा करत आहे...',
        'dis_ana': 'रोग विश्लेषण', 'sys_idle': 'प्रणाली निष्क्रिय आहे. निदान क्रम सुरू करा.',
        'hlth_res': 'आरोग्य निकाल', 'det_les': 'आढळलेले फोड', 'stat_lbl': 'स्थिती: ',
        'stat_h': 'निरोगी', 'stat_m': 'मध्यम धोका', 'stat_c': 'गंभीर धोका',
        'wait_sess': 'सत्र डेटाची प्रतीक्षा करत आहे...', 'what_do': 'काय करावे', 'wait_scan': 'स्कॅन निकालांची प्रतीक्षा करत आहे...',
        'feat_fast': 'जलद तपासणी', 'feat_ai': 'एआई-पावर्ड',
        'metric_res_title': 'निकाल', 'metric_res_val': '3 सेकंदात',
        'back_btn': '⬅️ मुख्य पृष्ठावर जा'
    }
}

lang = st.session_state.language
t = translations[lang]

# --- GLOBAL CSS: PASTORAL AIRY THEME ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    
    /* Sleek Tech Intro Animations */
    @keyframes scanRevealOverlay {
        0% { background: #0A192F; opacity: 1; }
        70% { background: #0A192F; opacity: 1; }
        100% { background: transparent; opacity: 0; visibility: hidden; }
    }
    
    @keyframes scanLineSweep {
        0% { top: -10%; opacity: 0; }
        10% { opacity: 1; }
        80% { top: 110%; opacity: 1; }
        100% { top: 110%; opacity: 0; }
    }

    @keyframes textGlowReveal {
        0% { opacity: 0; filter: blur(10px); transform: translate(-50%, -40%); }
        30% { opacity: 1; filter: blur(0px); transform: translate(-50%, -50%); text-shadow: 0 0 30px rgba(0, 224, 150, 0.8); }
        80% { opacity: 1; transform: translate(-50%, -50%); text-shadow: 0 0 10px rgba(0, 224, 150, 0.4); }
        100% { opacity: 0; filter: blur(5px); transform: translate(-50%, -60%); visibility: hidden; }
    }

    .intro-overlay {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: 99999; pointer-events: none;
        animation: scanRevealOverlay 4s cubic-bezier(0.4, 0, 0.2, 1) forwards; 
        overflow: hidden;
    }

    .scanner-line {
        position: absolute; width: 100%; height: 3px;
        background: #00E096; left: 0;
        box-shadow: 0 0 20px #00E096, 0 0 40px #00E096, 0 0 80px #7B61FF;
        animation: scanLineSweep 3.5s linear forwards;
    }

    .intro-text {
        position: absolute; top: 50%; left: 50%;
        transform: translate(-50%, -50%);
        font-size: 48px; font-weight: 800; color: #FFFFFF; text-align: center; width: 100%;
        letter-spacing: 4px; z-index: 100000;
        animation: textGlowReveal 4s ease-in-out forwards;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Faster Background Gradient Animation */
    @keyframes panSky { 
        0% { background-position: 0% 50%; } 
        50% { background-position: 100% 50%; } 
        100% { background-position: 0% 50%; } 
    }
    .stApp { 
        background: linear-gradient(-45deg, #E2FDF2, #A7F3D0, #A7C7E7, #D6E4FF, #EBF1FF); 
        background-size: 400% 400%; 
        animation: panSky 12s ease infinite; 
        font-family: 'Plus Jakarta Sans', sans-serif; 
        color: #1A202C; 
    }

    /* New Image Pulsing Glow Animation */
    @keyframes imageGlow {
        0% { box-shadow: 0 0 20px rgba(167, 199, 231, 0.2); transform: translateY(0px); }
        50% { box-shadow: 0 0 50px rgba(123, 97, 255, 0.4); transform: translateY(-8px); }
        100% { box-shadow: 0 0 20px rgba(167, 199, 231, 0.2); transform: translateY(0px); }
    }
    .animated-cow-img {
        width: 100%; border-radius: 15px; margin-bottom: 20px;
        animation: imageGlow 4s ease-in-out infinite;
    }
    .block-container { padding-top: 1rem; padding-bottom: 2rem; position: relative; z-index: 10; }
    .stAppDeployButton { display: none; }
    
    /* New Glassmorphic Card Style (Enhanced for text readability) */
    .glass-card {
        background: rgba(255, 255, 255, 0.55);
        border-radius: 20px; padding: 30px;
        backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(112, 144, 176, 0.15);
        margin-bottom: 20px; border: 1px solid rgba(255, 255, 255, 0.4);
        height: 100%; position: relative; z-index: 10;
        display: flex; flex-direction: column; justify-content: center;
    }
    
    .left-card { text-align: left; }
    .right-card { text-align: center; justify-content: space-around; }
    .description-text { font-size: 16px; line-height: 1.6; color: #2D3748; font-weight: 500; text-shadow: 0 1px 2px rgba(255,255,255,0.8); }

    /* --- COMMON ELEMENTS RETAINED FROM YOUR CODE --- */
    .purple-card { background: linear-gradient(135deg, #7B61FF 0%, #5A3FFF 100%); border-radius: 20px; padding: 20px; color: white; box-shadow: 0 6px 20px rgba(123, 97, 255, 0.2); margin-bottom: 15px; text-align: center; }
    .accent-green { background: rgba(0, 224, 150, 0.9); color: white; border-radius: 12px; padding: 12px; text-align: center; font-weight: bold; }
    .accent-orange { background: rgba(255, 138, 76, 0.9); color: white; border-radius: 12px; padding: 12px; text-align: center; font-weight: bold; }
    .accent-red { background: rgba(255, 90, 90, 0.9); color: white; border-radius: 12px; padding: 12px; text-align: center; font-weight: bold; }
    .app-title { font-size: 32px; font-weight: 800; color: #1B5E20; margin-bottom: 25px; letter-spacing: -0.5px; text-shadow: 0 2px 5px rgba(255,255,255,0.5); }
    .section-header { font-size: 14px; font-weight: 800; color: #7B61FF; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px; }
    div[data-testid="stFileUploader"] { background-color: #F7FAFC; border-radius: 16px; padding: 10px; border: 2px dashed #E2E8F0; }
    
    /* Launch Button Gradient Update */
    .stButton>button { 
        border-radius: 12px; font-weight: bold; transition: all 0.3s ease; border: none; 
        background: linear-gradient(90deg, #A7C7E7 0%, #B6A7F3 50%, #B2A7F3 100%); 
        color: white; padding: 10px 20px; text-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    .stButton>button:hover { 
        transform: translateY(-2px); box-shadow: 0 5px 15px rgba(182, 167, 243, 0.4); 
        background: linear-gradient(90deg, #B6A7F3 0%, #B2A7F3 50%, #A7C7E7 100%); 
        color: white; 
    }

    [data-testid="stImage"] img { border-radius: 16px; box-shadow: 0 10px 40px rgba(112, 144, 176, 0.1); border: 4px solid white;}
    section[data-testid="stSidebar"] { border-right: 1px solid #E2E8F0; }
    section[data-testid="stSidebar"] div[data-testid="stBlock"] p, section[data-testid="stSidebar"] div[data-testid="stBlock"] h1, section[data-testid="stSidebar"] div[data-testid="stBlock"] h2, section[data-testid="stSidebar"] div[data-testid="stBlock"] h3, section[data-testid="stSidebar"] div[data-testid="stBlock"] h4 { color: #2D3748 !important; }
    div[data-testid="stSidebar"] div[data-testid="stCheckbox"] label p { color: #2D3748 !important; }
    
    /* Animated Title Header */
    @keyframes titleShine {
        0% { filter: hue-rotate(0deg); }
        100% { filter: hue-rotate(30deg); }
    }
    .main-page-header { text-align: center; margin-bottom: 40px; }
    .welcome-title { 
        font-size: 64px; font-weight: 800; 
        background-image: linear-gradient(90deg, #1B5E20 0%, #32D08E 50%, #2B6CB0 100%); 
        -webkit-background-clip: text; background-clip: text; color: transparent; 
        letter-spacing: -1.5px; animation: titleShine 8s ease-in-out infinite alternate;
        text-shadow: 2px 4px 15px rgba(27, 94, 32, 0.15);
    }
    .welcome-subtitle { font-size: 22px; color: #2B6CB0; font-weight: 700; text-shadow: 0 2px 4px rgba(255,255,255,0.8); }
    
    /* Styling for selectbox in welcome page column */
    div[data-testid="stSelectbox"] label p { color: #2D3748 !important; font-weight: 800; font-size: 16px;}
    
    /* Styling for new sub-elements in Card 2 */
    .card-sub-elements { width: 100%; display: flex; flex-direction: column; align-items: center; justify-content: space-between; }
    .feature-row { width: 100%; display: flex; justify-content: space-around; margin-bottom: 20px; }
    .feature-block { 
        background: rgba(255, 255, 255, 0.7); border-radius: 10px; padding: 10px 15px; 
        color: #1A202C; font-weight: 700; font-size: 13px; display: flex; align-items: center; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .feature-block .icon { margin-right: 8px; font-size: 14px; }
    .metrics-row { width: 100%; display: flex; justify-content: space-around; }
    .metric-block { 
        color: #2D3748; font-weight: 700; font-size: 14px; display: flex; align-items: center; 
    }
    .metric-block .val { color: #2B6CB0; font-weight: 800; font-size: 16px; margin-left: 5px; }

    /* Redesigned Glass Loading Overlay */
    .loading-backdrop { 
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; 
        background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(15px); -webkit-backdrop-filter: blur(15px);
        z-index: 999999; display: flex; flex-direction: column; justify-content: center; align-items: center; 
    }
    .scanner-ring { 
        width: 120px; height: 120px; border-radius: 50%; 
        border: 4px solid rgba(123, 97, 255, 0.1); 
        border-top: 4px solid #7B61FF; border-bottom: 4px solid #00E096;
        animation: spin 1.2s cubic-bezier(0.5, 0.1, 0.4, 0.9) infinite; margin-bottom: 30px; 
        box-shadow: 0 0 30px rgba(123, 97, 255, 0.2); 
    }
    .pulse-text { 
        background: linear-gradient(90deg, #7B61FF, #00E096); -webkit-background-clip: text; background-clip: text; color: transparent;
        font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; font-size: 28px; letter-spacing: 2px; 
        animation: pulseOpacity 1s infinite alternate; 
    }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    @keyframes pulseOpacity { 0% { opacity: 0.5; filter: blur(1px); } 100% { opacity: 1; filter: blur(0px); } }
</style>
""", unsafe_allow_html=True)

# Sleek Tech Intro HTML
st.markdown("""
<div class="intro-overlay">
    <div class="scanner-line"></div>
    <div class="intro-text">Welcome to our LSD detection system</div>
</div>
""", unsafe_allow_html=True)

# --- PAGE LOGIC ---
if st.session_state.loading:
    st.markdown("""
    <div class="loading-backdrop">
        <div class="scanner-ring"></div>
        <div class="pulse-text">INITIALIZING NEURAL LAYERS...</div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(3.5) 
    st.session_state.page = 'dashboard'
    st.session_state.loading = False
    st.rerun()

elif st.session_state.page == 'welcome':
    # Updated translations and keys must be active here
    lang = st.session_state.language
    t = translations[lang]

    # Structure the main page title and subtitle outside the columns
    st.markdown(f"""
    <div class="main-page-header">
        <div class="welcome-title">{t['title']}</div>
        <div class="welcome-subtitle">{t['subtitle']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Container to hold the two main cards using columns
    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown(f"""
        <div class="glass-card left-card">
            <div class="description-text">{t['description']}</div>
        </div>
        """, unsafe_allow_html=True)
        # Position language selector and launch button within the columns, styled with custom divs.
        st.markdown(f"<div style='padding-top:20px; color:#2D3748; font-weight:800;'>{t['sel_lang']}</div>", unsafe_allow_html=True)
        new_lang = st.selectbox(t['sel_lang'], ['English', 'Hindi', 'Marathi'], index=['English', 'Hindi', 'Marathi'].index(st.session_state.language), label_visibility="collapsed")
        if new_lang != st.session_state.language:
            st.session_state.language = new_lang
            st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        st.button(t['launch_btn'], type="primary", use_container_width=True, on_click=trigger_loading, key="launch_btn_v2")

    with col2:
        try:
            # Calls the exact file in your VS Code folder
            img_base64 = get_base64_image("animated_cow.png")
            img_html = f'<img src="data:image/png;base64,{img_base64}" class="animated-cow-img">'
        except FileNotFoundError:
            img_html = '<div style="color: red; margin-bottom: 20px;">Error: animated_cow.png not found. Ensure it is in the same folder as app.py.</div>'

        st.markdown(f"""
        <div class="glass-card right-card">
            {img_html}
            <div class='card-sub-elements'>
                <div class='feature-row'>
                    <div class='feature-block'><span class='icon'>⚡</span>{t['feat_fast']}</div>
                    <div class='feature-block'><span class='icon'>🧠</span>{t['feat_ai']}</div>
                </div>
                <div class='metrics-row'>
                    <div class='metric-block'>{t['metric_res_title']}<span style='padding:0 5px;'></span><span class='val'>{t['metric_res_val']}</span></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Optional footer retention or modification
    st.markdown(f"<div style='text-align: center; color: #1B5E20; margin-top: 40px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px;'>{t['developed_by']}</div>", unsafe_allow_html=True)

elif st.session_state.page == 'dashboard':
    with st.sidebar:
        # Added Back Button Here
        if st.button(t['back_btn'], use_container_width=True):
            st.session_state.page = 'welcome'
            st.rerun()
            
        st.markdown(f"<h2 style='color: #1B5E20; font-weight: 800; margin-bottom: 0; margin-top: 15px;'>{t['sidebar_title']}</h2>", unsafe_allow_html=True)
        st.caption(t['sidebar_cap'])
        st.markdown("<br>", unsafe_allow_html=True)
        
        # --- CAMERA & UPLOAD TABS NOW IN SIDEBAR ---
        tab1, tab2 = st.tabs([t['tab_up'], t['tab_cam']])
        
        with tab1:
            uploaded_file = st.file_uploader(t['upload_prompt'], type=["jpg", "jpeg", "png"])
        with tab2:
            camera_file = st.camera_input(t['cam_prompt'])

        # Capture whichever input the user provides
        final_input = camera_file or uploaded_file
        
        st.markdown("<hr style='border-top: 1px solid #E2E8F0; margin: 15px 0;'>", unsafe_allow_html=True)
        show_admin = st.checkbox(t['adv_set'])
        if show_admin:
            st.session_state.threshold = st.slider(t['conf_thresh'], 0.05, 1.0, st.session_state.threshold, 0.01)
            st.caption(f"Current internal threshold memory: {st.session_state.threshold}")
            
        st.markdown("<br>", unsafe_allow_html=True)
        run_diag = st.button(t['start_scan'], type="primary", use_container_width=True)
        
        st.markdown("<hr style='border-top: 1px solid #E2E8F0; margin: 25px 0 15px 0;'>", unsafe_allow_html=True)
        st.markdown(f"<h4>{t['team_title']}</h4>", unsafe_allow_html=True)
        for name in ["Muskan", "Gauri", "Akanksha", "Rishabh", "Shravan"]:
            st.markdown(f"<p style='color: #718096; margin-bottom: 2px; font-weight: 600;'>• {name}</p>", unsafe_allow_html=True)

    # --- MAIN SCREEN (CLEAN) ---
    st.markdown(f"<div class='app-title'>{t['main_title']}</div>", unsafe_allow_html=True)
    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        st.markdown(f"<div class='section-header'>{t['src_data']}</div>", unsafe_allow_html=True)
        
        if final_input:
            input_img = Image.open(final_input)
            st.image(input_img, use_container_width=True)
        else:
            st.markdown(f"<div class='neo-card' style='text-align: center; padding: 10px; color: #4A5568;'>{t['wait_in']}</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown(f"<div class='section-header'>{t['dis_ana']}</div>", unsafe_allow_html=True)
        
        if final_input and run_diag:
            try:
                res_img, num_lumps = engine.run_inference(input_img, st.session_state.threshold) 
                st.image(res_img, channels="BGR", use_container_width=True)
            except Exception as e:
                st.error(f"Error executing AI inference: {e}")
                num_lumps = None
        else:
            st.markdown(f"<div class='neo-card' style='text-align: center; padding: 10px; color: #4A5568;'>{t['sys_idle']}</div>", unsafe_allow_html=True)
            num_lumps = None 
            
    st.markdown("<br>", unsafe_allow_html=True)
    col_report, col_act = st.columns([1, 2], gap="large")
    
    with col_report:
        st.markdown(f"<div class='section-header'>{t['hlth_res']}</div>", unsafe_allow_html=True)
        if num_lumps is not None:
            color = "#7EE787" if num_lumps <= 1 else ("#FFD166" if num_lumps < 10 else "#FF5A5A")
            status = t['stat_h'] if num_lumps <= 1 else (t['stat_m'] if num_lumps < 10 else t['stat_c'])
            report_html = f"""
            <div class='neo-card'>
                <div class='purple-card'>
                    <h1 style='margin:0; font-size:42px;'>{num_lumps}</h1>
                    <p style='margin:0; font-size:12px; opacity:0.9;'>{t['det_les']}</p>
                </div>
                <div class='accent-green' style='background:{color}; color:black;'>{t['stat_lbl']}{status}</div>
            </div>
            """
            st.markdown(report_html, unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='neo-card'>{t['wait_sess']}</div>", unsafe_allow_html=True)

    with col_act:
        st.markdown(f"<div class='section-header'>{t['what_do']}</div>", unsafe_allow_html=True)
        if num_lumps is not None:
            advice = engine.get_medical_advice(num_lumps, st.session_state.language)
            text_color = "#1B5E20" if num_lumps <= 1 else ("#B7791F" if num_lumps < 10 else "#C53030")
            st.markdown(f"<div class='neo-card' style='border-left: 10px solid {text_color}; min-height:200px; display:flex; align-items:center;'><h2 style='color:{text_color}; padding:20px;'>{advice}</h2></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='neo-card'>{t['wait_scan']}</div>", unsafe_allow_html=True)
