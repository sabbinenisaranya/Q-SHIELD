from dashboard.analytics import get_dashboard_data


print("\nQ-SHIELD DASHBOARD TEST")
print("=" * 40)

data = get_dashboard_data()

print(
    "Total Events:",
    data["total_events"]
)

print(
    "High Risk Events:",
    data["high_risk_events"]
)

print(
    "Critical Events:",
    data["critical_events"]
)

print(
    "Average Threat Score:",
    data["average_threat_score"]
)

print("\nRisk Distribution:")

for risk, count in data["risk_distribution"].items():
    print(f"  {risk}: {count}")

print("\nThreat Distribution:")

for threat, count in data["threat_distribution"].items():
    print(f"  {threat}: {count}")

print("\nThreat Score Timeline:")

for event in data["score_timeline"]:
    print(
        f"  {event['timestamp']} -> "
        f"{event['threat_score']}"
    )

print("\nTEST COMPLETE")