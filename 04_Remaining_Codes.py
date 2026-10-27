import hashlib
import base64
from pathlib import Path
import pandas as pd
import streamlit as st

# Use the supplied mining photograph as the app background.
PHOTO_FILE = Path(__file__).parent / "assets" / "mining_team.jpg"
BACKGROUND_IMAGE = "data:image/jpeg;base64," + base64.b64encode(PHOTO_FILE.read_bytes()).decode("ascii")

# Initialise login session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

# LOGIN PAGE AND APP STYLING
if not st.session_state.logged_in:
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(90deg, rgba(21,14,12,.34), rgba(22,15,12,.34)),
                    url("__MINING_BACKGROUND__") center / cover fixed no-repeat !important;
    }
    [data-testid="stHeader"] { background: transparent !important; }
    [data-testid="stMainBlockContainer"] { max-width: 1480px !important; padding-top: 9vh !important; }
    [data-testid="stMain"] h1, [data-testid="stMain"] h2,
    [data-testid="stMain"] h3 { color: #fff !important; -webkit-text-fill-color: #fff !important; }
    .khwezi-brand, .khwezi-brand * { color: white !important; -webkit-text-fill-color: white !important; }
    .khwezi-brand { padding: 0 0 22px 6px; text-shadow: 0 2px 7px rgba(0,0,0,.45); }
    .khwezi-brand-name { font-size: clamp(35px,4vw,58px); font-weight:800; letter-spacing:2px; line-height:1.1; }
    .khwezi-brand-rule { width:min(420px,90%); height:2px; background:#fff; margin:9px 0; }
    .khwezi-brand-tag { font-size:13px; letter-spacing:2px; margin:10px 0 22px; }
    .khwezi-white-slogan { color:#fff !important; -webkit-text-fill-color:#fff !important;
        font-size:clamp(24px,2.7vw,37px); font-weight:800; line-height:1.23; }
    .khwezi-brand-caption { font-size:17px; margin-top:10px; }
    /* Right-hand access portal: dark translucent panel, white labels and controls */
    [data-testid="stForm"] {
        background:rgba(23,21,20,.88) !important;
        border:1px solid rgba(255,255,255,.20) !important;
        border-radius:15px !important;
        padding:24px 30px 28px !important;
        box-shadow:0 12px 38px rgba(0,0,0,.24);
    }
    [data-testid="stForm"] label, [data-testid="stForm"] label p,
    [data-testid="stForm"] [data-testid="stWidgetLabel"] p {
        color:#fff !important; -webkit-text-fill-color:#fff !important;
    }
    [data-testid="stForm"] input {
        color:#fff !important; background:rgba(32,30,29,.9) !important;
    }
    [data-testid="stForm"] [data-baseweb="select"] > div {
        background:rgba(32,30,29,.9) !important; color:white !important;
    }
    [data-testid="stForm"] [data-baseweb="select"] span { color:#fff !important; }
    [data-testid="stForm"] [data-testid="stFormSubmitButton"] button {
        background:#fff !important; color:#161616 !important; border:1px solid #fff !important;
        width:100%; font-weight:750 !important;
    }
    [data-testid="stForm"] [data-testid="stFormSubmitButton"] button p {
        color:#161616 !important;
    }
    .khwezi-portal-head { background:rgba(23,21,20,.88); padding:25px 30px 5px;
        border-radius:15px 15px 0 0; margin-bottom:-12px; }
    .khwezi-portal-head h2 { font-size:clamp(24px,2.5vw,35px) !important; margin:0 0 12px !important; }
    .khwezi-portal-head p { color:#fff !important; font-size:15px; line-height:1.5; }
    @media(max-width:750px) {
        [data-testid="stMainBlockContainer"] { padding-top:45px !important; }
        .khwezi-brand { padding-top:0; }
    }
    </style>
    """.replace("__MINING_BACKGROUND__", BACKGROUND_IMAGE), unsafe_allow_html=True)

else:
    st.markdown("""
    <style>
    /* Main app background */
[data-testid="stAppViewContainer"] {
    background-color: #F4F6F8;
}

    /* Main text */
    .stApp,
    .stApp p,
    .stApp label,
    .stApp li {
        color: #263d4d;
    }

    h1, h2, h3 {
        color: #174f78 !important;
        font-weight: 700 !important;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span {
        color: #23465f !important;
    }

    /* Buttons */
    .stButton > button,
    .stFormSubmitButton > button,
    .stDownloadButton > button {
        background-color: #2f80bd !important;
        color: white !important;
        border: 1px solid #2f80bd !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    .stButton > button p,
    .stFormSubmitButton > button p,
    .stDownloadButton > button p {
        color: white !important;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover,
    .stDownloadButton > button:hover {
        background-color: #1d679c !important;
        border-color: #1d679c !important;
    }

    /* Tables */
    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        border: 1px solid #d5e6f2;
        border-radius: 8px;
    }
/* Dashboard metric cards */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #D5DEE8;
    border-left: 4px solid #245B85;
    padding: 18px 20px;
    border-radius: 10px;
    box-shadow: 0 3px 10px rgba(25, 55, 80, 0.08);
}

/* Metric labels */
[data-testid="stMetricLabel"] {
    color: #526579 !important;
    font-weight: 600 !important;
    white-space: normal !important;
    overflow: visible !important;
}

[data-testid="stMetricLabel"] p { white-space: normal !important; overflow-wrap: anywhere; font-size: 0.88rem !important; }
/* Metric values */
[data-testid="stMetricValue"] {
    color: #173F5F !important;
    font-weight: 800 !important;
}

/* Dashboard headings */
[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3 {
    color: #173F5F;
    font-weight: 750;
}

/* Subtle mining background for the dashboard */
[data-testid="stAppViewContainer"] {
    background:
        linear-gradient(
            rgba(239, 246, 252, 0.87),
            rgba(239, 246, 252, 0.87)
        ),
        url("__MINING_BACKGROUND__")
        center / cover fixed no-repeat;
}

/* Keep the main content clean and readable */
[data-testid="stMain"] {
    background: transparent;
}

/* Keep dashboard metric cards white */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
}

/* Clean dashboard table panels */
[data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] {
    background-color: rgba(255, 255, 255, 0.96);
    border: 1px solid #D5DEE8;
    border-radius: 12px;
    padding: 16px;
}

/* Blue section headings */
[data-testid="stMain"] h2,
[data-testid="stMain"] h3 {
    color: #173F5F !important;
    font-weight: 750 !important;
}

/* Clean table appearance */
[data-testid="stDataFrame"] {
    border: 1px solid #E0E8F0;
    border-radius: 8px;
    overflow: hidden;
}

    </style>
    """.replace("__MINING_BACKGROUND__", BACKGROUND_IMAGE), unsafe_allow_html=True)
DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(exist_ok=True)
WORKERS_FILE = DATA_DIR / "workers.csv"
INCIDENTS_FILE = DATA_DIR / "incidents.csv"
EQUIPMENT_FILE = DATA_DIR / "equipment.csv"
RISKS_FILE = DATA_DIR / "risks.csv"
ROLE_FILE = Path(__file__).resolve().parent / "role_passwords.csv"

ROLES = ["Administrator", "Safety Officer", "Mining Engineer", "Maintenance Engineer", "Manager"]
# login permissions 
PERMISSIONS = {
    "Administrator": ["Dashboard", "Worker safety", "Safety incidents", "Equipment monitoring", "Maintenance", "Risk assessment", "Alerts", "Data analysis", "Generate reports", "Manage users"],
    "Safety Officer": ["Dashboard", "Worker safety", "Safety incidents", "Risk assessment", "Alerts", "Data analysis", "Generate reports"],
    "Mining Engineer": ["Dashboard", "Worker safety", "Safety incidents", "Equipment monitoring", "Maintenance", "Risk assessment", "Alerts", "Data analysis", "Generate reports"],
    "Maintenance Engineer": ["Dashboard", "Equipment monitoring", "Maintenance", "Alerts", "Data analysis", "Generate reports"],
    "Manager": ["Dashboard", "Worker safety", "Safety incidents", "Equipment monitoring", "Maintenance", "Risk assessment", "Alerts", "Data analysis", "Generate reports"],
}

WORKER_COLUMNS = ["WorkerID", "Department", "JobRole", "Shift", "PPE_Compliance", "SafetyTrainingStatus", "FatigueLevel", "SafetyObservations", "NearMisses", "PreviousIncidents"]
INCIDENT_COLUMNS = ["IncidentID", "Date", "Time", "Shift", "Location", "Department", "IncidentType", "Severity", "InjuryStatus", "LostTimeInjury", "Cause", "CorrectiveAction", "Status"]
EQUIPMENT_COLUMNS = ["EquipmentID", "EquipmentType", "Manufacturer", "OperatingHours", "Temperature", "Vibration", "FuelConsumption", "BrakeStatus", "TyreStatus", "EngineStatus", "MaintenanceStatus", "Downtime", "Availability", "NextMaintenanceHours"]
RISK_COLUMNS = ["RiskID", "Date", "Location", "Hazard", "Likelihood", "Consequence", "RiskScore", "Classification", "Controls", "Status"]

SAMPLE_WORKERS = pd.read_csv(DATA_DIR / "workers.csv")
SAMPLE_INCIDENTS = pd.read_csv(DATA_DIR / "incidents.csv")
SAMPLE_EQUIPMENT = pd.read_csv(DATA_DIR / "equipment.csv")
SAMPLE_RISKS = pd.read_csv(DATA_DIR / "risks.csv")


def load_data(path, sample, required_columns):
    """Load CSV safely, add columns introduced by later app versions, and retain existing records."""
    if path.exists():
        try:
            df = pd.read_csv(path)
            if not df.empty:
                for col in required_columns:
                    if col not in df.columns:
                        df[col] = "" if col in ["SafetyObservations", "Manufacturer", "BrakeStatus", "TyreStatus", "EngineStatus", "MaintenanceStatus", "SafetyTrainingStatus", "IncidentType", "Severity", "InjuryStatus", "LostTimeInjury", "Cause", "CorrectiveAction", "Status", "Location", "Department", "JobRole", "Shift", "EquipmentType", "Hazard", "Controls", "Classification"] else 0
                return df[required_columns]
        except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError):
            pass
    sample.to_csv(path, index=False)
    return sample.copy()


def save_data(df, path):
    df.to_csv(path, index=False)


def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def load_role_passwords():
    if ROLE_FILE.exists():
        try:
            return pd.read_csv(ROLE_FILE, dtype=str).fillna("")
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            pass
    return pd.DataFrame(columns=["role", "password_hash"])


def risk_class(score):
    if score <= 4:
        return "Low"
    if score <= 9:
        return "Medium"
    if score <= 16:
        return "High"
    return "Critical"


def risk_alerts(risks):
    return [("CRITICAL" if str(r.get("Classification", "")) == "Critical" else "WARNING", r.get("RiskID", "Unknown"), f"{r.get('Classification')} risk: {r.get('Hazard')} (score {r.get('RiskScore')}/25).") for _, r in risks.iterrows() if str(r.get("Classification", "")) in ["High", "Critical"] and str(r.get("Status", "")).lower() != "closed"]

def equipment_alerts(equipment):
    alerts = []
    for _, e in equipment.iterrows():
        eid = e.get("EquipmentID", "Unknown")
        try:
            temp = float(e.get("Temperature", 0) or 0)
            vib = float(e.get("Vibration", 0) or 0)
            hours = float(e.get("OperatingHours", 0) or 0)
            downtime = float(e.get("Downtime", 0) or 0)
            due_at = float(e.get("NextMaintenanceHours", 0) or 0)
        except (TypeError, ValueError):
            temp, vib, hours, downtime, due_at = 0, 0, 0, 0, 0
        if temp > 100:
            alerts.append(("CRITICAL", eid, f"Temperature is {temp:g} °C — inspect equipment."))
        elif temp >= 80:
            alerts.append(("WARNING", eid, f"Temperature is {temp:g} °C — approaching critical threshold."))
        if vib > 8:
            alerts.append(("CRITICAL", eid, f"Vibration is {vib:g} mm/s — inspection required."))
        elif vib >= 5:
            alerts.append(("WARNING", eid, f"Vibration is {vib:g} mm/s — check equipment condition."))
        if str(e.get("BrakeStatus", "")).strip().lower() == "faulty":
            alerts.append(("CRITICAL", eid, "Brake fault recorded."))
        if str(e.get("EngineStatus", "")).strip().lower() in ["overheating", "faulty"]:
            alerts.append(("CRITICAL", eid, f"Engine status: {e.get('EngineStatus')}."))
        if str(e.get("MaintenanceStatus", "")).strip().lower() == "overdue":
            alerts.append(("CRITICAL", eid, "Maintenance is overdue."))
        if due_at > 0 and hours >= due_at and str(e.get("MaintenanceStatus", "")).strip().lower() not in ["in progress", "completed"]:
            alerts.append(("WARNING", eid, f"Maintenance due: operating hours ({hours:g}) reached next service point ({due_at:g})."))
        if downtime >= 24:
            alerts.append(("WARNING", eid, f"High downtime recorded: {downtime:g} hours."))
        if hours + downtime > 0 and hours / (hours + downtime) * 100 < 80:
            alerts.append(("WARNING", eid, f"Low calculated availability: {hours / (hours + downtime) * 100:.1f}%."))
    return alerts


def worker_alerts(workers):
    alerts = []
    for _, w in workers.iterrows():
        wid = w.get("WorkerID", "Unknown")
        try:
            ppe = float(w.get("PPE_Compliance", 100) or 0)
            fatigue = float(w.get("FatigueLevel", 1) or 1)
            near = float(w.get("NearMisses", 0) or 0)
            prev = float(w.get("PreviousIncidents", 0) or 0)
        except (TypeError, ValueError):
            ppe, fatigue, near, prev = 100, 1, 0, 0
        if ppe < 70:
            alerts.append(("CRITICAL", wid, f"Low PPE compliance: {ppe:g}%."))
        if str(w.get("SafetyTrainingStatus", "")).strip().lower() == "pending":
            alerts.append(("WARNING", wid, "Safety training is pending."))
        if fatigue >= 4:
            alerts.append(("CRITICAL" if fatigue >= 5 else "WARNING", wid, f"High fatigue level: {fatigue:g}/5."))
        if near > 0:
            alerts.append(("WARNING", wid, f"{near:g} near miss(es) recorded."))
        if prev >= 2:
            alerts.append(("WARNING", wid, f"Previous incidents recorded: {prev:g}."))
        obs = str(w.get("SafetyObservations", "")).lower()
        if any(word in obs for word in ["high risk", "unsafe", "danger", "hazard"]):
            alerts.append(("WARNING", wid, f"Review safety observation: {w.get('SafetyObservations')}"))
    return alerts


def incident_alerts(incidents):
    alerts = []
    for _, i in incidents.iterrows():
        if str(i.get("Severity", "")).lower() in ["high", "critical"] or str(i.get("LostTimeInjury", "")).lower() == "yes":
            alerts.append(("CRITICAL", i.get("IncidentID", "Unknown"), f"Incident needs attention: {i.get('Severity')} severity; status {i.get('Status')}."))
    return alerts

#LOGIN 
role_passwords = load_role_passwords()
configured_roles = set(role_passwords.get("role", pd.Series(dtype=str)).astype(str))
if not set(ROLES).issubset(configured_roles):
    st.subheader("First-time setup: create role passwords")
    st.info("Create one password for each role. This educational prototype uses shared role passwords, not individual user accounts.")
    with st.form("setup_passwords"):
        password_values = {r: st.text_input(f"Create password for {r}", type="password", key=f"setup_{r}") for r in ROLES}
        setup = st.form_submit_button("Save role passwords")
    if setup:
        if any(not p.strip() for p in password_values.values()):
            st.error("Enter a password for every role.")
        elif any(len(p) < 8 for p in password_values.values()):
            st.error("Use at least 8 characters for each password.")
        else:
            pd.DataFrame([{"role": r, "password_hash": hash_password(p)} for r, p in password_values.items()]).to_csv(ROLE_FILE, index=False)
            st.success("Role passwords saved. You can now log in.")
            st.rerun()
    st.stop()


if not st.session_state.logged_in:
    left, right = st.columns([1.3, 1], gap="large")

    with left:
        st.markdown("""
        <div class="khwezi-brand">
            <div style="font-size:58px; line-height:1;">&#9651;</div>
            <div class="khwezi-brand-name">KHWEZI MINING</div>
            <div class="khwezi-brand-rule"></div>
            <div class="khwezi-brand-tag">HEALTH | SAFETY | EQUIPMENT | PEOPLE | PERFORMANCE</div>
            <div class="khwezi-white-slogan">EVERY SHIFT MATTERS.<br>EVERY WARNING COUNTS.</div>
            <div class="khwezi-brand-caption">Monitoring today for a safer, more productive tomorrow.</div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="khwezi-portal-head">
            <h2>OPERATIONS ACCESS PORTAL</h2>
            <p>Sign in to access the Khwezi Mining Monitoring System</p>
        </div>
        """, unsafe_allow_html=True)
        with st.form("login_form"):
            selected_role = st.selectbox("Select Role", ROLES)
            entered_password = st.text_input(
                "Password", type="password", placeholder="Enter your password"
            )
            login = st.form_submit_button("Sign In", use_container_width=True)

        if login:
            match = role_passwords[
                role_passwords["role"] == selected_role
            ]

            if (
                not match.empty
                and hash_password(entered_password)
                == match.iloc[0]["password_hash"]
            ):
                st.session_state.logged_in = True
                st.session_state.role = selected_role
                st.rerun()
            else:
                st.error(
                    "ACCESS DENIED: Incorrect password for the selected role."
                )

    st.stop()
role = st.session_state.role
st.sidebar.markdown("""
<div style="padding: 12px 0 18px 0;">
    <h2 style="color: #F4C430; margin-bottom: 0;">
        KHWEZI MINING
    </h2>
    <p style="color: #D1D5DB; font-size: 13px;">
        HEALTH, SAFETY & EQUIPMENT INTELLIGENCE
    </p>
    <hr style="border: 1px solid #F4C430;">
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(
    f"**Logged in as:** {role}"
)
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.role = ""
    st.rerun()

# Load and persist data after login.
if "workers" not in st.session_state:
    st.session_state.workers = load_data(WORKERS_FILE, SAMPLE_WORKERS, WORKER_COLUMNS)
if "incidents" not in st.session_state:
    st.session_state.incidents = load_data(INCIDENTS_FILE, SAMPLE_INCIDENTS, INCIDENT_COLUMNS)
if "equipment" not in st.session_state:
    st.session_state.equipment = load_data(EQUIPMENT_FILE, SAMPLE_EQUIPMENT, EQUIPMENT_COLUMNS)
if "risks" not in st.session_state:
    st.session_state.risks = load_data(RISKS_FILE, SAMPLE_RISKS, RISK_COLUMNS)

section = st.sidebar.selectbox("Choose a function", PERMISSIONS.get(role, []))
workers = st.session_state.workers
incidents = st.session_state.incidents
equipment = st.session_state.equipment
risks = st.session_state.risks

# DATA ANALYSIS 
elif section == "Data analysis":
    st.header("Interactive Mining Data Analysis")
    if role == "Maintenance Engineer":
        st.info("Only equipment-related analysis is available for this role.")
    analysis_options = ["Incidents by department", "Incidents by shift", "Incident types", "PPE compliance by department", "Equipment with highest downtime", "Equipment with lowest availability", "Equipment with highest temperature", "Equipment with highest vibration", "Equipment maintenance priority"]
    if role == "Maintenance Engineer":
        analysis_options = [item for item in analysis_options if item not in ["Incidents by department", "Incidents by shift", "Incident types", "PPE compliance by department"]]
    if role == "Safety Officer":
        analysis_options = [item for item in analysis_options if item in ["Incidents by department", "Incidents by shift", "Incident types", "PPE compliance by department"]]
    analysis_topic = st.selectbox("Choose a question", analysis_options)
    if analysis_topic == "Incidents by department":
        result = incidents.groupby("Department").size().sort_values(ascending=False).rename("Incident count")
        st.write("Which department has the highest number of incidents?"); st.bar_chart(result); st.dataframe(result)
    elif analysis_topic == "Incidents by shift":
        result = incidents.groupby("Shift").size().sort_values(ascending=False).rename("Incident count")
        st.write("Which shift records the most incidents?"); st.bar_chart(result); st.dataframe(result)
    elif analysis_topic == "Incident types":
        result = incidents.groupby("IncidentType").size().sort_values(ascending=False).rename("Incident count")
        st.write("Which incident types occur most frequently?"); st.bar_chart(result); st.dataframe(result)
    elif analysis_topic == "PPE compliance by department":
        result = workers.assign(PPE_Compliance=pd.to_numeric(workers["PPE_Compliance"], errors="coerce")).groupby("Department")["PPE_Compliance"].mean().sort_values(ascending=False)
        st.write("What is the average recorded PPE compliance in each department?"); st.bar_chart(result); st.dataframe(result)
    elif analysis_topic == "Equipment with highest downtime":
        result = equipment.assign(Downtime=pd.to_numeric(equipment["Downtime"], errors="coerce")).sort_values("Downtime", ascending=False)
        st.dataframe(result[["EquipmentID", "EquipmentType", "Downtime"]], use_container_width=True)
        if not result.empty: st.write(f"Highest downtime: {result.iloc[0]['EquipmentID']} — {result.iloc[0]['Downtime']} hours.")
    elif analysis_topic == "Equipment with lowest availability":
        result = equipment.copy()
        operating = pd.to_numeric(result["OperatingHours"], errors="coerce")
        downtime = pd.to_numeric(result["Downtime"], errors="coerce")
        result["Availability"] = (100 * operating / (operating + downtime).replace(0, float("nan"))).round(1)
        result = result.sort_values("Availability", ascending=True)
        st.dataframe(result[["EquipmentID", "EquipmentType", "Availability"]], use_container_width=True)
        if not result.empty: st.write(f"Lowest recorded availability: {result.iloc[0]['EquipmentID']} — {result.iloc[0]['Availability']}%.")
    elif analysis_topic == "Equipment with highest temperature":
        result = equipment.assign(Temperature=pd.to_numeric(equipment["Temperature"], errors="coerce")).sort_values("Temperature", ascending=False)
        st.dataframe(result[["EquipmentID", "EquipmentType", "Temperature"]], use_container_width=True)
        if not result.empty: st.write(f"Highest recorded temperature: {result.iloc[0]['EquipmentID']} — {result.iloc[0]['Temperature']} °C.")
    elif analysis_topic == "Equipment with highest vibration":
        result = equipment.assign(Vibration=pd.to_numeric(equipment["Vibration"], errors="coerce")).sort_values("Vibration", ascending=False)
        st.dataframe(result[["EquipmentID", "EquipmentType", "Vibration"]], use_container_width=True)
        if not result.empty: st.write(f"Highest recorded vibration: {result.iloc[0]['EquipmentID']} — {result.iloc[0]['Vibration']} mm/s.")
    else:
        priority = equipment.copy()
        priority["Downtime"] = pd.to_numeric(priority["Downtime"], errors="coerce").fillna(0)
        priority["Temperature"] = pd.to_numeric(priority["Temperature"], errors="coerce").fillna(0)
        priority["Vibration"] = pd.to_numeric(priority["Vibration"], errors="coerce").fillna(0)
        operating = pd.to_numeric(priority["OperatingHours"], errors="coerce")
        priority["Availability"] = (100 * operating / (operating + priority["Downtime"]).replace(0, float("nan"))).fillna(100)
        priority["PriorityScore"] = (priority["MaintenanceStatus"].astype(str).str.lower().isin(["overdue", "due"]).astype(int) * 4 + (priority["Temperature"] > 100).astype(int) * 3 + (priority["Vibration"] > 8).astype(int) * 3 + (priority["Downtime"] >= 24).astype(int) * 2 + (priority["Availability"] < 80).astype(int) * 2 + (priority["BrakeStatus"].astype(str).str.lower() == "faulty").astype(int) * 3)
        priority = priority.sort_values("PriorityScore", ascending=False)
        st.write("A simple prioritisation score ranks records for review; it is not a formal engineering standard.")
        st.dataframe(priority[["EquipmentID", "EquipmentType", "MaintenanceStatus", "Downtime", "Availability", "PriorityScore"]], use_container_width=True)

