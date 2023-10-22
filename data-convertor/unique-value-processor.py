import csv
import json
import pandas as pd


def csv_to_json_column_wise(csv_file_path):
    json_array = []

    poet_en = []
    poet_sn = []

    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path, encoding='utf-8')

    # Create JSON arrays from the 'Poet_EN' and 'Poet_SN' columns
    poet_en_json = json.loads(df['Poet_EN'].to_json(orient='values', force_ascii=False))
    poet_sn_json = json.loads(df['Poet_SN'].to_json(orient='values', force_ascii=False))

    # convert python jsonArray to JSON String and write to file
    with open('../Corpus/Poet_EN.json', 'w', encoding='utf-8') as jsonf:
        json_string = json.dumps(poet_en_json, indent=4)
        jsonf.write(json_string)

    with open('../Corpus/Poet_SN.json', 'w', encoding='utf-8') as jsonf:
        json_string = json.dumps(poet_sn_json, indent=4)
        jsonf.write(json_string)


csv_to_json_column_wise("../Corpus/Courpus_poet_Unique_values.csv")
