# Car Listing Analysis Plotter using Cars.com - Amair084 on GitHub

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import sys, os

def get_data_dir():
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = Path(__file__).parent.parent
    return Path(base) / "data"

# Dark theme defaults ───────────────────────────────────────
DARK_BG    = "#1a1a1a"
AXES_BG    = "#222222"
TEXT_COLOR = "#e2e8f0"
GRID_COLOR = "#444444"
SPINE_COLOR = "#444444"

def apply_dark_theme(fig, ax):
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(AXES_BG)
    ax.title.set_color(TEXT_COLOR)
    ax.xaxis.label.set_color(TEXT_COLOR)
    ax.yaxis.label.set_color(TEXT_COLOR)
    ax.tick_params(colors=TEXT_COLOR)
    ax.grid(True, linestyle="--", alpha=0.3, color=GRID_COLOR)
    for spine in ax.spines.values():
        spine.set_edgecolor(SPINE_COLOR)
    legend = ax.get_legend()
    if legend:
        legend.get_frame().set_facecolor("#2b2b2b")
        legend.get_frame().set_edgecolor("#555555")
        for text in legend.get_texts():
            text.set_color(TEXT_COLOR)
        legend.get_title().set_color("#AB74CF")

class Plot():
    def __init__(self, name):
        self.name = name
        lname = self.name.lower()

        print(name)

        self.df = pd.read_csv(get_data_dir() / f"{lname}_market_data.csv", encoding="utf-8", on_bad_lines="skip")
        df = self.df

        df["price"] = (
            df["price"]
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .astype(float)
        )

        df["mileage"] = (
            df["mileage"]
            .str.replace(" mi.", "", regex=False)
            .str.replace(",", "", regex=False)
            .astype(float)
        )

        df["age"] = datetime.datetime.now().year - df["year"]

        print(f"{lname}_market_data.csv")

    def age_plot(self):
        df = self.df

        colors_list = ["#8136B2", "#AB74CF", "#1f77b4", "#ff7f0e"]
        colors = {model: colors_list[i] for i, model in enumerate(df["model"].unique())}

        fig, ax = plt.subplots(figsize=(10, 6))
        fig.canvas.manager.set_window_title("Cars.com Market Analysis")

        for model, color in colors.items():
            subset = df[df["model"] == model]
            ax.scatter(subset["price"], subset["age"],
                       label=model, color=color, alpha=0.85, edgecolors="#555555")

        ax.set_title("Car Prices vs Age", fontsize=16)
        ax.set_xlabel("Price ($)")
        ax.set_ylabel("Age (years)")
        ax.legend(title="Model")

        apply_dark_theme(fig, ax)
        plt.tight_layout()
        plt.show()

    def python_plot(self):
        df = self.df

        colors_list = ["#8136B2", "#AB74CF", "#1f77b4", "#ff7f0e"]
        colors = {model: colors_list[i] for i, model in enumerate(df["model"].unique())}

        fig, ax = plt.subplots(figsize=(10, 6))
        fig.canvas.manager.set_window_title("Cars.com Market Analysis")

        for model, color in colors.items():
            subset = df[df["model"] == model]
            ax.scatter(subset["mileage"], subset["price"],
                       label=model, color=color, alpha=0.85, edgecolors="#555555")

        ax.set_title("Car Prices vs Mileage", fontsize=16)
        ax.set_xlabel("Mileage")
        ax.set_ylabel("Price ($)")
        ax.legend(title="Model")

        apply_dark_theme(fig, ax)
        plt.tight_layout()
        plt.show()

    def getavg(self):
        df = self.df
        avglist = [p for p in df["price"] if isinstance(p, float)]
        print(avglist)
        avg = sum(avglist) / len(avglist)
        return avg


if __name__ == "__main__":
    app = Plot("charger")