import pandas as pd
from .data_loader import load_crime_data, FEATURE_COLUMNS


def explain_district(district_name):
    df = load_crime_data()

    # Find the selected district
    district_data = df[
        df["District"].str.lower() == district_name.lower()
    ]

    if district_data.empty:
        raise ValueError(f"District not found: {district_name}")

    # Get crime values for the selected district
    district_values = district_data.iloc[0][FEATURE_COLUMNS]

    # Calculate median values across all districts
    median_values = df[FEATURE_COLUMNS].median()

    # Calculate how much each category differs from the median
    comparison = pd.DataFrame({
        "Crime_Category": FEATURE_COLUMNS,
        "District_Cases": district_values.values,
        "Dataset_Median": median_values.values
    })

    comparison["Difference"] = (
        comparison["District_Cases"] - comparison["Dataset_Median"]
    )

    comparison["Absolute_Difference"] = comparison["Difference"].abs()

    comparison["Pattern"] = comparison["Difference"].apply(
        lambda value: "Higher than median" if value > 0
        else "Lower than median" if value < 0
        else "Equal to median"
    )

    # Display categories with the largest differences
    explanation = comparison.sort_values(
        "Absolute_Difference", ascending=False
    ).head(5)

    return explanation