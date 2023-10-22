import configparser
import json

from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Index, Document, Text, Long, Date, Keyword

config = configparser.ConfigParser()
config.read('config.ini')

es = Elasticsearch(
    cloud_id=config['ELASTIC']['cloud_id'],
    basic_auth=(config['ELASTIC']['user'], config['ELASTIC']['password'])
)

INDEX = 'metaphor-master'


class MetaphorDocument(Document):
    Poem_Name_EN = Text(analyzer='english')
    Poem_Name_SN = Keyword()
    Poet_SN = Keyword()
    Poet_EN = Text(analyzer='english')
    Year = Date(format="yyyy", ignore_malformed=True, type="keyword")
    Count_of_the_metaphor = Long()
    Target_domain = Text()
    Source_domain = Text()
    Metaphorical_term = Text()


def createIndex():
    index = Index(INDEX, using=es)
    index.document(MetaphorDocument)
    res = index.create()
    print(res)


def read_all_poems(json_file_path):
    with open(json_file_path, 'r') as f:
        all_poems = json.loads(f.read())
        res_list = [i for n, i in enumerate(all_poems) if i not in all_poems[n + 1:]]
        return res_list


def filter_metaphors(corpus_data_array):
    # Use list comprehension to filter data objects that have metaphor
    filtered_data = [data for data in corpus_data_array if str.lower(data["Metaphor present or not"]) == "yes"]
    return filtered_data


def generate_data(corpus_data_array):
    for poem in corpus_data_array:
        # English
        poem_english_name = poem.get("Poem Name_EN", None)
        poet_english_name = poem.get("Poet_EN", None)

        # Sinhala
        poem_sinhala_name = poem.get("Poem Name_SN", None)
        poet_sinhala_name = poem.get("Poet_SN", None)
        poem_line = poem.get("Line", None)

        published_year = poem.get("Year", None)

        number_of_meta = poem.get("Count of the metaphor", None)
        target_of_meta = poem.get("Target domain", None)

        source_of_meta = poem.get("Source domain", None)
        meta = poem.get("Metaphorical term", None)

        yield {
            "_index": INDEX,
            "_source": {
                "Poem_Sinhala_Name": poem_sinhala_name,
                "Poem_English_Name": poem_english_name,
                "Poet_Sinhala_Name": poet_sinhala_name,
                "Poet_English_Name": poet_english_name,
                "Year": published_year,
                "Line": poem_line,
                "Count_of_the_metaphor": number_of_meta,
                "Target_domain": target_of_meta,
                "Source_domain": source_of_meta,
                "Metaphorical_term": meta
            },
        }


createIndex()
corpus_data = read_all_poems("./Corpus/data.json")
filtered_corpus_data = filter_metaphors(corpus_data)
helpers.bulk(es, generate_data(filtered_corpus_data))
