import pandas as pd

# Check main_metadata.csv
df = pd.read_csv("data/main_metadata.csv", nrows=5)
print("=== main_metadata.csv ===")
print(f"Columns: {list(df.columns)}")
print(df.head(2))

# Check players_reduced.csv
df = pd.read_csv("data/players_reduced.csv", nrows=5)
print("\n=== players_reduced.csv ===")
print(f"Columns: {list(df.columns)}")
print(df.head(2))

df = pd.read_csv("data/teams.csv", nrows=5)
print("\n=== teams.csv ===")
print(f"Columns: {list(df.columns)}")
print(df.head(2))

df = pd.read_csv("data/picks_bans.csv", nrows=5)
print("\n=== picks_bans.csv ===")
print(f"Columns: {list(df.columns)}")
print(df.head(2))

