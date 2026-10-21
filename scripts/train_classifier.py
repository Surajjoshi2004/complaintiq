from collections import Counter
from pathlib import Path
import joblib
from imblearn.over_sampling import RandomOverSampler
from sklearn.base import clone


from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score
from sklearn.pipeline import FeatureUnion
# ==========================================
# CONFIGURATION & HYPERPARAMETERS
# ==========================================
# Hugging Face dataset path for CFPB consumer complaints
DATASET_NAME = "Mouwiya/cfpb-consumer-complaints"

# Maximum number of complaint records to sample from the dataset
SAMPLE_SIZE = 10_000

# Fixed seed for reproducibility across randomized steps (shuffling, splitting, training)
RANDOM_SEED = 42

# Key names inside the dataset record dictionaries
TEXT_COLUMN = "consumer_complaint_narrative"  # Feature column (Input text)
LABEL_COLUMN = "product"                      # Target column (Product category label)


def load_training_data():
    """
    Streams data directly from Hugging Face, shuffles it using a streaming buffer,
    filters out invalid/empty records, and stops once SAMPLE_SIZE valid records are fetched.
    """
    # Load dataset in streaming mode so the entire dataset isn't loaded into RAM all at once
    dataset = load_dataset(
        DATASET_NAME,
        split="train",
        streaming=True
    )

    # Shuffle dataset using a buffer to ensure random sampling while streaming
    dataset = dataset.shuffle(seed=RANDOM_SEED, buffer_size=10_000)

    texts = []
    labels = []

    # Iterate through streamed records
    for record in dataset:
        narrative = record.get(TEXT_COLUMN)
        label = record.get(LABEL_COLUMN)

        # Skip records missing a valid string label
        if not isinstance(label, str) or not label.strip():
            continue

        # Skip records missing a valid narrative text
        if not isinstance(narrative, str) or not narrative.strip():
            continue

        # Clean leading/trailing whitespaces and save to lists
        texts.append(narrative.strip())
        labels.append(label.strip())

        # Break early once desired sample size is reached
        if len(texts) >= SAMPLE_SIZE:
            break

    return texts, labels


def filter_rare_categories(texts, labels, min_samples=20):
    """
    Removes categories with fewer than `min_samples` instances.
    Prevents errors during stratified splits and improves training stability on minority classes.
    """
    # Count occurrences of each category label
    counts = Counter(labels)

    # Filter categories that meet the minimum frequency threshold
    valid_categories = {
        category
        for category, count in counts.items()
        if count >= min_samples
    }

    # Keep only samples belonging to valid categories
    #tuples ki list 
    filtered = [
        (text, label)
        for text, label in zip(texts, labels)
        if label in valid_categories
    ]

    # Unpack filtered (text, label) pairs back into separate lists
    filtered_texts = [text for text, label in filtered]
    filtered_labels = [label for text, label in filtered]

    # Print summary statistics
    print("Category counts before filtering:")
    for category, count in counts.most_common():
        print(f"{category}: {count}")

    print(f"\nCategories retained: {len(valid_categories)}")
    print(f"Examples retained: {len(filtered_texts)}")
    print(f"Examples removed: {len(texts) - len(filtered_texts)}")

    return filtered_texts, filtered_labels


def main():
    # ----------------------------------------------------
    # Step 1: Load and Clean Dataset
    # ----------------------------------------------------
    texts, labels = load_training_data()
    print(f"Loaded complaints: {len(texts)}")

    # Filter out rare classes that do not have enough samples
    texts, labels = filter_rare_categories(
        texts,
        labels,
        min_samples=20
    )
    print(f"\nFinal training dataset size: {len(texts)}")

    # ----------------------------------------------------
    # Step 2: Train-Test Split (80% Train, 20% Test)
    # ----------------------------------------------------
    # `stratify=labels` maintains the same class distributions in both train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=0.2,
        random_state=RANDOM_SEED,
        stratify=labels
    )
    oversampler = RandomOverSampler(random_state= Rand)
    

    print(f"Training examples: {len(X_train)}")
    print(f"Testing examples: {len(X_test)}")

    # ----------------------------------------------------
    # Step 3: Build Machine Learning Pipeline
    # ----------------------------------------------------
    model = Pipeline([
        # Vectorizer: Converts raw text into numerical TF-IDF feature vectors
        ("features",FeatureUnion([
            ("word_tfidf", TfidfVectorizer(
                analyzer="word",
                max_features=20_000,
                ngram_range=(1,2),
                stop_words="english"
            )),
            ("char_tfidf",TfidfVectorizer(
                analyzer="char",
                max_features=20_000,
                ngram_range=(3,5),
                min_df=2
            ))
    ])),
        # Classifier: Multi-class Logistic Regression model
        ("classifier", LogisticRegression(
            max_iter=1_000,          # Increase iterations to guarantee convergence
            class_weight="balanced", # Adjust weights inversely proportional to class frequencies
            random_state=RANDOM_SEED,
        ))
    ])

    # ----------------------------------------------------
    # Step 4: Train Model
    # ----------------------------------------------------
    print("\nTraining the classifier...")
    model.fit(X_train, y_train)
    print("Training complete!")

    # ----------------------------------------------------
    # Step 5: Save Model Artifact to Disk
    # ----------------------------------------------------
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    model_path = artifacts_dir / "complaint_classifier.joblib"
    joblib.dump(model, model_path)  # Persists the entire pipeline (vectorizer + model)

    print(f"Model saved to: {model_path}")

    # ----------------------------------------------------
    # Step 6: Evaluate Model on Test Set
    # ----------------------------------------------------
    predictions = model.predict(X_test)
    
    print("\nMisclassified complaint examples:")
    
    shown = 0
    
    for text,actual,predicted in zip(X_test,y_test,predictions):
        if actual != predicted:
            print(f"\n Actual:    {actual}")
            print(f"Prediced: {predicted}")
            print(f"Complaint: {text[:300]}")
            
            shown +=1
        if shown == 10:
            break
    

    # Output detailed metrics (Precision, Recall, F1-Score per class)
    print("\nClassification Report:")
    print(classification_report(
        y_test,
        predictions,
        zero_division=0,
    ))

    # Confusion matrix to inspect exact prediction vs actual overlaps
    print("\nConfusion Matrix:")
    print(confusion_matrix(
        y_test,
        predictions,
        labels=model.classes_,
    ))

    # Print label indices matching rows/columns of the confusion matrix
    print("\nCategory order in confusion matrix:")
    for index, category in enumerate(model.classes_):
        print(f"{index}: {category}")
        
    print("Accuracy:", accuracy_score(y_test, predictions))
    print("Macro F1:", f1_score(y_test, predictions, average="macro"))
    print("Weighted F1:", f1_score(y_test, predictions, average="weighted"))


if __name__ == "__main__":
    main()