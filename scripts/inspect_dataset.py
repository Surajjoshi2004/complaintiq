from collections import Counter
from itertools import islice

from datasets import load_dataset


DATASET_NAME = "Mouwiya/cfpb-consumer-complaints"
SAMPLE_SIZE = 10_000


def main() -> None:
    dataset = load_dataset(
        DATASET_NAME,
        split="train",
        streaming=True,
    )
    dataset = dataset.shuffle(seed=42, buffer_size = 10_000 )

    product_counts: Counter[str] = Counter()
    total = 0
    usable = 0

    for record in islice(dataset, SAMPLE_SIZE):
        total += 1

        narrative = record.get("consumer_complaint_narrative")

        if not isinstance(narrative, str) or not narrative.strip():
            continue

        product = record.get("product")

        if isinstance(product, str) and product.strip():
            product_counts[product] += 1
            usable += 1

    print(f"Records inspected: {total}")
    print(f"Records with usable text and labels: {usable}")
    print("\nProduct distribution:")

    for product, count in product_counts.most_common():
        print(f"{product}: {count}")


if __name__ == "__main__":
    main()