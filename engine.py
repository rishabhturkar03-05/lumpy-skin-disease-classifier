import streamlit as st
from ultralytics import YOLO

class DiagnosticEngine:
    def __init__(self, model_path='best.pt'):
        self.model_path = model_path
        self.model = self.load_yolo_model()

    @st.cache_resource
    def load_yolo_model(_self):
        """Loads the YOLOv8 model into memory once to prevent lag."""
        return YOLO(_self.model_path)

    def run_inference(self, image, conf_threshold, iou_threshold=0.25):
        """Processes the image and returns plotted image + lump count."""
        results = self.model.predict(image, conf=conf_threshold, iou=iou_threshold)
        res_img = results[0].plot()
        num_lumps = len(results[0].boxes)
        return res_img, num_lumps

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