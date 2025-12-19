import pandas as pd
from sklearn.model_selection import train_test_split

from training.steps.train_model import train
from training.steps.evaluate_model import evaluate
from training.steps.save_model import save


def run_pipeline():
    # 1️⃣ Load data
    df = pd.read_csv("data/processed/ads_features.csv")

    X = df[
        ["cost", "priority", "clicks", "conversions", "conversion_rate"]
    ]
    y = df["value_score"]

    # 2️⃣ Split ONCE
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 3️⃣ Train ONCE
    model = train(X_train, y_train)

    # 4️⃣ Evaluate
    mse = evaluate(model, X_test, y_test)
    print(f"Evaluation MSE: {mse:.2f}")

    # 5️⃣ Save
    save(model)
    print("Model saved successfully.")


if __name__ == "__main__":
    run_pipeline()
