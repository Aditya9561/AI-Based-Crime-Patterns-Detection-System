from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "crime_data.csv"

EXCLUDED_PATTERN = (
    r"crime branch|cyber cell|C\. I\. D\.|G\. R\. P\.|railway"
)

FEATURE_COLUMNS = [
    "Murder",
    "Attempt to commit Murder",
    "Culpable Homicide not amounting to Murder",
    "Attempt to commit Culpable Homicide",
    "Rape",
    "Attempt to commit Rape",
    "Kidnapping & Abduction_Total",
    "Dacoity",
    "Robbery",
    "Theft",
    "Unlawful Assembly",
    "Riots",
    "Criminal Breach of Trust",
    "Cheating",
    "Forgery",
    "Arson",
    "Grievous Hurt",
    "Acid attack",
    "Dowry Deaths",
    "Sexual Harassment",
    "Cruelty by Husband or his Relatives",
    "Causing Death by Negligence",
    "Offences against State",
    "Extortion",
    "Incidence of Rash Driving",
    "HumanTrafficking",
    "Unnatural Offence",
    "Other IPC crimes",
]


def load_crime_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    required = ["States/UTs", "District", "Year"] + FEATURE_COLUMNS
    missing = [column for column in required if column not in df.columns]

    if missing:
        raise ValueError(f"Missing dataset columns: {missing}")

    df["District"] = df["District"].astype(str).str.strip()
    df["States/UTs"] = df["States/UTs"].astype(str).str.strip()

    exclude = (
        df["District"].str.lower().eq("total")
        | df["District"].str.contains(
            EXCLUDED_PATTERN, case=False, regex=True, na=False
        )
    )

    df = df.loc[~exclude].copy()

    df["Location"] = df["District"] + ", " + df["States/UTs"]

    if df["Location"].duplicated().any():
        raise ValueError("Duplicate geographical locations found.")

    for column in FEATURE_COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

    return df


def prepare_features(df):
    return df[FEATURE_COLUMNS].copy()


