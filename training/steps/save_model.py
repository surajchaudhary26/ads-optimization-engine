import joblib


def save(model, path="artifacts/value_model.pkl"):
    joblib.dump(model, path)
