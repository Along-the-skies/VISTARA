from search.keyword import keyword_search
from search.semantic_search import semantic_search


def normalize_keyword_scores(results):
    if not results:
        return {}

    scores = [result[5] for result in results]

    best = min(scores)
    worst = max(scores)

    if best == worst:
        return {
            result[0]: 1.0
            for result in results
        }

    return {
        result[0]: (worst - result[5]) / (worst - best)
        for result in results
    }


def hybrid_search(
    query,
    limit=20,
    include_sensitive=False,
    keyword_weight=0.5,
    semantic_weight=0.5
):
    keyword_results = keyword_search(
        query,
        limit=limit,
        include_sensitive=include_sensitive
    )

    semantic_results = semantic_search(
        query,
        limit=limit,
        include_sensitive=include_sensitive
    )

    keyword_scores = normalize_keyword_scores(
        keyword_results
    )

    combined = {}

    for result in keyword_results:
        (
            document_id,
            path,
            title,
            file_type,
            snippet,
            score
        ) = result

        combined[document_id] = {
            "id": document_id,
            "path": path,
            "title": title,
            "file_type": file_type,
            "snippet": snippet,
            "keyword_score": keyword_scores[document_id],
            "semantic_score": 0.0
        }

    for result in semantic_results:
        (
            document_id,
            path,
            title,
            file_type,
            snippet,
            score
        ) = result

        if document_id not in combined:
            combined[document_id] = {
                "id": document_id,
                "path": path,
                "title": title,
                "file_type": file_type,
                "snippet": snippet,
                "keyword_score": 0.0,
                "semantic_score": score
            }
        else:
            combined[document_id]["semantic_score"] = score

    results = []

    for result in combined.values():
        final_score = (
            result["keyword_score"] * keyword_weight
            + result["semantic_score"] * semantic_weight
        )

        result["score"] = final_score
        results.append(result)

    results.sort(
        key=lambda result: result["score"],
        reverse=True
    )

    return results[:limit]