def rank_candidates(candidates):

    ranked = sorted(
        candidates,
        key=lambda x: x["total_score"],
        reverse=True
    )

    return ranked