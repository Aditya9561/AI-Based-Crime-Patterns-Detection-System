from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .eda import generate_crime_summary


def create_eda_charts():
    summary, districts, categories = generate_crime_summary()

    output_dir = Path(__file__).resolve().parents[1] / "static" / "analytics"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Chart 1: Top 10 districts
    plt.figure(figsize=(11, 6))
    plt.barh(
        districts["District"] + ", " + districts["States/UTs"],
        districts["Total Cognizable IPC crimes"]
    )
    plt.xlabel("Recorded IPC Crimes")
    plt.title("Top 10 Districts by Recorded IPC Crimes (2014)")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(output_dir / "top_districts.png", dpi=150)
    plt.close()

    # Chart 2: Top 10 selected crime categories
    top_categories = categories.head(10).sort_values()

    plt.figure(figsize=(11, 6))
    plt.barh(top_categories.index, top_categories.values)
    plt.xlabel("Recorded Crime Count")
    plt.title("Top 10 Selected Crime Categories (2014)")
    plt.tight_layout()
    plt.savefig(output_dir / "top_categories.png", dpi=150)
    plt.close()

    return output_dir
