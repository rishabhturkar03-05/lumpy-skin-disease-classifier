import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np

# --- OPTIMIZATION 1: GLOBAL CACHING ---
# Loading models outside the class prevents Streamlit memory leaks
@st.cache_resource
def load_verifier_model():
    """Loads the Gatekeeper model (Standard YOLOv8)"""
    return YOLO('yolov8n.pt')

@st.cache_resource
def load_specialist_model(model_path):
    """Loads your custom LSD Specialist model"""
    return YOLO(model_path)


class DiagnosticEngine:
    def __init__(self, model_path='best.pt'):
        # Initialize both models from the secure Streamlit cache
        self.verifier = load_verifier_model()
        self.specialist = load_specialist_model(model_path)

    def run_inference(self, image, conf_threshold, iou_threshold=0.25):
        """Processes the image through a two-stage diagnostic pipeline."""
        
        # --- OPTIMIZATION 2 & 3: STRICT PREPROCESSING ---
        img_array = np.array(image)
        
        # Strip Alpha Channel if the user uploads a transparent PNG
        if img_array.shape[-1] == 4:
            img_array = img_array[..., :3]
            
        # Convert RGB (Streamlit/PIL) to BGR (OpenCV/YOLO standard)
        cv2_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

        # ---------------------------------------------------------
        # STAGE 1: THE GATEKEEPER (ANIMAL VERIFICATION)
        # ---------------------------------------------------------
        # Run the lightweight model silently (verbose=False speeds up processing)
        ver_results = self.verifier.predict(cv2_img, conf=0.05, verbose=False)
        detected_classes = ver_results[0].boxes.cls.tolist()
        
        # COCO IDs: 19 = Cow, 18 = Sheep, 17 = Horse. 
        # We allow 17 and 18 because close-up cow photos are occasionally misclassified by the base model.
        valid_livestock_ids = {17.0, 18.0, 19.0}
        
        # Logic Check: If no livestock is found in the frame, halt execution
        if not any(cls_id in valid_livestock_ids for cls_id in detected_classes):
            raise ValueError("INVALID IMAGE: No cattle detected. Please upload a clear picture of a cow.")

        # ---------------------------------------------------------
        # STAGE 2: THE SPECIALIST (LSD DETECTION)
        # ---------------------------------------------------------
        # This only executes if Stage 1 approves the image
        results = self.specialist.predict(cv2_img, conf=conf_threshold, iou=iou_threshold, verbose=False)
        
        # Draw bounding boxes
        res_img_bgr = results[0].plot()
        
        # Convert back to RGB so Streamlit renders the colors correctly
        res_img_rgb = cv2.cvtColor(res_img_bgr, cv2.COLOR_BGR2RGB)
        
        # Count total detections
        num_lumps = len(results[0].boxes)
        
        return res_img_rgb, num_lumps

    def get_medical_advice(self, count, lang):
        """Returns specific medical actions based on detected severity."""
        if count <= 1:
            advice = {
                'English': "The cow is very healthy. No signs of infection detected.",
                'Hindi': "गाय बहुत स्वस्थ है। संक्रमण का कोई संकेत नहीं मिला।",
                'Marathi': "गाय खूप निरोगी आहे. संसर्गाचे कोणतेही लक्षण आढळले नाही."
            }
        elif count < 10:
            advice = {
                'English': "MODERATE: Please consult a veterinary doctor for a checkup.",
                'Hindi': "मध्यम: कृपया जांच के लिए पशु चिकित्सक से परामर्श करें।",
                'Marathi': "मध्यम: कृपया तपासणीसाठी पशुवैद्यकीय डॉक्टरांचा सल्ला घ्या."
            }
        else:
            advice = {
                'English': "CRITICAL: Very critical situation! Take immediate action and start treatment.",
                'Hindi': "गंभीर: बहुत ही नाजुक स्थिति! तत्काल कार्रवाई करें और उपचार शुरू करें।",
                'Marathi': "गंभीर: अत्यंत गंभीर परिस्थिती! त्वरित कारवाई करा आणि उपचार सुरू करा."
            }
        return advice.get(lang, advice['English'])
