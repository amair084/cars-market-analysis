import pandas as pd
from pathlib import Path


current_dir = Path(__file__).parent
data_path = current_dir.parent / "data"

corolla = pd.read_csv(data_path / "corolla_market_data.csv", encoding="utf-8", on_bad_lines="skip")
fourrunner = pd.read_csv(data_path / "4runner_market_data.csv", encoding="utf-8", on_bad_lines="skip")
camry = pd.read_csv(data_path / "camry_market_data.csv", encoding="utf-8", on_bad_lines="skip")

# print(df.columns)
# print(df.head())
#
# df["condition"] = df["year"]
#
# df = df[[
#     "condition",
#     "year",
#     "model",
#     "trim",
#     "title",
#     "price",
#     "mileage",
#     "dealer",
#     "deal",
#     "link"
# ]]
#
# df = df.dropna(how="all")
#
# df['model'] = pd.to_numeric(df['model'], errors='coerce').astype('Int64')
#
# df["year"] = df["model"]
#
# df["model"] = "Camry"


df = pd.read_csv(data_path / "toyota_combined.csv", encoding="utf-8", on_bad_lines="skip")

df["price"] = (
    df["price"]
    .astype(int)
)

df["mileage"] = (
    df["mileage"]
    .astype(int)
)

df["year"] = df["year"].astype(int)

df.to_csv(data_path /  "toyota_combined.csv", index=False)

print(df.head())


#camry["model"] = "Camry"
#corolla["model"] = "Corolla"
#fourrunner["model"] = "4Runner"


