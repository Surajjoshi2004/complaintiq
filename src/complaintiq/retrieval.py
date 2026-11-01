import psycopg
from sentence_transformers import SentenceTransformer
from complaintiq.config import settings


model = SentenceTransformer("all-MiniLM-L6-v2")

def search_policy(complaint, top_k=2):
    embedding = model.encode(complaint)
    embedding_list = embedding.tolist()
    embedding_strings = []
    
    for number in embedding_list:
        embedding_str = str(number)
        embedding_strings.append(embedding_str)
    
    comma_separated_values = ",".join(embedding_strings)
    vector_string = "[" + comma_separated_values +"]"
    
    database_url = settings.database_url.replace("postgresql+psycopg://",
                                                 "postgresql://")
    
    with psycopg.connect(database_url )as conn:
        with conn.cursor() as cur:
            cur.execute(
                    """
                    SELECT content, 
                            embedding <=> %s::vector AS distance
                        FROM policy_chunks
                        ORDER BY distance
                        LIMIT %s;
                        """,
                        (vector_string, top_k)
                        )
            
            results = cur.fetchall()
    return results

results = search_policy(
    "My bank transferred money without my permission."
)

for content, distance in results:
    print(f"Distance: {distance:.4f}")
    print(f"Policy: {content}")
    print("-" * 40)