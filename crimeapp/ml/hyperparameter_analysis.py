import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from .data_loader import load_crime_data, prepare_features


def analyze_hyperparameters():
    df = load_crime_data()
    X = prepare_features(df)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    results = []

    # Test different model settings
    for estimators in [100, 200]:
        for contamination in [0.03, 0.05, 0.08]:

            model = IsolationForest(
                n_estimators=estimators,
                contamination=contamination,
                random_state=42
            )

            predictions = model.fit_predict(X_scaled)

            results.append({
                "Estimators": estimators,
                "Contamination": contamination,
                "Anomalies_Detected": int((predictions == -1).sum())
            })

    return pd.DataFrame(results)