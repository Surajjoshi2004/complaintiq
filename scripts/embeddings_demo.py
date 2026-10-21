# from sentence_transformers import SentenceTransformer

# from sentence_transformers import util 

# model = SentenceTransformer("all-MiniLM-L6-v2")

# sentences= ["Money was withdrawn from my bank account without my permission.",
#             "An unauthorized transaction occured in my bank account.",
#             "I want to apply for home loan."
#             ]

# embeddings = model.encode(sentences)

# similarity= util.cos_sim(embeddings,embeddings)

# print(similarity)

# print("Embedding shape:", embeddings.shape)


# print("\n Number of dimensions:", len(embeddings[0]))

from sentence_transformers import SentenceTransformer, util 

model = SentenceTransformer("all-MiniLM-L6-v2")

complaint = "My bank transferred money from my bank account without my permission."

documents=[
       "Unauthorized transactions should be investigated using the applicable dispute procedure.",
    "Home loan applications require verification of income and property documents.",
    "Customers should report suspicious debit-card transactions to their bank promptly."
]

complaint_embedding = model.encode(complaint,convert_to_tensor=True)
document_embedding = model.encode(documents, convert_to_tensor=True)
