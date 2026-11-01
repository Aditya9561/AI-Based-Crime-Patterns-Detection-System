import pandas as pd

from .data_loader import load_crime_data, FEATURE_COLUMNS


def generate_crime_summary():
    df = load_crime_data()

    total_column = "Total Cognizable IPC crimes"

    if total_column not in df.columns:
        raise ValueError(f"Missing column: {total_column}")

    df[total_column] = pd.to_numeric(
        df[total_column], errors="coerce"
    ).fillna(0)

    top_districts = (
        df[["States/UTs", "District", total_column]]
        .sort_values(total_column, ascending=False)
        .head(10)
    )

    crime_totals = (
        df[FEATURE_COLUMNS]
        .sum()
        .sort_values(ascending=False)
    )

    summary = {
        "total_districts": len(df),
        "total_categories": len(FEATURE_COLUMNS),
        "total_recorded_crimes": int(df[total_column].sum()),
        "average_per_district": round(df[total_column].mean(), 2),
    }

    return summary, top_districts, crime_totals
