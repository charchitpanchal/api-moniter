import logging
import numpy as np
from sklearn.ensemble import IsolationForest
from app.models.api_check import ApiCheck

logger = logging.getLogger("ml.anomaly_detector")

MIN_CHECKS_REQUIRED = 10  # need enough data for the model to learn "normal"


def detect_anomalies(checks: list[ApiCheck]) -> list[tuple[ApiCheck, bool]]:
    """
    Runs Isolation Forest on response_time values from a list of checks.
    Returns pairs of (check, is_anomaly). Trains fresh each call — the
    dataset is small (recent checks for one API), so this is fast and
    needs no persistent model storage.

    Returns an empty result gracefully if there's not enough data yet,
    or if response_time values are missing (e.g., all timeouts).
    """
    valid_checks = [c for c in checks if c.response_time is not None]

    if len(valid_checks) < MIN_CHECKS_REQUIRED:
        logger.info(
            f"Not enough data for anomaly detection "
            f"({len(valid_checks)}/{MIN_CHECKS_REQUIRED} checks with valid response_time)."
        )
        return [(c, False) for c in checks]

    response_times = np.array([[c.response_time] for c in valid_checks])

    model = IsolationForest(contamination=0.1, random_state=42)
    predictions = model.fit_predict(response_times)  # -1 = anomaly, 1 = normal

    result = []
    valid_index = 0
    for check in checks:
        if check.response_time is None:
            result.append((check, False))
        else:
            is_anomaly = predictions[valid_index] == -1
            result.append((check, bool(is_anomaly)))
            valid_index += 1

    return result