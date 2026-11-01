import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

from .data_loader import load_crime_data, prepare_features


def perform_crime_clustering(n_clusters=3):
    # Load cleaned district-level crime data
    df = load_crime_data()
    features = prepare_features(df)

    # Reduce the influence of extremely large crime counts
    log_features = pd.DataFrame(
        __import__("numpy").log1p(features),
        columns=features.columns,
        index=features.index
    )

    # Scale all features to comparable ranges
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(log_features)

    # Train K-Means clustering model
    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    cluster_labels = model.fit_predict(scaled_features)

    # Attach cluster labels to district information
    results = df[["States/UTs", "District", "Location"]].copy()
    results["Cluster"] = cluster_labels

    # Evaluate clustering quality
    score = silhouette_score(scaled_features, cluster_labels)

    return results, score
