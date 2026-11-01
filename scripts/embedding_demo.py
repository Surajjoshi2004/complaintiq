from sentence_transformers import SentenceTransformer, util 

model = SentenceTransformer("all-MiniLM-L6-v2")

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


def retrieve_documents(complaint,documents,top_k=2):
    complaint_embedding = model.encode(complaint,convert_to_tensor=True)
    document_embeddings = model.encode(documents, convert_to_tensor=True)

    # return this function in one d 

    scores = util.cos_sim(complaint_embedding, document_embeddings)[0]

    ranked_indices = scores.argsort(descending=True)[:top_k]

    return [
        {
            "document": documents[index],
            "score": scores[index].item() # tensor object
        }
        for index in ranked_indices
]
complaint = "My bank transferred money from my account without my permission."

documents = [
    "A customer must report an unauthorized transaction within 48 hours. "
    "The bank will investigate the transaction and determine whether "
    "reimbursement is appropriate.\n\n"
    "Home loan applicants must submit proof of income and property documents."
]

results = retrieve_documents(complaint, documents, top_k=2)

for result in results:
    print(f"Score: {result['score']:.4f}")
    print(f"Document: {result['document']}")
    print()

policy = (
    "A customer must report an unauthorized transaction within 48 hours. "
    "The bank will investigate the transaction and determine whether "
    "reimbursement is appropriate.\n\n "
    "Home loan applicants must submit proof of income and property documents."
)

chunks = chunk_text(policy)


for i , chunk in  enumerate(chunks, start=1):
    print(f"Chunk{i}: {chunk}" )
