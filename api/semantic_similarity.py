from sentence_transformers import SentenceTransformer,util

def semantic_similarity(df, query, model, corpus_embeddings):
    query_embedding = model.encode(query)
    cosine_similarity = util.cos_sim(query_embedding, corpus_embeddings)[0]
    df = df.assign(similarity=cosine_similarity)

    return {
        'results':
            df[['title','url','similarity']]
                .sort_values(by='similarity',ascending=False)
                .to_dict('records')
    }