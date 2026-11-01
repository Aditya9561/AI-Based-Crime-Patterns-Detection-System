import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from .data_loader import load_crime_data, prepare_features


def detect_crime_anomalies(contamination=0.05):
    # Load cleaned crime data
    df = load_crime_data()
    features = prepare_features(df)

    # Reduce extreme differences in crime counts
    transformed = np.log1p(features)

    # Train Isolation Forest
    model = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=42
    )

    predictions = model.fit_predict(transformed)

    # Prepare district-level results
    results = df[["States/UTs", "District", "Location"]].copy()
    results["Anomaly"] = predictions == -1
    results["Anomaly_Score"] = -model.score_samples(transformed)

    results["Pattern"] = results["Anomaly"].map({
        True: "Unusual Pattern",
        False: "Typical Pattern"
    })

    return results
