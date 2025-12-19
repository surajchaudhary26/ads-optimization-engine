import pandas as pd


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Avoid division by zero
    df["conversion_rate"] = df["conversions"] / df["clicks"].replace(0, 1)

    return df


if __name__ == "__main__":
    df = pd.read_csv("data/raw/ads_historical.csv")
    df = add_features(df)

    df.to_csv("data/processed/ads_features.csv", index=False)
    print("Feature engineered data saved.")
