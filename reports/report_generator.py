from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


REPORTS_DIR = Path(__file__).parent


def generate_security_report(result, document_name):
    """
    Generate a Q-SHIELD security report in PDF format.

    Returns:
        Path to the generated PDF report.
    """

    behavior = result.get("behavior", {})

    report_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    safe_name = Path(document_name).stem

    report_filename = (
        f"{safe_name}_QSHIELD_REPORT_{timestamp}.pdf"
    )

    report_path = REPORTS_DIR / report_filename


    # ========================================================
    # PDF DOCUMENT
    # ========================================================

    document = SimpleDocTemplate(
        str(report_path),
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )


    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    normal_style = styles["BodyText"]


    story = []


    # ========================================================
    # TITLE
    # ========================================================

    story.append(
        Paragraph(
            "Q-SHIELD SECURITY REPORT",
            title_style
        )
    )

    story.append(
        Spacer(1, 10)
    )

    story.append(
        Paragraph(
            "Quantum-Inspired Cyber Threat Detection "
            "for Digital Signatures",
            normal_style
        )
    )

    story.append(
        Spacer(1, 20)
    )


    # ========================================================
    # REPORT INFORMATION
    # ========================================================

    story.append(
        Paragraph(
            "Report Information",
            heading_style
        )
    )

    report_information = [
        ["Report Generated", report_time],
        [
            "User ID",
            result.get("user_id", "UNKNOWN")
        ],
        [
            "Document",
            document_name
        ],
        [
            "Analysis Time",
            result.get("timestamp", "UNKNOWN")
        ]
    ]

    report_table = Table(
        report_information,
        colWidths=[150, 350]
    )

    report_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(
        report_table
    )

    story.append(
        Spacer(1, 20)
    )


    # ========================================================
    # DIGITAL SIGNATURE
    # ========================================================

    story.append(
        Paragraph(
            "Digital Signature Verification",
            heading_style
        )
    )

    signature_status = (
        "VALID DIGITAL SIGNATURE"
        if result.get("signature_valid", False)
        else "INVALID DIGITAL SIGNATURE"
    )

    signature_information = [
        [
            "SHA-256 Hash",
            result.get(
                "document_hash",
                "UNKNOWN"
            )
        ],
        [
            "Signature Status",
            signature_status
        ]
    ]

    signature_table = Table(
        signature_information,
        colWidths=[150, 350]
    )

    signature_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(
        signature_table
    )

    story.append(
        Spacer(1, 20)
    )


    # ========================================================
    # ML ANALYSIS
    # ========================================================

    story.append(
        Paragraph(
            "ML Anomaly Detection",
            heading_style
        )
    )

    ml_information = [
        [
            "Anomaly Score",
            str(
                round(
                    result.get(
                        "anomaly_score",
                        0
                    ),
                    4
                )
            )
        ],
        [
            "Classification",
            result.get(
                "ml_classification",
                "UNKNOWN"
            )
        ]
    ]

    ml_table = Table(
        ml_information,
        colWidths=[150, 350]
    )

    ml_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(
        ml_table
    )

    story.append(
        Spacer(1, 20)
    )


    # ========================================================
    # QUANTUM-INSPIRED ANALYSIS
    # ========================================================

    story.append(
        Paragraph(
            "Quantum-Inspired Analysis",
            heading_style
        )
    )

    quantum_information = [
        [
            "Quantum-Inspired Score",
            str(
                round(
                    result.get(
                        "quantum_score",
                        0
                    ),
                    4
                )
            )
        ],
        [
            "Optimized Feature Weights",
            str(
                result.get(
                    "quantum_weights",
                    []
                )
            )
        ]
    ]

    quantum_table = Table(
        quantum_information,
        colWidths=[150, 350]
    )

    quantum_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(
        quantum_table
    )

    story.append(
        Spacer(1, 20)
    )


    # ========================================================
    # THREAT ASSESSMENT
    # ========================================================

    story.append(
        Paragraph(
            "Threat Assessment",
            heading_style
        )
    )

    threat_information = [
        [
            "Threat Score",
            f"{result.get('threat_score', 0)} / 100"
        ],
        [
            "Risk Level",
            result.get(
                "risk_level",
                "UNKNOWN"
            )
        ],
        [
            "Threat Type",
            result.get(
                "threat_type",
                "NONE"
            )
        ]
    ]

    threat_table = Table(
        threat_information,
        colWidths=[150, 350]
    )

    threat_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(
        threat_table
    )

    story.append(
        Spacer(1, 20)
    )


    # ========================================================
    # BEHAVIORAL ANALYSIS
    # ========================================================

    story.append(
        Paragraph(
            "Behavioral Analysis",
            heading_style
        )
    )

    behavior_information = [
        [
            "Signing Frequency",
            str(
                behavior.get(
                    "signing_frequency",
                    0
                )
            )
        ],
        [
            "Device Change",
            str(
                behavior.get(
                    "device_change",
                    0
                )
            )
        ],
        [
            "Location Change",
            str(
                behavior.get(
                    "location_change",
                    0
                )
            )
        ],
        [
            "Activity Hour",
            str(
                behavior.get(
                    "activity_hour",
                    0
                )
            )
        ],
        [
            "Failed Attempts",
            str(
                behavior.get(
                    "failed_attempts",
                    0
                )
            )
        ],
        [
            "Signature Count",
            str(
                behavior.get(
                    "signature_count",
                    0
                )
            )
        ]
    ]

    behavior_table = Table(
        behavior_information,
        colWidths=[150, 350]
    )

    behavior_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(
        behavior_table
    )

    story.append(
        Spacer(1, 20)
    )


    # ========================================================
    # SECURITY TELEMETRY
    # ========================================================

    story.append(
        Paragraph(
            "Security Telemetry",
            heading_style
        )
    )

    telemetry_information = [
        [
            "Device ID",
            result.get(
                "device_id",
                "UNKNOWN"
            )
        ],
        [
            "IP Address",
            result.get(
                "ip_address",
                "UNKNOWN"
            )
        ],
        [
            "Approximate Location",
            result.get(
                "location",
                "UNKNOWN"
            )
        ]
    ]

    telemetry_table = Table(
        telemetry_information,
        colWidths=[150, 350]
    )

    telemetry_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
            ("PADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(
        telemetry_table
    )

    story.append(
        Spacer(1, 20)
    )


    # ========================================================
    # Q-SHIELD SUMMARY
    # ========================================================

    story.append(
        Paragraph(
            "Q-SHIELD Analysis Summary",
            heading_style
        )
    )

    summary_text = """
    Q-SHIELD combines digital signature verification,
    behavioral feature analysis, ML-based anomaly detection,
    quantum-inspired optimization, threat score calculation,
    and risk classification to analyze digital-signing activity.
    """

    story.append(
        Paragraph(
            summary_text,
            normal_style
        )
    )


    # ========================================================
    # BUILD PDF
    # ========================================================

    document.build(
        story
    )

    return report_path