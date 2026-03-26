# Car Listing Analysis Plotter using Cars.com - Amair084 on GitHub

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

current_dir = Path(__file__).parent
data_path = current_dir.parent / "data"

df = pd.read_csv(data_path / "toyota_combined.csv", encoding="utf-8", on_bad_lines="skip")

plt.figure()
models = df["model"].unique()

plt.title("Toyota")

for model in models:
    subset = df[df["model"] == model]
    plt.scatter(subset["mileage"], subset["price"], label=model)

plt.xlabel("Mileage")
plt.ylabel("Price ($)")
plt.title("Toyota Price vs Mileage")
plt.legend()

plt.show()