#DASHBOARD 
if section == "Dashboard":
    st.title("Operations Overview")
    st.caption("KHWEZI MINING | One clear view of workforce safety, equipment reliability and operational risk.")
    all_alerts = worker_alerts(workers) + incident_alerts(incidents) + equipment_alerts(equipment) + risk_alerts(risks)
    high_risks = risks[risks.get("Classification", pd.Series(dtype=str)).isin(["High", "Critical"])] if not risks.empty else risks
    ppe_mean = pd.to_numeric(workers["PPE_Compliance"], errors="coerce").mean() if not workers.empty else 0
    availability_mean = (100 * pd.to_numeric(equipment["OperatingHours"], errors="coerce") / (pd.to_numeric(equipment["OperatingHours"], errors="coerce") + pd.to_numeric(equipment["Downtime"], errors="coerce")).replace(0, float("nan"))).mean() if not equipment.empty else 0
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total workers", len(workers))
    c2.metric("Safety incidents", len(incidents))
    c3.metric("Near misses", int(pd.to_numeric(workers["NearMisses"], errors="coerce").fillna(0).sum()))
    c4.metric("High/critical risks", len(high_risks))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Average PPE compliance", f"{ppe_mean:.1f}%" if pd.notna(ppe_mean) else "N/A")
    c2.metric("Equipment items", len(equipment))
    c3.metric("Equipment alerts", len(equipment_alerts(equipment)))
    c4.metric("Average availability", f"{availability_mean:.1f}%" if pd.notna(availability_mean) else "N/A")    
    available_count = int((equipment["MaintenanceStatus"].astype(str).str.lower() != "in progress").sum())
    under_maintenance = int((equipment["MaintenanceStatus"].astype(str).str.lower() == "in progress").sum())
    critical_equipment_alerts = sum(level == "CRITICAL" for level, _, _ in equipment_alerts(equipment))
    d1, d2, d3 = st.columns(3)
    d1.metric("Equipment not in maintenance", available_count)
    d2.metric("Under maintenance", under_maintenance)
    d3.metric("Critical equipment alerts", critical_equipment_alerts)
    st.subheader("Priority alerts")
    st.caption("Review alerts generated from recorded worker, incident and equipment data.")

    if all_alerts:
        df_priority = pd.DataFrame(
            all_alerts,
            columns=["Level", "Record ID", "Message"]
        )

        st.dataframe(
            df_priority,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Level": st.column_config.TextColumn("Alert Level"),
                "Record ID": st.column_config.TextColumn("Record ID"),
                "Message": st.column_config.TextColumn(
                    "Alert Details",
                    width="large"
                )
            }
        )
    else:
        st.success("No alerts generated from the current records.")


# RISK ASSESSMENT 
elif section == "Risk assessment":
    st.header("Basic Mining Risk Assessment")
    st.warning("This simple educational assessment does not replace a formal site risk assessment or approved mine procedure.")
    st.write("Risk score = Likelihood × Consequence. Both use a scale from 1 (lowest) to 5 (highest).")
    st.dataframe(risks, use_container_width=True)
    if not risks.empty:
        high = risks[risks["Classification"].isin(["High", "Critical"])]
        if not high.empty: st.error(f"{len(high)} high/critical risk record(s) require attention."); st.dataframe(high, use_container_width=True)
    if role in ["Administrator", "Safety Officer", "Mining Engineer"]:
        with st.form("risk_form", clear_on_submit=True):
            rid = st.text_input("Risk ID")
            date = st.date_input("Assessment date")
            location = st.text_input("Location / work area")
            hazard = st.text_input("Hazard or unsafe condition")
            likelihood = st.slider("Likelihood (1–5)", 1, 5, 3)
            consequence = st.slider("Consequence (1–5)", 1, 5, 3)
            controls = st.text_input("Existing / proposed controls")
            status = st.selectbox("Status", ["Open", "Controlled", "Closed"])
            submit = st.form_submit_button("Calculate and save risk")
        if submit:
            score = likelihood * consequence
            classification = risk_class(score)
            if not rid.strip() or not hazard.strip(): st.error("Risk ID and hazard are required.")
            elif rid.strip() in risks["RiskID"].astype(str).values: st.error("That Risk ID already exists.")
            else:
                row = pd.DataFrame([{"RiskID":rid.strip(), "Date":str(date), "Location":location.strip(), "Hazard":hazard.strip(), "Likelihood":likelihood, "Consequence":consequence, "RiskScore":score, "Classification":classification, "Controls":controls, "Status":status}])
                st.session_state.risks = pd.concat([risks, row], ignore_index=True)[RISK_COLUMNS]
                save_data(st.session_state.risks, RISKS_FILE)
                if classification in ["High", "Critical"]: st.error(f"{classification} risk! Score: {score}/25. Review controls promptly.")
                else: st.success(f"{classification} risk. Score: {score}/25.")
                st.rerun()

# CENTRAL ALERTS 
elif section == "Alerts":
    st.header("Alerts and Notifications")
    alerts = worker_alerts(workers) + incident_alerts(incidents) + equipment_alerts(equipment) + risk_alerts(risks)
    if alerts:
        df_alerts = pd.DataFrame(alerts, columns=["Level", "Record ID", "Message"])
        st.dataframe(df_alerts, use_container_width=True)
        st.metric("Critical alerts", int((df_alerts["Level"] == "CRITICAL").sum()))
        st.metric("Warning alerts", int((df_alerts["Level"] == "WARNING").sum()))
    else:
        st.success("No alerts generated from current records.")
    st.caption("Alerts use educational prototype thresholds and saved records, not live sensor data or mine safety limits.")

