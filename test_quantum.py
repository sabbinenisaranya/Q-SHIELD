from quantum.optimizer import QuantumInspiredOptimizer


print("\n========================================")
print("   Q-SHIELD QUANTUM-INSPIRED TEST")
print("========================================")


# Six behavioral features
features = [
    1.0,   # Signing frequency
    1.0,   # Device change
    1.0,   # Location change
    1.0,   # Time anomaly
    1.0,   # Failed attempts
    1.0    # Signature count
]


optimizer = QuantumInspiredOptimizer()


weights, score = optimizer.optimize_weights(
    features
)


print("\nOptimized Feature Weights:")

feature_names = [
    "Signing Frequency",
    "Device Change",
    "Location Change",
    "Time Anomaly",
    "Failed Attempts",
    "Signature Count"
]


for name, weight in zip(
    feature_names,
    weights
):

    print(
        f"{name}: {weight:.3f}"
    )


print("\nQuantum-Inspired Score:")

print(
    round(score, 3)
)


print("\n========================================")
print("              TEST COMPLETE")
print("========================================")