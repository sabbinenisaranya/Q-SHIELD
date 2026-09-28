import numpy as np


class AnomalyDetector:

    def __init__(self):
        """
        Lightweight anomaly detector.

        This implementation uses NumPy only.
        It does not depend on scikit-learn or SciPy.
        """

        self.normal_data = None
        self.normal_mean = None
        self.normal_std = None

    def train(self, normal_data):
        """
        Learn the normal behavioral pattern.

        normal_data:
            List of normal feature vectors.
        """

        self.normal_data = np.array(
            normal_data,
            dtype=float
        )

        self.normal_mean = np.mean(
            self.normal_data,
            axis=0
        )

        self.normal_std = np.std(
            self.normal_data,
            axis=0
        )

        # Prevent division by zero for features
        # that do not vary in the normal dataset.
        self.normal_std = np.where(
            self.normal_std < 0.01,
            0.01,
            self.normal_std
        )

    def predict_anomaly_score(self, features):
        """
        Calculate an anomaly score between 0 and 1.

        0   = very similar to normal behavior
        1   = highly unusual behavior

        Returns:
            anomaly_score
            prediction
        """

        if self.normal_mean is None:
            raise RuntimeError(
                "Anomaly detector has not been trained."
            )

        data = np.array(
            features,
            dtype=float
        )

        # Calculate standardized distance
        # from the learned normal behavior.
        z_scores = np.abs(
            (
                data - self.normal_mean
            )
            / self.normal_std
        )

        # Average deviation across features.
        distance = float(
            np.mean(z_scores)
        )

        # Convert distance into a 0-1 anomaly score.
        anomaly_score = (
            1.0
            - np.exp(-distance / 2.0)
        )

        anomaly_score = float(
            np.clip(
                anomaly_score,
                0.0,
                1.0
            )
        )

        # Classification threshold.
        if anomaly_score >= 0.5:
            prediction = -1
        else:
            prediction = 1

        return (
            anomaly_score,
            prediction
        )