# Car Listing Cleaner using Cars.com - Amair084 on GitHub

import pandas as pd
from pathlib import Path
import sys, os

def get_data_dir():
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = Path(__file__).parent.parent
    data_dir = Path(base) / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir


class Clean():
    def __init__(self, name):
        # Get Input  ----------------
        self.name = name
        lname = self.name.lower()

        data_path = get_data_dir()

        # Create Vars for csv files  ----------------

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

        print(df.head())

if __name__ == "__main__":
    app = Clean()
    app.mainloop()