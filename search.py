from elasticsearch import Elasticsearch
import configparser
import queries
import booster
from booster import is_english
import re

config = configparser.ConfigParser()
config.read('config.ini')

es = Elasticsearch(
    cloud_id=config['ELASTIC']['cloud_id'],
    basic_auth=(config['ELASTIC']['user'], config['ELASTIC']['password'])
)

INDEX = 'metaphor-master'


# Function to check if a string is a valid year
def is_valid_year(input_string):
    # Define a regular expression pattern for a valid year (four digits)
    year_pattern = r"^\d{4}$"
    if re.match(year_pattern, input_string):
        return True
    else:
        return False


def boost(boost_array):
    term1 = "Poem_English_Name^{}".format(boost_array[0])
    term2 = "Poet_English_Name^{}".format(boost_array[1])
    term3 = "Poem_Sinhala_Name^{}".format(boost_array[2])
    term4 = "Poet_Sinhala_Name^{}".format(boost_array[3])
    term5 = "Year^{}".format(boost_array[4])
    term6 = "Line^{}".format(boost_array[5])
    term7 = "Metaphorical_term^{}".format(boost_array[6])
    term8 = "Target_domain^{}".format(boost_array[7])
    term9 = "Source_domain^{}".format(boost_array[8])
    term10 = "Count_of_the_metaphor^{}".format(boost_array[9])

    return [term1, term2, term3, term4, term5, term6, term7, term8, term9, term10]


def search(search_text, search_type):
    phrase = search_text.strip()
    if search_type == "anywhere":
        flags = booster.boost_field(phrase)
        fields = boost(flags)
        query_body = queries.fuzzy_multi_match(phrase, fields)

    elif search_type == "title_only":
        if is_english(phrase):
            query_body = queries.single_phrase_prefix_match(phrase, "Poem_English_Name")
        else:
            query_body = queries.single_phrase_prefix_match(phrase, "Poem_Sinhala_Name")

    elif search_type == "metaphors_only":
        if not is_english(phrase):
            query_body = queries.fuzzy_multi_match(phrase, ["Metaphorical_term", "Line"])
        else:
            return "Cannot search metaphors in english"

    elif search_type == "year_only":
        if is_valid_year(phrase):
            query_body = queries.exact_field_match(phrase, "Year")
        else:
            return "Invalid Year"

    res = es.search(index=INDEX, body=query_body)  # Calling the elastic search client with the corresponding query body
    return res
