import streamlit as st
from model import predict
from database import init_db, insert_record
import datetime

# -------------------------------
# HARDWARE IMPORT SAFE MODE
# -------------------------------
try:
    from hardware import dispense_medicine
    HARDWARE_AVAILABLE = True
except:
    HARDWARE_AVAILABLE = False

HARDWARE_ENABLED = HARDWARE_AVAILABLE

init_db()

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Health AI", layout="wide")

# -------------------------------
# SESSION STATE
# -------------------------------
if "page" not in st.session_state:
    st.session_state.page = 0
if "lang" not in st.session_state:
    st.session_state.lang = "English"
if "data" not in st.session_state:
    st.session_state.data = {}
if "billing" not in st.session_state:
    st.session_state.billing = {}
if "dispensed" not in st.session_state:
    st.session_state.dispensed = False

# -------------------------------
# NAVIGATION
# -------------------------------
def next_page():
    st.session_state.page += 1

def restart():
    st.session_state.page = 0
    st.session_state.data = {}
    st.session_state.billing = {}
    st.session_state.dispensed = False

# -------------------------------
# TRANSLATION SYSTEM
# -------------------------------
TEXT = {
    "English": {
        "language": "Language",
        "select": "Select",
        "next": "Next ➡️",
        "details": "User Details",
        "name": "Name",
        "age": "Age",
        "dob": "Date of Birth",
        "symptoms": "Select Symptoms",
        "severity": "Severity",
        "duration": "Duration (days)",
        "result": "Diagnosis Result",
        "confidence": "Confidence",
        "meds": "Medication Plan",
        "medicine": "Medicine",
        "dose": "Dose",
        "timing": "Timing",
        "type": "Type",
        "days": "Days (1-5)",
        "total": "Total Cost",
        "proceed": "Proceed ➡️",
        "payment": "Payment",
        "amount": "Amount",
        "pay_done": "Payment Done",
        "success": "Medicine Dispensed Successfully",
        "thanks": "Thank you for using the service",
        "restart": "Restart"
    },
    "Hindi": {
        "language": "भाषा",
        "select": "चुनें",
        "next": "आगे ➡️",
        "details": "उपयोगकर्ता विवरण",
        "name": "नाम",
        "age": "आयु",
        "dob": "जन्म तिथि",
        "symptoms": "लक्षण चुनें",
        "severity": "गंभीरता",
        "duration": "अवधि (दिन)",
        "result": "निदान",
        "confidence": "विश्वास",
        "meds": "दवा योजना",
        "medicine": "दवा",
        "dose": "खुराक",
        "timing": "समय",
        "type": "प्रकार",
        "days": "दिन (1-5)",
        "total": "कुल लागत",
        "proceed": "आगे ➡️",
        "payment": "भुगतान",
        "amount": "राशि",
        "pay_done": "भुगतान पूर्ण",
        "success": "दवा सफलतापूर्वक दी गई",
        "thanks": "सेवा उपयोग करने के लिए धन्यवाद",
        "restart": "पुनः प्रारंभ"
    }
}

T = TEXT[st.session_state.lang]

# -------------------------------
# SYMPTOMS (BASE)
# -------------------------------
symptoms = [
    "Fever","Cough","Headache","Fatigue","Nausea","Vomiting",
    "Diarrhea","BodyPain","SoreThroat","RunnyNose","ChestPain",
    "Breathlessness","Acidity","AbdominalPain","Dizziness",
    "Allergy","Rash","Chills","Sweating","BurnInjury",
    "Bleeding","Swelling"
]

SYMPTOMS_T = {
    "English": {s: s for s in symptoms},
    "Hindi": {
        "Fever":"बुखार","Cough":"खांसी","Headache":"सिरदर्द","Fatigue":"थकान",
        "Nausea":"मतली","Vomiting":"उल्टी","Diarrhea":"दस्त","BodyPain":"शरीर दर्द",
        "SoreThroat":"गले में दर्द","RunnyNose":"नाक बहना","ChestPain":"छाती दर्द",
        "Breathlessness":"सांस की तकलीफ","Acidity":"अम्लता","AbdominalPain":"पेट दर्द",
        "Dizziness":"चक्कर","Allergy":"एलर्जी","Rash":"दाने","Chills":"ठंड लगना",
        "Sweating":"पसीना","BurnInjury":"जलन","Bleeding":"खून","Swelling":"सूजन"
    }
}

# -------------------------------
# DISEASE TRANSLATION
# -------------------------------
DISEASE_T = {
    "English": {},
    "Hindi": {}
}

# -------------------------------
# MEDICATION DATABASE
# -------------------------------
medications = {
    "Flu": {"name":"Paracetamol","dose":"500mg","freq":3,"timing":"After food","type":"tablet","price":5},
    "Common Cold": {"name":"Cetirizine","dose":"10mg","freq":1,"timing":"Night","type":"tablet","price":8},
    "Allergy": {"name":"Cetirizine","dose":"10mg","freq":1,"timing":"Night","type":"tablet","price":8},
    "Gastritis": {"name":"Antacid","dose":"1 tab","freq":2,"timing":"Before food","type":"tablet","price":6},
    "Food Poisoning": {"name":"ORS","dose":"1 sachet","freq":2,"timing":"After meals","type":"external","price":10},
    "Migraine": {"name":"Ibuprofen","dose":"400mg","freq":2,"timing":"After food","type":"tablet","price":7},
    "Asthma": {"name":"Salbutamol","dose":"2 puffs","freq":2,"timing":"Morning & Night","type":"inhaler","price":150},
    "Cuts Bruises": {"name":"Antiseptic","dose":"Apply","freq":2,"timing":"Morning & Night","type":"cream","price":40},
    "Burns Mild": {"name":"Burn Cream","dose":"Apply","freq":2,"timing":"Morning & Night","type":"cream","price":50},
    "Burns Severe": {"name":"Silver Cream","dose":"Apply","freq":2,"timing":"Morning & Night","type":"cream","price":120},
    "Skin Infection": {"name":"Clotrimazole","dose":"Apply","freq":2,"timing":"Morning & Night","type":"cream","price":60},
    "Viral Infection": {"name":"Paracetamol","dose":"500mg","freq":3,"timing":"After food","type":"tablet","price":5}
}

# -------------------------------
# SERVO MAPPING (1-12)
# -------------------------------
SERVO_MAP = {
    "Flu":1,"Common Cold":2,"Allergy":3,"Gastritis":4,
    "Food Poisoning":5,"Migraine":6,"Asthma":7,"Cuts Bruises":8,
    "Burns Mild":9,"Burns Severe":10,"Skin Infection":11,"Viral Infection":12
}

def get_servo_id(disease):
    return SERVO_MAP.get(disease, 0)  # 0 = phantom

# -------------------------------
# PAGE FLOW
# -------------------------------

# PAGE 1
if st.session_state.page == 0:
    st.title(T["language"])
    st.session_state.lang = st.selectbox(T["select"], ["English","Hindi"])
    st.button(T["next"], on_click=next_page)

# PAGE 2
elif st.session_state.page == 1:
    st.title(T["details"])

    st.session_state.data["name"] = st.text_input(T["name"])

    today = datetime.date.today()
    dob = st.date_input(T["dob"], min_value=datetime.date(1900,1,1), max_value=today)

    if dob:
        age = today.year - dob.year - ((today.month,today.day) < (dob.month,dob.day))
        st.session_state.data["age"] = age
        st.write(f"{T['age']}: {age}")

    st.session_state.data["dob"] = dob
    st.button(T["next"], on_click=next_page)

# PAGE 3 (SCROLL FIXED)
elif st.session_state.page == 2:
    st.title(T["symptoms"])

    with st.container():
        st.markdown("<div style='height:350px; overflow-y:auto; padding:10px; border:1px solid #ddd'>", unsafe_allow_html=True)

        data = {}
        for sym in symptoms:
            label = SYMPTOMS_T[st.session_state.lang][sym]
            data[sym] = st.checkbox(label)

        st.markdown("</div>", unsafe_allow_html=True)

    st.session_state.data["symptoms"] = data
    st.button(T["next"], on_click=next_page)

# PAGE 4
elif st.session_state.page == 3:
    severity = st.selectbox(T["severity"], ["Low","Moderate","High"])
    duration = st.number_input(T["duration"],1,30,1)

    st.session_state.data.update({
        "Condition": ["Low","Moderate","High"].index(severity),
        "Duration": duration,
        "AgeGroup": 1
    })

    st.button(T["next"], on_click=next_page)

# PAGE 5
elif st.session_state.page == 4:
    user_input = {}
    user_input.update(st.session_state.data["symptoms"])
    user_input.update({
        "Duration": st.session_state.data["Duration"],
        "AgeGroup": st.session_state.data["AgeGroup"],
        "Condition": st.session_state.data["Condition"]
    })

    result = predict(user_input)
    st.session_state.result = result

    st.success(result["prediction"])
    st.progress(result["confidence"]/100)

    st.button(T["next"], on_click=next_page)

# PAGE 6
elif st.session_state.page == 5:
    med = medications[st.session_state.result["prediction"]]

    st.write(f"{T['medicine']}: {med['name']}")
    st.write(f"{T['dose']}: {med['dose']}")
    st.write(f"{T['timing']}: {med['timing']}")
    st.write(f"{T['type']}: {med['type']}")

    days = st.number_input(T["days"],1,5,1)

    units = med["freq"] * days
    cost = round(units * med["price"] * 1.10,2)

    st.session_state.billing = {"units":units,"cost":cost}

    st.write(f"{T['total']}: ₹{cost}")
    st.button(T["proceed"], on_click=next_page)

# PAGE 7 (PAYMENT + DISPENSE)
elif st.session_state.page == 6:
    bill = st.session_state.billing

    st.write(f"{T['amount']}: ₹{bill['cost']}")
    st.code(f"upi://pay?pa=healthai@upi&am={bill['cost']}")

    if st.button(T["pay_done"]):
        if not st.session_state.dispensed:

            result = st.session_state.result
            servo_id = get_servo_id(result["prediction"])

            if HARDWARE_ENABLED and servo_id != 0:
                dispense_medicine(servo_id)
            else:
                st.warning("Simulation / Phantom mode")

            insert_record({
                "name":st.session_state.data.get("name",""),
                "age":st.session_state.data.get("age",0),
                "dob":str(st.session_state.data.get("dob","")),
                "symptoms":st.session_state.data.get("symptoms",{}),
                "disease":result["prediction"],
                "confidence":result["confidence"],
                "medicine":medications[result["prediction"]]["name"],
                "units":bill["units"],
                "cost":bill["cost"]
            })

            st.session_state.dispensed = True
            next_page()

# PAGE 8
elif st.session_state.page == 7:
    st.success(T["success"])
    st.write(T["thanks"])
    st.button(T["restart"], on_click=restart)