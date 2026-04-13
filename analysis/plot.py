# Car Listing Analysis Plotter using Cars.com - Amair084 on GitHub

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

current_dir = Path(__file__).parent
data_path = current_dir.parent / "data"



class Plot():
    def __init__(self, name):
        self.name = name
        lname = self.name.lower()

        print(name)

        self.df = pd.read_csv(data_path / f"{lname}_market_data.csv", encoding="utf-8", on_bad_lines="skip")
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

        import datetime
        df["age"] = datetime.datetime.now().year - df["year"]

        print(f"{lname}_market_data.csv")


    def age_plot(self):
        df = self.df
        # Set Chart Settings ----------
        plt.style.use("seaborn-v0_8")

        fig, ax = plt.subplots(figsize=(10,6))

        fig.canvas.manager.set_window_title("Cars.com Market Analysis")

        # Color Code for Models -------

        number = 0

        colors_list = ["#1f77b4","#2ca02c","#ff7f0e"]

        colors = {}

        for x in df["model"].unique():
            colors[x] = colors_list[number]
            number += 1

        for model, color in colors.items():
            subset = df[df["model"] == model]

            ax.scatter(
                subset["price"],
                subset["age"],
                label=model,
                color=color,
                alpha=0.7,
                edgecolors="black"
            )

        # Labels ---------------------
        ax.set_title("Toyota Used Car Prices vs Mileage", fontsize=16)
        ax.set_xlabel("Price ($)")
        ax.set_ylabel("Age (years)")

        # Grid -----------------------
        ax.grid(True, linestyle="--", alpha=0.4)

        # Legend ---------------------
        ax.legend(title="Model")

        plt.tight_layout()
        plt.show()

    def python_plot(self):
        df = self.df
        # Set Chart Settings ----------
        plt.style.use("seaborn-v0_8")

        fig, ax = plt.subplots(figsize=(10, 6))

        fig.canvas.manager.set_window_title("Cars.com Market Analysis")

        # Color Code for Models -------

        number = 0

        colors_list = ["#1f77b4", "#2ca02c", "#ff7f0e"]

        colors = {}

        for x in df["model"].unique():
            colors[x] = colors_list[number]
            number += 1

        for model, color in colors.items():
            subset = df[df["model"] == model]

            ax.scatter(
                subset["mileage"],
                subset["price"],
                label=model,
                color=color,
                alpha=0.7,
                edgecolors="black"
            )

        # Labels ---------------------
        ax.set_title("Car Prices vs Mileage", fontsize=16)
        ax.set_xlabel("Mileage")
        ax.set_ylabel("Price ($)")

        # Grid -----------------------
        ax.grid(True, linestyle="--", alpha=0.4)

        # Legend ---------------------
        ax.legend(title="Model")

        plt.tight_layout()
        plt.show()

    def getavg(self):
        df = self.df

        colors_list = ["#1f77b4", "#2ca02c", "#ff7f0e"]

        colors = {}

        number=0

        for x in df["model"].unique():
            colors[x] = colors_list[number]
            number += 1

        # for model, color in colors.items():
        #     subset = df[df["model"] == model]
        #
        #     print(subset["price"])

        avglist = []

        for each in df["price"]:
            if type(each) == type(0.1):
                avglist.append(each)

        print(avglist)
        avg = sum(avglist) / len(avglist)
        return avg


if __name__ == "__main__":
    app = Plot("camry")
    app.mainloop()