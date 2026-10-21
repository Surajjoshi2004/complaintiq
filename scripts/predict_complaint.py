
import joblib
from pathlib import Path


MODEL_PATH = Path("artifacts/complaint_classifier.joblib")


def main():
    model = joblib.load(MODEL_PATH)

    complaint = """
    My credit report contains an account that I do not recognize.
    I contacted the company to dispute the account, but the
    incorrect information is still appearing on my report.
    """

    prediction = model.predict([complaint])[0]
    probabilities = model.predict_proba([complaint])[0]

    confidence = max(probabilities)

    print("Complaint:", complaint.strip())
    print("Predicted category:", prediction)
    print(f"Model confidence: {confidence:.2%}")


if __name__ == "__main__":
    main()
