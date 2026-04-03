import streamlit as st
from model import predict
from database import init_db, insert_record
import datetime
import time
import requests  # ✅ NEW

# -------------------------------
# CLOUD SERVER URL (REPLACE THIS)
# -------------------------------
BASE_URL = "https://your-url.trycloudflare.com"  # ✅ CHANGE THIS

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
st.set_page_config(page_title="Health AI", layout="centered")

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
if "busy" not in st.session_state:
    st.session_state.busy = False

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
# MOTOR FUNCTION (UPDATED)
# -------------------------------
def send_motor(cmd, spins=1):
    if st.session_state.busy:
        st.warning("Motor busy")
        return

    st.session_state.busy = True

    try:
        for _ in range(spins):
            url = f"{BASE_URL}/med/{cmd.replace('MED','')}"
            r = requests.get(url, timeout=5)
            st.write(r.json())
            time.sleep(1.2)

        st.success(f"{cmd} x{spins}")

    except Exception as e:
        st.error(e)

    st.session_state.busy = False


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
# SYMPTOMS
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
    "Viral Infection": {"name":"Paracetamol","dose":"500mg","freq":3,"timing":"After food","type":"tablet","price":5},

    "Typhoid": {"name":"Doctor Consultation Required","price":0},
    "Dengue": {"name":"Doctor Consultation Required","price":0},
    "Pneumonia": {"name":"Doctor Consultation Required","price":0}
}

# -------------------------------
# DISEASE → MOTOR
# -------------------------------
disease_to_motor = {
    "Flu": "MED1", "Viral Infection": "MED1", "Common Cold": "MED1",
    "Allergy": "MED2", "Gastritis": "MED2", "Food Poisoning": "MED2",
    "Migraine": "MED3", "Asthma": "MED3", "Skin Infection": "MED3",
    "Cuts Bruises": "MED4", "Burns Mild": "MED4", "Burns Severe": "MED4",
    "Typhoid": None, "Dengue": None, "Pneumonia": None
}

# -------------------------------
# MOTOR FUNCTION
# -------------------------------
def send_motor(cmd, spins=1):
    if st.session_state.busy:
        st.warning("Motor busy")
        return

    st.session_state.busy = True

    try:
        for _ in range(spins):
            if HARDWARE_ENABLED:
                dispense_medicine(cmd)
            else:
                st.write(f"[SIMULATION] {cmd}")
            time.sleep(1.2)

        st.success(f"{cmd} x{spins}")

    except Exception as e:
        st.error(e)

    st.session_state.busy = False

# -------------------------------
# PAGE FLOW
# -------------------------------
if st.session_state.page == 0:
    st.title(T["language"])
    st.session_state.lang = st.selectbox(T["select"], ["English","Hindi"])
    st.button(T["next"], on_click=next_page)

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

elif st.session_state.page == 2:
    st.title(T["symptoms"])

    data = {}
    for sym in symptoms:
        data[sym] = st.checkbox(SYMPTOMS_T[st.session_state.lang][sym])

    st.session_state.data["symptoms"] = data
    st.button(T["next"], on_click=next_page)

elif st.session_state.page == 3:
    severity = st.selectbox(T["severity"], ["Low","Moderate","High"])
    duration = st.number_input(T["duration"],1,30,1)

    st.session_state.data.update({
        "Condition": ["Low","Moderate","High"].index(severity),
        "Duration": duration,
        "AgeGroup": 1
    })

    st.button(T["next"], on_click=next_page)

elif st.session_state.page == 4:
    user_input = {}
    user_input.update(st.session_state.data["symptoms"])
    user_input.update({
        "Duration": st.session_state.data["Duration"],
        "AgeGroup": 1,
        "Condition": st.session_state.data["Condition"]
    })

    result = predict(user_input)
    st.session_state.result = result

    st.success(result["prediction"])
    st.progress(result["confidence"]/100)

    st.button(T["next"], on_click=next_page)

elif st.session_state.page == 5:
    disease = st.session_state.result["prediction"]
    med = medications[disease]

    if med["price"] == 0:
        st.warning("⚠ No automated medicine available. Please consult a doctor.")
        st.session_state.billing = {"units":0,"cost":0,"days":0}
        st.button(T["proceed"], on_click=next_page)
    else:
        st.write(f"{T['medicine']}: {med['name']}")
        st.write(f"{T['dose']}: {med['dose']}")
        st.write(f"{T['timing']}: {med['timing']}")
        st.write(f"{T['type']}: {med['type']}")

        days = st.number_input(T["days"],1,5,1)
        units = med["freq"] * days
        cost = round(units * med["price"] * 1.10,2)

        st.session_state.billing = {"units":units,"cost":cost,"days":days}

        st.write(f"{T['total']}: ₹{cost}")
        st.button(T["proceed"], on_click=next_page)

elif st.session_state.page == 6:
    bill = st.session_state.billing
    st.write(f"{T['amount']}: ₹{bill['cost']}")

    if st.button(T["pay_done"]):

        if not st.session_state.dispensed:

            disease = st.session_state.result["prediction"]
            motor_cmd = disease_to_motor.get(disease)

            if motor_cmd:
                spins = max(1, bill["days"])
                send_motor(motor_cmd, spins)  # ✅ FIXED
            else:
                st.warning("Doctor consultation required")

            insert_record({
                "name": st.session_state.data.get("name",""),
                "age": st.session_state.data.get("age",0),
                "dob": str(st.session_state.data.get("dob","")),
                "symptoms": st.session_state.data.get("symptoms",{}),
                "disease": disease,
                "confidence": st.session_state.result["confidence"],
                "medicine": medications[disease]["name"],
                "units": bill["units"],
                "cost": bill["cost"]
            })

            st.session_state.dispensed = True
            next_page()

elif st.session_state.page == 7:
    st.success(T["success"])
    st.write(T["thanks"])
    st.button(T["restart"], on_click=restart)