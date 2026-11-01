import psycopg

from sentence_transformers import SentenceTransformer
from complaintiq.config import settings



model = SentenceTransformer("all-MiniLM-L6-v2")


complaint = "my bank transferred money without my permission ."

embedding= model.encode(complaint)

embedding_list = embedding.tolist()
embedding_string = []

for number in embedding_list:
    embedding_string.append(str(number))
    
comma_separated_values = ",".join(embedding_string)

vector_string = "[" + comma_separated_values + "]"

print(vector_string[:100])

def search_policy(vector_string, top_k=2):
    database_url=settings.database_url.replace(
        "postgresql+psycopg://",
        "postgresql://"
    )
   
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT content, embedding <=> %s::vector AS distance
                FROM policy_chunks
                ORDER BY distance
                LIMIT %s;
                """,
                (vector_string, top_k),
            )
            
            results = cur.fetchall()
            
        for content, distance in results:
            print(f"Distance: {distance:.4f}")
            print(f"Policy: {content}")
            print("-" * 40)
       
    return results