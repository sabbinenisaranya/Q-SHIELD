import hashlib
from datetime import datetime, timedelta

from crypto.key_manager import generate_key_pair
from crypto.signer import sign_document
from crypto.verifier import verify_signature

from features.extractor import extract_features
from ml.detector import AnomalyDetector
from quantum.optimizer import QuantumInspiredOptimizer
from threat.scorer import calculate_threat_score

from database.database import get_connection

from telemetry import get_network_telemetry
from device import get_device_id


class QShieldPipeline:

    def __init__(self):

        # ========================================================
        # USER / DEVICE INFORMATION
        # ========================================================

        self.user_id = "USER-001"

        self.device_id = get_device_id()

        telemetry = get_network_telemetry()

        self.ip_address = telemetry["ip_address"]
        self.location = telemetry["location"]


        # ========================================================
        # CRYPTOGRAPHIC KEYS
        # ========================================================

        self.private_key, self.public_key = (
            generate_key_pair()
        )


        # ========================================================
        # ML ANOMALY DETECTOR
        # ========================================================

        self.anomaly_detector = AnomalyDetector()

        self.train_anomaly_detector()


        # ========================================================
        # QUANTUM-INSPIRED OPTIMIZER
        # ========================================================

        self.quantum_optimizer = (
            QuantumInspiredOptimizer()
        )


    # ============================================================
    # TRAIN ANOMALY DETECTOR
    # ============================================================

    def train_anomaly_detector(self):

        """
        Train the anomaly detector using representative
        normal signing behavior.

        Feature order:

        1. Signing frequency
        2. Device change
        3. Location change
        4. Time anomaly
        5. Failed attempts
        6. Signature count
        """

        normal_data = [

            [0.05, 0, 0, 0, 0.00, 0.05],

            [0.10, 0, 0, 0, 0.00, 0.10],

            [0.15, 0, 0, 0, 0.00, 0.15],

            [0.20, 0, 0, 0, 0.00, 0.20],

            [0.25, 0, 0, 0, 0.00, 0.25],

            [0.30, 0, 0, 0, 0.00, 0.30],

            [0.20, 0, 0, 0, 0.05, 0.20],

            [0.25, 0, 0, 0, 0.05, 0.25],

            [0.30, 0, 0, 0, 0.05, 0.30],

        ]

        self.anomaly_detector.train(
            normal_data
        )


    # ============================================================
    # GET SIGNING HISTORY
    # ============================================================

    def get_signing_history(self):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                timestamp,
                device_id,
                ip_address,
                location,
                signature_valid,
                failed_attempts,
                signature_count
            FROM signature_events
            WHERE user_id = ?
            ORDER BY id ASC
            """,
            (self.user_id,)
        )

        history = cursor.fetchall()

        connection.close()

        return history


    # ============================================================
    # CALCULATE CURRENT BEHAVIOR
    # ============================================================

    def calculate_behavior(
        self,
        timestamp
    ):

        history = self.get_signing_history()


        # --------------------------------------------------------
        # SIGNATURE COUNT
        # --------------------------------------------------------

        signature_count = (
            len(history) + 1
        )


        # --------------------------------------------------------
        # FAILED ATTEMPTS
        # --------------------------------------------------------

        failed_attempts = 0

        for event in history:

            signature_valid = event[4]

            if not signature_valid:

                failed_attempts += 1


        # --------------------------------------------------------
        # DEVICE CHANGE
        # --------------------------------------------------------

        device_change = 0

        if history:

            last_device = history[-1][1]

            if (
                last_device
                and last_device != self.device_id
            ):

                device_change = 1


        # --------------------------------------------------------
        # LOCATION CHANGE
        # --------------------------------------------------------

        location_change = 0

        if history:

            last_location = history[-1][3]

            if (
                last_location
                and last_location != self.location
                and self.location != "UNKNOWN"
            ):

                location_change = 1


        # --------------------------------------------------------
        # SIGNING FREQUENCY
        # --------------------------------------------------------

        recent_count = 0

        one_hour_ago = (
            timestamp - timedelta(hours=1)
        )

        for event in history:

            event_timestamp = event[0]

            try:

                event_time = datetime.fromisoformat(
                    event_timestamp
                )

                if event_time >= one_hour_ago:

                    recent_count += 1

            except Exception:

                continue


        # Include the current event

        recent_count += 1

        signing_frequency = recent_count


        # --------------------------------------------------------
        # ACTIVITY HOUR
        # --------------------------------------------------------

        activity_hour = timestamp.hour


        return {
            "signing_frequency": signing_frequency,
            "device_change": device_change,
            "location_change": location_change,
            "activity_hour": activity_hour,
            "failed_attempts": failed_attempts,
            "signature_count": signature_count
        }


    # ============================================================
    # DETERMINE THREAT TYPE
    # ============================================================

    def determine_threat_type(
        self,
        signature_valid,
        ml_classification,
        behavior
    ):

        # --------------------------------------------------------
        # INVALID DIGITAL SIGNATURE
        # --------------------------------------------------------

        if not signature_valid:

            return "INVALID_DIGITAL_SIGNATURE"


        # --------------------------------------------------------
        # DEVICE CHANGE
        # --------------------------------------------------------

        if behavior["device_change"] == 1:

            return "DEVICE_CHANGE"


        # --------------------------------------------------------
        # LOCATION CHANGE
        # --------------------------------------------------------

        if behavior["location_change"] == 1:

            return "LOCATION_CHANGE"


        # --------------------------------------------------------
        # FAILED SIGNING ATTEMPTS
        # --------------------------------------------------------

        if behavior["failed_attempts"] > 0:

            return "FAILED_SIGNING_ATTEMPTS"


        # --------------------------------------------------------
        # ABNORMAL SIGNING FREQUENCY
        # --------------------------------------------------------

        if behavior["signing_frequency"] > 10:

            return "ABNORMAL_SIGNING_FREQUENCY"


        # --------------------------------------------------------
        # VALID SIGNATURE + ANOMALOUS BEHAVIOR
        # --------------------------------------------------------

        if (
            signature_valid
            and ml_classification == "ANOMALY"
        ):

            return "VALID_SIGNATURE_MISUSE"


        # --------------------------------------------------------
        # NO THREAT
        # --------------------------------------------------------

        return "NONE"


    # ============================================================
    # ANALYZE DOCUMENT
    # ============================================================

    def analyze(
        self,
        document
    ):

        # --------------------------------------------------------
        # CURRENT TIMESTAMP
        # --------------------------------------------------------

        timestamp = datetime.now()


        # --------------------------------------------------------
        # DIGITAL SIGNATURE
        # --------------------------------------------------------

        document_hash, signature = sign_document(
            document,
            self.private_key
        )


        # --------------------------------------------------------
        # VERIFY GENERATED SIGNATURE
        # --------------------------------------------------------

        signature_valid = verify_signature(
            document,
            signature,
            self.public_key
        )


        # --------------------------------------------------------
        # BEHAVIOR
        # --------------------------------------------------------

        behavior = self.calculate_behavior(
            timestamp
        )


        # --------------------------------------------------------
        # FEATURE EXTRACTION
        # --------------------------------------------------------

        features = extract_features(
            signing_frequency=behavior[
                "signing_frequency"
            ],
            device_change=behavior[
                "device_change"
            ],
            location_change=behavior[
                "location_change"
            ],
            activity_hour=behavior[
                "activity_hour"
            ],
            failed_attempts=behavior[
                "failed_attempts"
            ],
            signature_count=behavior[
                "signature_count"
            ]
        )


        # --------------------------------------------------------
        # CONVERT FEATURES TO MODEL INPUT
        # --------------------------------------------------------

        feature_vector = [

            features["signing_frequency"],

            features["device_change"],

            features["location_change"],

            features["time_anomaly"],

            features["failed_attempts"],

            features["signature_count"]

        ]


        # --------------------------------------------------------
        # ML ANOMALY DETECTION
        # --------------------------------------------------------

        (
            anomaly_score,
            prediction
        ) = self.anomaly_detector.predict_anomaly_score(
            feature_vector
        )


        if prediction == -1:

            ml_classification = "ANOMALY"

        else:

            ml_classification = "NORMAL"


        # --------------------------------------------------------
        # QUANTUM-INSPIRED OPTIMIZATION
        # --------------------------------------------------------

        (
            quantum_weights,
            quantum_score
        ) = self.quantum_optimizer.optimize_weights(
            feature_vector
        )


        # --------------------------------------------------------
        # THREAT TYPE
        # --------------------------------------------------------

        threat_type = self.determine_threat_type(

            signature_valid=signature_valid,

            ml_classification=ml_classification,

            behavior=behavior

        )


        # --------------------------------------------------------
        # FINAL THREAT SCORE
        # --------------------------------------------------------

        (
            threat_score,
            risk_level
        ) = calculate_threat_score(

            signature_valid=signature_valid,

            anomaly_score=anomaly_score,

            quantum_score=quantum_score,

            features=features

        )


        # --------------------------------------------------------
        # RETURN COMPLETE RESULT
        # --------------------------------------------------------

        return {

            "document_hash": document_hash,

            "signature": signature,

            "signature_valid": signature_valid,

            "user_id": self.user_id,

            "timestamp": timestamp.isoformat(
                timespec="seconds"
            ),

            "device_id": self.device_id,

            "ip_address": self.ip_address,

            "location": self.location,

            "behavior": behavior,

            "features": features,

            "anomaly_score": anomaly_score,

            "ml_classification": ml_classification,

            "quantum_weights": quantum_weights.tolist(),

            "quantum_score": quantum_score,

            "threat_score": threat_score,

            "risk_level": risk_level,

            "threat_type": threat_type

        }


    # ============================================================
    # ANALYZE EXTERNAL SIGNATURE
    # ============================================================

    def analyze_external_signature(
        self,
        document,
        signature,
        public_key
    ):

        # --------------------------------------------------------
        # CURRENT TIMESTAMP
        # --------------------------------------------------------

        timestamp = datetime.now()


        # --------------------------------------------------------
        # DOCUMENT HASH
        # --------------------------------------------------------

        document_hash = hashlib.sha256(
            document
        ).hexdigest()


        # --------------------------------------------------------
        # VERIFY EXTERNAL SIGNATURE
        # --------------------------------------------------------

        signature_valid = verify_signature(
            document,
            signature,
            public_key
        )


        # --------------------------------------------------------
        # BEHAVIOR
        # --------------------------------------------------------

        behavior = self.calculate_behavior(
            timestamp
        )


        # --------------------------------------------------------
        # FEATURE EXTRACTION
        # --------------------------------------------------------

        features = extract_features(
            signing_frequency=behavior[
                "signing_frequency"
            ],
            device_change=behavior[
                "device_change"
            ],
            location_change=behavior[
                "location_change"
            ],
            activity_hour=behavior[
                "activity_hour"
            ],
            failed_attempts=behavior[
                "failed_attempts"
            ],
            signature_count=behavior[
                "signature_count"
            ]
        )


        # --------------------------------------------------------
        # FEATURE VECTOR
        # --------------------------------------------------------

        feature_vector = [

            features["signing_frequency"],

            features["device_change"],

            features["location_change"],

            features["time_anomaly"],

            features["failed_attempts"],

            features["signature_count"]

        ]


        # --------------------------------------------------------
        # ML ANOMALY DETECTION
        # --------------------------------------------------------

        (
            anomaly_score,
            prediction
        ) = self.anomaly_detector.predict_anomaly_score(
            feature_vector
        )


        if prediction == -1:

            ml_classification = "ANOMALY"

        else:

            ml_classification = "NORMAL"


        # --------------------------------------------------------
        # QUANTUM-INSPIRED OPTIMIZATION
        # --------------------------------------------------------

        (
            quantum_weights,
            quantum_score
        ) = self.quantum_optimizer.optimize_weights(
            feature_vector
        )


        # --------------------------------------------------------
        # THREAT TYPE
        # --------------------------------------------------------

        threat_type = self.determine_threat_type(

            signature_valid=signature_valid,

            ml_classification=ml_classification,

            behavior=behavior

        )


        # --------------------------------------------------------
        # THREAT SCORE
        # --------------------------------------------------------

        (
            threat_score,
            risk_level
        ) = calculate_threat_score(

            signature_valid=signature_valid,

            anomaly_score=anomaly_score,

            quantum_score=quantum_score,

            features=features

        )


        # --------------------------------------------------------
        # RETURN RESULT
        # --------------------------------------------------------

        return {

            "document_hash": document_hash,

            "signature": signature,

            "signature_valid": signature_valid,

            "user_id": self.user_id,

            "timestamp": timestamp.isoformat(
                timespec="seconds"
            ),

            "device_id": self.device_id,

            "ip_address": self.ip_address,

            "location": self.location,

            "behavior": behavior,

            "features": features,

            "anomaly_score": anomaly_score,

            "ml_classification": ml_classification,

            "quantum_weights": quantum_weights.tolist(),

            "quantum_score": quantum_score,

            "threat_score": threat_score,

            "risk_level": risk_level,

            "threat_type": threat_type

        }