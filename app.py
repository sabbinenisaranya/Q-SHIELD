import streamlit as st
from streamlit_autorefresh import st_autorefresh

from pipeline import QShieldPipeline
from crypto.public_key_loader import load_public_key
from database.database import (
    initialize_database,
    insert_event,
    get_events
)
from dashboard.analytics import get_dashboard_data
from reports.report_generator import generate_security_report


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Q-SHIELD | Cyber Threat Detection",
    page_icon="🛡️",
    layout="wide"
)


# ============================================================
# AUTOMATIC DASHBOARD REFRESH
# ============================================================

st_autorefresh(
    interval=10000,
    key="qshield_dashboard_refresh"
)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

initialize_database()


# ============================================================
# PIPELINE INITIALIZATION
# ============================================================

if "pipeline" not in st.session_state:
    st.session_state.pipeline = QShieldPipeline()

pipeline = st.session_state.pipeline


# ============================================================
# HEADER
# ============================================================

st.title("🛡️ Q-SHIELD")

st.markdown(
    """
    **Quantum-Inspired Cyber Threat Detection for Digital Signatures**

    Monitor digital-signing activity, detect anomalous behavior,
    calculate threat scores, and identify potential signature misuse.
    """
)

st.divider()


# ============================================================
# SECURITY DASHBOARD
# ============================================================

st.header("📊 Security Dashboard")

dashboard_data = get_dashboard_data()


# ============================================================
# SECURITY ALERTS
# ============================================================

st.subheader("🚨 Security Alerts")

alerts = dashboard_data.get("alerts", [])

if alerts:

    st.error(
        f"🚨 {len(alerts)} HIGH/CRITICAL SECURITY ALERT(S) DETECTED"
    )

    for alert in alerts[:5]:

        risk = alert["risk_level"]

        if risk == "CRITICAL":

            st.error(
                f"🔴 CRITICAL | "
                f"Event #{alert['event_id']} | "
                f"Score: {alert['threat_score']} | "
                f"{alert['threat_type']}"
            )

        else:

            st.warning(
                f"🟠 HIGH | "
                f"Event #{alert['event_id']} | "
                f"Score: {alert['threat_score']} | "
                f"{alert['threat_type']}"
            )

        st.caption(
            f"Time: {alert['timestamp']}  |  "
            f"Document: {alert['document_id']}  |  "
            f"Device: {alert['device_id']}  |  "
            f"Location: {alert['location']}"
        )

else:

    st.success(
        "🟢 No HIGH or CRITICAL security alerts."
    )


# ============================================================
# DASHBOARD METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Events",
        dashboard_data["total_events"]
    )

with col2:

    st.metric(
        "High Risk Events",
        dashboard_data["high_risk_events"]
    )

with col3:

    st.metric(
        "Critical Events",
        dashboard_data["critical_events"]
    )

with col4:

    st.metric(
        "Average Threat Score",
        dashboard_data["average_threat_score"]
    )


st.divider()


# ============================================================
# RISK DISTRIBUTION
# ============================================================

st.subheader("📈 Risk Distribution")

risk_distribution = dashboard_data["risk_distribution"]

if risk_distribution:

    st.bar_chart(
        risk_distribution
    )

else:

    st.info(
        "No risk data available yet."
    )


# ============================================================
# THREAT TYPE DISTRIBUTION
# ============================================================

st.subheader("⚠️ Threat Type Distribution")

threat_distribution = dashboard_data[
    "threat_distribution"
]

if threat_distribution:

    st.bar_chart(
        threat_distribution
    )

else:

    st.info(
        "No threat type data available yet."
    )


# ============================================================
# THREAT SCORE TIMELINE
# ============================================================

st.subheader("📊 Threat Score Timeline")

score_timeline = dashboard_data[
    "score_timeline"
]

if score_timeline:

    timeline_data = {
        event["timestamp"]: event["threat_score"]
        for event in score_timeline
    }

    st.line_chart(
        timeline_data
    )

else:

    st.info(
        "No threat score history available yet."
    )


st.divider()


# ============================================================
# DIGITAL DOCUMENT ANALYSIS
# ============================================================

st.header("📄 Digital Document Analysis")

st.markdown(
    """
    Upload a document to generate a digital signature and
    analyze its signing behavior.
    """
)

document_file = st.file_uploader(
    "Upload Document",
    type=["pdf", "txt", "doc", "docx"],
    key="document_analysis"
)


if document_file:

    document_bytes = document_file.read()

    st.info(
        f"Document loaded: {document_file.name}"
    )

    if st.button(
        "🔍 Analyze Document",
        key="analyze_document"
    ):

        with st.spinner(
            "Running Q-SHIELD threat analysis..."
        ):

            try:

                # ------------------------------------------------
                # RUN ANALYSIS
                # ------------------------------------------------

                result = pipeline.analyze(
                    document_bytes
                )


                # ------------------------------------------------
                # SAVE EVENT TO DATABASE
                # ------------------------------------------------

                insert_event(
                    user_id=result["user_id"],
                    document_id=document_file.name,
                    timestamp=result["timestamp"],
                    device_id=result["device_id"],
                    ip_address=result["ip_address"],
                    location=result["location"],
                    signature_valid=result["signature_valid"],
                    signing_frequency=result["behavior"][
                        "signing_frequency"
                    ],
                    device_change=result["behavior"][
                        "device_change"
                    ],
                    location_change=result["behavior"][
                        "location_change"
                    ],
                    activity_hour=result["behavior"][
                        "activity_hour"
                    ],
                    failed_attempts=result["behavior"][
                        "failed_attempts"
                    ],
                    signature_count=result["behavior"][
                        "signature_count"
                    ],
                    anomaly_score=result["anomaly_score"],
                    quantum_score=result["quantum_score"],
                    threat_score=result["threat_score"],
                    risk_level=result["risk_level"],
                    threat_type=result["threat_type"]
                )


                # ------------------------------------------------
                # ANALYSIS SUCCESS
                # ------------------------------------------------

                st.success(
                    "✅ Document analysis completed."
                )


                # ------------------------------------------------
                # GENERATE PDF SECURITY REPORT
                # ------------------------------------------------

                try:

                    report_path = generate_security_report(
                        result,
                        document_file.name
                    )

                    st.subheader(
                        "📄 Security Report"
                    )

                    st.success(
                        "✅ PDF security report generated."
                    )

                    report_bytes = report_path.read_bytes()

                    st.download_button(
                        label="⬇️ Download PDF Security Report",
                        data=report_bytes,
                        file_name=report_path.name,
                        mime="application/pdf",
                        key="download_document_report"
                    )

                except Exception as error:

                    st.error(
                        "❌ Could not generate security report."
                    )

                    st.exception(error)


                # ------------------------------------------------
                # DIGITAL SIGNATURE
                # ------------------------------------------------

                st.subheader(
                    "🔐 Digital Signature"
                )

                st.write(
                    "Document SHA-256 Hash:"
                )

                st.code(
                    result["document_hash"]
                )

                st.write(
                    "Generated Digital Signature:"
                )

                st.code(
                    result["signature"].hex()
                )


                # ------------------------------------------------
                # SIGNATURE STATUS
                # ------------------------------------------------

                st.subheader(
                    "✅ Signature Verification"
                )

                if result["signature_valid"]:

                    st.success(
                        "VALID DIGITAL SIGNATURE"
                    )

                else:

                    st.error(
                        "INVALID DIGITAL SIGNATURE"
                    )


                # ------------------------------------------------
                # ML ANALYSIS
                # ------------------------------------------------

                st.subheader(
                    "🤖 ML Anomaly Detection"
                )

                ml_col1, ml_col2 = st.columns(2)

                with ml_col1:

                    st.metric(
                        "Anomaly Score",
                        round(
                            result["anomaly_score"],
                            4
                        )
                    )

                with ml_col2:

                    st.metric(
                        "Classification",
                        result["ml_classification"]
                    )


                # ------------------------------------------------
                # QUANTUM-INSPIRED ANALYSIS
                # ------------------------------------------------

                st.subheader(
                    "⚛️ Quantum-Inspired Analysis"
                )

                quantum_col1, quantum_col2 = st.columns(2)

                with quantum_col1:

                    st.metric(
                        "Quantum-Inspired Score",
                        round(
                            result["quantum_score"],
                            4
                        )
                    )

                with quantum_col2:

                    st.write(
                        "Optimized Feature Weights"
                    )

                    st.write(
                        result["quantum_weights"]
                    )


                # ------------------------------------------------
                # THREAT SCORE
                # ------------------------------------------------

                st.subheader(
                    "🚨 Threat Assessment"
                )

                threat_col1, threat_col2, threat_col3 = st.columns(
                    3
                )

                with threat_col1:

                    st.metric(
                        "Threat Score",
                        result["threat_score"]
                    )

                with threat_col2:

                    st.metric(
                        "Risk Level",
                        result["risk_level"]
                    )

                with threat_col3:

                    st.metric(
                        "Threat Type",
                        result["threat_type"]
                    )


                # ------------------------------------------------
                # BEHAVIORAL ANALYSIS
                # ------------------------------------------------

                st.subheader(
                    "🧠 Behavioral Analysis"
                )

                behavior = result["behavior"]

                behavior_col1, behavior_col2, behavior_col3 = st.columns(
                    3
                )

                with behavior_col1:

                    st.write(
                        "**Signing Frequency**"
                    )

                    st.write(
                        behavior["signing_frequency"]
                    )

                    st.write(
                        "**Signature Count**"
                    )

                    st.write(
                        behavior["signature_count"]
                    )

                with behavior_col2:

                    st.write(
                        "**Device Change**"
                    )

                    st.write(
                        behavior["device_change"]
                    )

                    st.write(
                        "**Location Change**"
                    )

                    st.write(
                        behavior["location_change"]
                    )

                with behavior_col3:

                    st.write(
                        "**Failed Attempts**"
                    )

                    st.write(
                        behavior["failed_attempts"]
                    )

                    st.write(
                        "**Activity Hour**"
                    )

                    st.write(
                        behavior["activity_hour"]
                    )


                # ------------------------------------------------
                # TELEMETRY
                # ------------------------------------------------

                st.subheader(
                    "🌐 Security Telemetry"
                )

                telemetry_col1, telemetry_col2, telemetry_col3 = st.columns(
                    3
                )

                with telemetry_col1:

                    st.write(
                        "**Device ID**"
                    )

                    st.code(
                        result["device_id"]
                    )

                with telemetry_col2:

                    st.write(
                        "**IP Address**"
                    )

                    st.code(
                        result["ip_address"]
                    )

                with telemetry_col3:

                    st.write(
                        "**Approximate Location**"
                    )

                    st.write(
                        result["location"]
                    )


                # ------------------------------------------------
                # VALID SIGNATURE MISUSE ALERT
                # ------------------------------------------------

                if (
                    result["threat_type"]
                    == "VALID_SIGNATURE_MISUSE"
                ):

                    st.warning(
                        """
                        ⚠️ VALID SIGNATURE MISUSE DETECTED

                        The digital signature is cryptographically
                        valid, but the observed signing behavior has
                        been classified as anomalous.

                        This is the key behavioral-threat scenario
                        targeted by Q-SHIELD.
                        """
                    )


            except Exception as error:

                st.error(
                    "❌ Document analysis failed."
                )

                st.exception(
                    error
                )


st.divider()


# ============================================================
# EXTERNAL SIGNATURE VERIFICATION
# ============================================================

st.header(
    "🔏 Verify Existing Digital Signature"
)

st.markdown(
    """
    Upload an existing document, public key, and digital signature
    to verify whether the signature is valid and analyze the
    associated signing behavior.
    """
)


verification_document = st.file_uploader(
    "Upload Document",
    type=["pdf", "txt", "doc", "docx"],
    key="verification_document"
)

public_key_file = st.file_uploader(
    "Upload Public Key (.pem)",
    type=["pem"],
    key="public_key_file"
)

signature_file = st.file_uploader(
    "Upload Digital Signature (.sig)",
    type=["sig", "bin"],
    key="signature_file"
)


if (
    verification_document
    and public_key_file
    and signature_file
):

    if st.button(
        "🔍 Verify & Analyze Signature",
        key="verify_external_signature"
    ):

        with st.spinner(
            "Verifying signature and running threat analysis..."
        ):

            try:

                # -----------------------------------------------
                # READ FILES
                # -----------------------------------------------

                document_bytes = (
                    verification_document.read()
                )

                public_key_bytes = (
                    public_key_file.read()
                )

                signature_bytes = (
                    signature_file.read()
                )


                # -----------------------------------------------
                # LOAD PUBLIC KEY
                # -----------------------------------------------

                public_key = load_public_key(
                    public_key_bytes
                )


                # -----------------------------------------------
                # RUN EXTERNAL SIGNATURE PIPELINE
                # -----------------------------------------------

                result = pipeline.analyze_external_signature(
                    document=document_bytes,
                    signature=signature_bytes,
                    public_key=public_key
                )


                # -----------------------------------------------
                # SAVE EVENT
                # -----------------------------------------------

                insert_event(
                    user_id=result["user_id"],
                    document_id=verification_document.name,
                    timestamp=result["timestamp"],
                    device_id=result["device_id"],
                    ip_address=result["ip_address"],
                    location=result["location"],
                    signature_valid=result["signature_valid"],
                    signing_frequency=result["behavior"][
                        "signing_frequency"
                    ],
                    device_change=result["behavior"][
                        "device_change"
                    ],
                    location_change=result["behavior"][
                        "location_change"
                    ],
                    activity_hour=result["behavior"][
                        "activity_hour"
                    ],
                    failed_attempts=result["behavior"][
                        "failed_attempts"
                    ],
                    signature_count=result["behavior"][
                        "signature_count"
                    ],
                    anomaly_score=result["anomaly_score"],
                    quantum_score=result["quantum_score"],
                    threat_score=result["threat_score"],
                    risk_level=result["risk_level"],
                    threat_type=result["threat_type"]
                )


                # -----------------------------------------------
                # SUCCESS
                # -----------------------------------------------

                st.success(
                    "✅ Signature verification and threat analysis completed."
                )


                # -----------------------------------------------
                # GENERATE PDF SECURITY REPORT
                # -----------------------------------------------

                try:

                    report_path = generate_security_report(
                        result,
                        verification_document.name
                    )

                    st.subheader(
                        "📄 Security Report"
                    )

                    st.success(
                        "✅ PDF security report generated."
                    )

                    report_bytes = report_path.read_bytes()

                    st.download_button(
                        label="⬇️ Download PDF Security Report",
                        data=report_bytes,
                        file_name=report_path.name,
                        mime="application/pdf",
                        key="download_external_report"
                    )

                except Exception as error:

                    st.error(
                        "❌ Could not generate security report."
                    )

                    st.exception(error)


                # -----------------------------------------------
                # SIGNATURE VERIFICATION
                # -----------------------------------------------

                st.subheader(
                    "🔐 Signature Verification"
                )

                if result["signature_valid"]:

                    st.success(
                        "🟢 VALID DIGITAL SIGNATURE"
                    )

                else:

                    st.error(
                        "🔴 INVALID DIGITAL SIGNATURE"
                    )


                # -----------------------------------------------
                # HASH
                # -----------------------------------------------

                st.write(
                    "Document SHA-256 Hash:"
                )

                st.code(
                    result["document_hash"]
                )


                # -----------------------------------------------
                # ML
                # -----------------------------------------------

                st.subheader(
                    "🤖 ML Anomaly Detection"
                )

                ml_col1, ml_col2 = st.columns(2)

                with ml_col1:

                    st.metric(
                        "Anomaly Score",
                        round(
                            result["anomaly_score"],
                            4
                        )
                    )

                with ml_col2:

                    st.metric(
                        "Classification",
                        result["ml_classification"]
                    )


                # -----------------------------------------------
                # QUANTUM
                # -----------------------------------------------

                st.subheader(
                    "⚛️ Quantum-Inspired Analysis"
                )

                quantum_col1, quantum_col2 = st.columns(2)

                with quantum_col1:

                    st.metric(
                        "Quantum-Inspired Score",
                        round(
                            result["quantum_score"],
                            4
                        )
                    )

                with quantum_col2:

                    st.write(
                        "Optimized Feature Weights"
                    )

                    st.write(
                        result["quantum_weights"]
                    )


                # -----------------------------------------------
                # THREAT
                # -----------------------------------------------

                st.subheader(
                    "🚨 Threat Assessment"
                )

                threat_col1, threat_col2, threat_col3 = st.columns(
                    3
                )

                with threat_col1:

                    st.metric(
                        "Threat Score",
                        result["threat_score"]
                    )

                with threat_col2:

                    st.metric(
                        "Risk Level",
                        result["risk_level"]
                    )

                with threat_col3:

                    st.metric(
                        "Threat Type",
                        result["threat_type"]
                    )


                # -----------------------------------------------
                # BEHAVIOR
                # -----------------------------------------------

                st.subheader(
                    "🧠 Behavioral Analysis"
                )

                behavior = result["behavior"]

                behavior_col1, behavior_col2, behavior_col3 = st.columns(
                    3
                )

                with behavior_col1:

                    st.write(
                        "**Signing Frequency**"
                    )

                    st.write(
                        behavior["signing_frequency"]
                    )

                    st.write(
                        "**Signature Count**"
                    )

                    st.write(
                        behavior["signature_count"]
                    )

                with behavior_col2:

                    st.write(
                        "**Device Change**"
                    )

                    st.write(
                        behavior["device_change"]
                    )

                    st.write(
                        "**Location Change**"
                    )

                    st.write(
                        behavior["location_change"]
                    )

                with behavior_col3:

                    st.write(
                        "**Failed Attempts**"
                    )

                    st.write(
                        behavior["failed_attempts"]
                    )

                    st.write(
                        "**Activity Hour**"
                    )

                    st.write(
                        behavior["activity_hour"]
                    )


                # -----------------------------------------------
                # TELEMETRY
                # -----------------------------------------------

                st.subheader(
                    "🌐 Security Telemetry"
                )

                telemetry_col1, telemetry_col2, telemetry_col3 = st.columns(
                    3
                )

                with telemetry_col1:

                    st.write(
                        "**Device ID**"
                    )

                    st.code(
                        result["device_id"]
                    )

                with telemetry_col2:

                    st.write(
                        "**IP Address**"
                    )

                    st.code(
                        result["ip_address"]
                    )

                with telemetry_col3:

                    st.write(
                        "**Approximate Location**"
                    )

                    st.write(
                        result["location"]
                    )


                # -----------------------------------------------
                # VALID SIGNATURE MISUSE
                # -----------------------------------------------

                if (
                    result["threat_type"]
                    == "VALID_SIGNATURE_MISUSE"
                ):

                    st.warning(
                        """
                        ⚠️ VALID SIGNATURE MISUSE DETECTED

                        The signature is cryptographically valid,
                        but the observed signing behavior is
                        anomalous.
                        """
                    )


            except Exception as error:

                st.error(
                    "❌ External signature analysis failed."
                )

                st.exception(
                    error
                )


st.divider()


# ============================================================
# SECURITY EVENT HISTORY
# ============================================================

st.header(
    "📋 Security Event History"
)

events = get_events()


if events:

    for event in events:

        (
            event_id,
            user_id,
            document_id,
            timestamp,
            device_id,
            ip_address,
            location,
            signature_valid,
            anomaly_score,
            quantum_score,
            threat_score,
            risk_level,
            threat_type
        ) = event


        # ----------------------------------------------------
        # EVENT ICON
        # ----------------------------------------------------

        if risk_level == "CRITICAL":

            icon = "🔴"

        elif risk_level == "HIGH":

            icon = "🟠"

        elif risk_level == "MEDIUM":

            icon = "🟡"

        else:

            icon = "🟢"


        # ----------------------------------------------------
        # EVENT DETAILS
        # ----------------------------------------------------

        with st.expander(
            f"{icon} Event #{event_id} | "
            f"{risk_level} | "
            f"Score: {threat_score} | "
            f"{threat_type}"
        ):

            history_col1, history_col2 = st.columns(
                2
            )

            with history_col1:

                st.write(
                    f"**User ID:** {user_id}"
                )

                st.write(
                    f"**Document:** {document_id}"
                )

                st.write(
                    f"**Timestamp:** {timestamp}"
                )

                st.write(
                    f"**Device ID:** {device_id}"
                )

                st.write(
                    f"**IP Address:** {ip_address}"
                )

            with history_col2:

                st.write(
                    f"**Location:** {location}"
                )

                st.write(
                    f"**Signature Valid:** "
                    f"{'YES' if signature_valid else 'NO'}"
                )

                st.write(
                    f"**Anomaly Score:** "
                    f"{round(anomaly_score, 4)}"
                )

                st.write(
                    f"**Quantum Score:** "
                    f"{round(quantum_score, 4)}"
                )

                st.write(
                    f"**Threat Score:** "
                    f"{threat_score}"
                )

                st.write(
                    f"**Risk Level:** "
                    f"{risk_level}"
                )

                st.write(
                    f"**Threat Type:** "
                    f"{threat_type}"
                )


else:

    st.info(
        "No security events recorded yet."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Q-SHIELD | Quantum-Inspired Cyber Threat Detection "
    "for Digital Signatures"
)

st.caption(
    "Prototype implementation for cybersecurity threat monitoring."
)