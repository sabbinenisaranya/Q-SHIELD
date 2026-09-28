import numpy as np


class QuantumInspiredOptimizer:

    def __init__(self, seed=42):

        self.rng = np.random.default_rng(seed)


    def optimize_weights(self, features):

        features = np.array(features, dtype=float)

        # Initial equal weights
        weights = np.ones(len(features)) / len(features)

        # Quantum-inspired probability amplitudes
        amplitudes = np.sqrt(weights)

        best_weights = weights.copy()

        best_score = self._objective(
            features,
            best_weights
        )


        # Search through different weight combinations
        for _ in range(100):

            # Small quantum-inspired perturbation
            perturbation = self.rng.normal(
                0,
                0.15,
                len(features)
            )

            candidate_amplitudes = (
                amplitudes + perturbation
            )

            # Convert amplitudes into probabilities
            candidate_weights = (
                candidate_amplitudes ** 2
            )

            # Normalize weights
            total = candidate_weights.sum()

            if total == 0:
                continue

            candidate_weights = (
                candidate_weights / total
            )


            candidate_score = self._objective(
                features,
                candidate_weights
            )


            # Keep the better solution
            if candidate_score > best_score:

                best_score = candidate_score

                best_weights = (
                    candidate_weights.copy()
                )

                amplitudes = np.sqrt(
                    best_weights
                )


        return best_weights, best_score


    def _objective(self, features, weights):

        # Weighted threat contribution
        score = np.sum(
            features * weights
        )

        return float(score)