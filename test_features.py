from features.extractor import extract_features


print("\n========================================")
print("       Q-SHIELD FEATURE TEST")
print("========================================")


features = extract_features(
    signing_frequency=25,
    device_change=True,
    location_change=True,
    activity_hour=3,
    failed_attempts=5,
    signature_count=25
)


print("\nExtracted Behavioral Features:")

for name, value in features.items():

    print(f"{name}: {value:.2f}")


print("\n========================================")
print("              TEST COMPLETE")
print("========================================")