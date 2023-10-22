import csv
import json


def remove_bom_from_keys(data):
    cleaned_data = {}
    for key, value in data.items():
        cleaned_key = key.strip('\ufeff')
        cleaned_data[cleaned_key] = value
    return cleaned_data


def csv_to_json(csv_file_path, json_file_path):
    json_array = []

    # read csv file
    with open(csv_file_path, encoding='utf-8') as csvf:
        # load csv file data using csv library's dictionary reader
        csv_reader = csv.DictReader(csvf)

        # convert each csv row into python dict
        for row in csv_reader:
            # add this python dict to json array
            # Remove BOM from field values if present
            row = remove_bom_from_keys(row)
            json_array.append(row)

    # convert python jsonArray to JSON String and write to file
    with open(json_file_path, 'w', encoding='utf-8') as jsonf:
        json_string = json.dumps(json_array, indent=4)
        jsonf.write(json_string)


csv_to_json(csv_file_path='../Corpus/190046E_Corpus.csv', json_file_path='../Corpus/data.json')
