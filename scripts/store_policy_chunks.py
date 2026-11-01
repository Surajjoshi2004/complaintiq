import psycopg
from sentence_transformers import SentenceTransformer
from complaintiq.config import settings

model = SentenceTransformer("all-MiniLM-L6-v2")

policy = (
    "A customer must report an unauthorized transaction within 48 hours. "
    "The bank will investigate the transaction and determine whether "
    "reimbursement is appropriate.\n\n"
    "Home loan applicants must submit proof of income and property documents."
)

def chunk_text(text, max_chars=300):
    paragraphs = text.split("\n\n")
    chunks = []

    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        sentences = paragraph.split(".")
        current_chunk = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            if current_chunk and len(current_chunk) + len(sentence) + 2 > max_chars:
                chunks.append(current_chunk)
                current_chunk = sentence
            else:
                if current_chunk:
                    current_chunk += ". " + sentence
                else:
                    current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk)

    return chunks


database_url = settings.database_url.replace(
    "postgresql+psycopg://",
    "postgresql://",
)

chunks = chunk_text(policy)
embeddings = model.encode(chunks)

with psycopg.connect(database_url) as conn:
    with conn.cursor() as cur:
        for chunk, embedding in zip(chunks, embeddings):
            cur.execute(
                """
                INSERT INTO policy_chunks (content, embedding)
                VALUES (%s, %s)
                """,
                (chunk, embedding.tolist()),
            )

print(f"Stored {len(chunks)} policy chunks.")