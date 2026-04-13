# Car Listing Cleaner using Cars.com - Amair084 on GitHub

import pandas as pd
from pathlib import Path


class Clean():
    def __init__(self, name):
        # Get Input  ----------------
        self.name = name
        lname = self.name.lower()

        current_dir = Path(__file__).parent
        data_path = current_dir.parent / "data"

        # Create Vars for csv files  ----------------

        corolla = pd.read_csv(data_path / "corolla_market_data.csv", encoding="utf-8", on_bad_lines="skip")
        fourrunner = pd.read_csv(data_path / "4runner_market_data.csv", encoding="utf-8", on_bad_lines="skip")
        camry = pd.read_csv(data_path / "camry_market_data.csv", encoding="utf-8", on_bad_lines="skip")
        df = pd.read_csv(data_path / f"{lname}_market_data.csv", encoding="utf-8", on_bad_lines="skip")

        print(df.columns)
        print(df.head())

        # Clean Data  ----------------

        df["condition"] = df["year"]

        df = df[[
            "condition",
            "year",
            "model",
            "trim",
            "title",
            "price",
            "mileage",
            "dealer",
            "deal",
            "link"
        ]]

        df = df.dropna(how="all")

        df['model'] = pd.to_numeric(df['model'], errors='coerce').astype('Int64')

        df["year"] = df["model"]

        df["model"] = f"{name}"

        df.to_csv(data_path /  f"{lname}_market_data.csv", index=False)

        # Combiner  ----------------


        # df = pd.read_csv(data_path / "toyota_combined.csv", encoding="utf-8", on_bad_lines="skip")
        #
        # df["price"] = (
        #     df["price"]
        #     .astype(int)
        # )
        #
        # df["mileage"] = (
        #     df["mileage"]
        #     .astype(int)
        # )
        #
        # df["year"] = df["year"].astype(int)
        #
        # df.to_csv(data_path /  "toyota_combined.csv", index=False)

        print(df.head())


        #camry["model"] = "Camry"
        #corolla["model"] = "Corolla"
        #fourrunner["model"] = "4Runner"


if __name__ == "__main__":
    app = Clean()
    app.mainloop()