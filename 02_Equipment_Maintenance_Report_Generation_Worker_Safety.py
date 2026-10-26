# WORKER SAFETY 
elif section == "Worker safety":
    st.header("Worker Health and Safety Monitoring")
    st.dataframe(workers, use_container_width=True)
    st.subheader("Worker safety alerts")
    alerts = worker_alerts(workers)
    if alerts:
        st.dataframe(pd.DataFrame(alerts, columns=["Level", "Worker ID", "Message"]), use_container_width=True)
    else:
        st.success("No worker safety alerts from current records.")
    if role in ["Administrator", "Safety Officer"]:
        st.subheader("Add worker record")
        with st.form("worker_form", clear_on_submit=True):
            wid = st.text_input("Worker ID")
            dept = st.selectbox("Department", ["Drilling", "Hauling", "Maintenance", "Blasting", "Processing", "Other"])
            job = st.text_input("Job role")
            shift = st.selectbox("Shift", ["Day", "Night"])
            ppe = st.number_input("PPE compliance (%)", min_value=0, max_value=100, value=100)
            training = st.selectbox("Safety training", ["Completed", "Pending"])
            fatigue = st.slider("Fatigue level (1–5)", 1, 5, 1)
            obs = st.text_input("Safety observation / hazard")
            near = st.number_input("Near misses", min_value=0, step=1)
            prev = st.number_input("Previous incidents", min_value=0, step=1)
            save = st.form_submit_button("Save worker")
        if save:
            if not wid.strip() or not job.strip():
                st.error("Worker ID and job role are required.")
            elif wid.strip() in workers["WorkerID"].astype(str).values:
                st.error("That Worker ID already exists.")
            else:
                row = pd.DataFrame([{"WorkerID":wid.strip(), "Department":dept, "JobRole":job.strip(), "Shift":shift, "PPE_Compliance":ppe, "SafetyTrainingStatus":training, "FatigueLevel":fatigue, "SafetyObservations":obs, "NearMisses":near, "PreviousIncidents":prev}])
                st.session_state.workers = pd.concat([workers, row], ignore_index=True)[WORKER_COLUMNS]
                save_data(st.session_state.workers, WORKERS_FILE)
                st.success("Worker record saved.")
                st.rerun()


# MAINTENANCE 
elif section == "Maintenance":
    st.header("Equipment Maintenance Monitoring")
    eq = equipment.copy()
    for col in ["OperatingHours", "Downtime", "Availability", "NextMaintenanceHours"]:
        eq[col] = pd.to_numeric(eq[col], errors="coerce").fillna(0)
    denominator = eq["OperatingHours"] + eq["Downtime"]
    eq["CalculatedAvailability"] = (eq["OperatingHours"] / denominator.replace(0, float("nan")) * 100).fillna(100)
    eq.loc[denominator == 0, "CalculatedAvailability"] = 100
    eq["MaintenanceDue"] = (eq["NextMaintenanceHours"] > 0) & (eq["OperatingHours"] >= eq["NextMaintenanceHours"])
    eq["RepeatedAlertCount"] = eq["EquipmentID"].apply(lambda eid: sum(1 for a in equipment_alerts(equipment) if a[1] == eid))
    st.write("Availability = Operating time ÷ (Operating time + Downtime) × 100")
    st.dataframe(eq[["EquipmentID", "EquipmentType", "OperatingHours", "Downtime", "CalculatedAvailability", "MaintenanceStatus", "MaintenanceDue", "RepeatedAlertCount"]], use_container_width=True)
    overdue = eq[eq["MaintenanceStatus"].astype(str).str.lower() == "overdue"]
    under_maintenance = eq[eq["MaintenanceStatus"].astype(str).str.lower() == "in progress"]
    due = eq[eq["MaintenanceDue"] | (eq["MaintenanceStatus"].astype(str).str.lower().isin(["due", "due soon"]))]
    high_down = eq[eq["Downtime"] >= 24]
    low_avail = eq[eq["CalculatedAvailability"] < 80]
    repeated = eq[eq["RepeatedAlertCount"] >= 2]
    a, b, c = st.columns(3)
    a.metric("Overdue", len(overdue)); b.metric("Due for maintenance", len(due)); c.metric("Under maintenance", len(under_maintenance))
    st.subheader("Maintenance lists")
    for title, frame in [("Overdue equipment", overdue), ("Due for maintenance", due), ("Under maintenance", under_maintenance), ("Excessive downtime (24+ hours)", high_down), ("Low availability (below 80%)", low_avail), ("Repeated alerts (2+)", repeated)]:
        with st.expander(title):
            if frame.empty: st.write("No records match this condition.")
            else: st.dataframe(frame, use_container_width=True)


# REPORTS 
elif section == "Generate reports":
    st.header("Generate Reports")
    report_options = ["Worker safety report", "Safety incidents report", "Equipment report", "Risk assessment report", "Current alerts report"]
    if role == "Maintenance Engineer":
        report_options = ["Equipment report", "Current alerts report"]
    elif role == "Safety Officer":
        report_options = ["Worker safety report", "Safety incidents report", "Risk assessment report", "Current alerts report"]
    report_choice = st.selectbox("Choose report", report_options)
    if report_choice == "Worker safety report": report, filename = workers, "worker_safety_report.csv"
    elif report_choice == "Safety incidents report": report, filename = incidents, "safety_incidents_report.csv"
    elif report_choice == "Equipment report": report, filename = equipment, "equipment_report.csv"
    elif report_choice == "Risk assessment report": report, filename = risks, "risk_assessment_report.csv"
    else:
        report = pd.DataFrame(worker_alerts(workers) + incident_alerts(incidents) + equipment_alerts(equipment) + risk_alerts(risks), columns=["Level", "Record ID", "Message"])
        filename = "current_alerts_report.csv"
    st.dataframe(report, use_container_width=True)
    st.download_button("Download CSV report", report.to_csv(index=False).encode("utf-8"), file_name=filename, mime="text/csv")

