def single_phrase_prefix_match(query, field):
    q = {
        "size": 200,
        "explain": True,
        "query": {
            "match_phrase_prefix": {
                field: {
                    "query": query,
                    "analyzer": "standard",
                    # standard, simple, whitespace, stop, keyword, pattern, <language>, fingerprint
                }
            }
        },
        "aggs": {
            "Poet Filter": {
                "terms": {
                    "field": "Poet_English_Name.keyword",
                    "size": 10
                }
            },
            "Year Filter": {
                "terms": {
                    "field": "Year.keyword",
                    "size": 10
                }
            }

        }
    }
    return q


def exact_field_match(query, field):
    q = {
        "query": {
            "term": {
                field: query
            }
        },
        "aggs": {
            "Poet Filter": {
                "terms": {
                    "field": "Poet_English_Name.keyword",
                    "size": 10
                }
            },
            "Year Filter": {
                "terms": {
                    "field": "Year.keyword",
                    "size": 10
                }
            }

        }
    }
    return q


def fuzzy_multi_match(query, fields, operator='or'):
    q = {
        "size": 200,
        "explain": True,
        "query": {
            "multi_match": {
                "query": query,
                "fields": fields,
                "type": "best_fields",  # best_fields, most_fields, cross-fields, phrase, phrase_prefix try all
                "operator": operator,
                # "minimum_should_match": 2, # How many terms must be included to match if the operator is or
                "analyzer": "standard",  # standard, simple, whitespace, stop, keyword, pattern, <language>, fingerprint
                "fuzziness": "AUTO",
                # The number of character edits (insert, delete, substitute) to get the required term
                "fuzzy_transpositions": True,  # Allow character swaps
                "lenient": False,  # Avoid data type similarity requirement
                "prefix_length": 0,
                "max_expansions": 50,
                "auto_generate_synonyms_phrase_query": True,
                "zero_terms_query": "none"
            }
        },
        "aggs": {
            "Poet Filter": {
                "terms": {
                    "field": "Poet_English_Name.keyword",
                    "size": 10
                }
            },
            "Year Filter": {
                "terms": {
                    "field": "Year.keyword",
                    "size": 10
                }
            }

        }
    }
    return q
