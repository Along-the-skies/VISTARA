from search.hybrid import hybrid_search

def format_result(result):
    return {
        "id":result["id"],
        "path":result["path"],
        "title":result["title"],
        "file_type":result["file_type"],
        "snippet":result["snippet"],
        "score":result["score"]
    }
def run_search(query):
    raw_results=hybrid_search(query)

    results =[]

    for result in raw_results:
        results.append(format_result(result))

    return results