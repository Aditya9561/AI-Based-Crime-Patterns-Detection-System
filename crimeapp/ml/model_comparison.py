
from sklearn.neighbors import LocalOutlierFactor
from .data_loader import load_crime_data, prepare_features
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest


def compare_anomaly_models():
    df = load_crime_data()
    X = prepare_features(df)

    # Scale the crime data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Model 1: Isolation Forest
    isolation_model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )
    isolation_predictions = isolation_model.fit_predict(X_scaled)

    # Model 2: Local Outlier Factor
    lof_model = LocalOutlierFactor(
        n_neighbors=20,
        contamination=0.05
    )
    lof_predictions = lof_model.fit_predict(X_scaled)

    # Combine results
    results = df[["States/UTs", "District"]].copy()
    results["Isolation_Forest"] = isolation_predictions == -1
    results["Local_Outlier_Factor"] = lof_predictions == -1

    results["Both_Models_Flagged"] = (
        results["Isolation_Forest"]
        & results["Local_Outlier_Factor"]
    )

    # Calculate model agreement
    summary_both = int(results["Both_Models_Flagged"].sum())

    union_count = int(
        (
            results["Isolation_Forest"]
            | results["Local_Outlier_Factor"]
        ).sum()
    )

    jaccard_score = (
        summary_both / union_count if union_count else 0
    )

    summary = {
        "isolation_count": int(results["Isolation_Forest"].sum()),
        "lof_count": int(results["Local_Outlier_Factor"].sum()),
        "both_count": summary_both,
        "union_count": union_count,
        "jaccard_percentage": round(jaccard_score * 100, 2),
    }

    return results, summary
