from ml.detector import AnomalyDetector


print("\n========================================")
print("       Q-SHIELD ML ANOMALY TEST")
print("========================================")


# Normal historical signing behavior
normal_data = [

    [0.10, 0, 0, 0, 0, 0.10],
    [0.15, 0, 0, 0, 0, 0.15],
    [0.20, 0, 0, 0, 0, 0.20],
    [0.10, 0, 0, 0, 0, 0.05],
    [0.25, 0, 0, 0, 0, 0.20],
    [0.15, 0, 0, 0, 0, 0.10],
    [0.20, 0, 0, 0, 0, 0.15],
    [0.10, 0, 0, 0, 0, 0.10],
    [0.30, 0, 0, 0, 0, 0.25],
    [0.15, 0, 0, 0, 0, 0.15]

]


# Create detector
detector = AnomalyDetector()


# Train detector
detector.train(normal_data)


print("\nModel trained successfully.")


# Suspicious behavior
suspicious_event = [
    1.0,
    1.0,
    1.0,
    1.0,
    1.0,
    1.0
]


# Detect anomaly
score, prediction = detector.predict_anomaly_score(
    suspicious_event
)


print("\nSuspicious Event:")
print("Anomaly Score:", round(score, 3))


if prediction == -1:

    print("Classification: ANOMALY")

else:

    print("Classification: NORMAL")


print("\n========================================")
print("              TEST COMPLETE")
print("========================================")