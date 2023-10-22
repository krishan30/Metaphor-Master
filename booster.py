import json


def read_unique_vals(path):
    with open(path, 'r') as f:
        json_data = json.loads(f.read())
        res_list = [i for n, i in enumerate(json_data) if i not in json_data[n + 1:]]
        return res_list


poet_en = read_unique_vals("./Corpus/Poet_EN.json")  # 2
poet_sn = read_unique_vals("./Corpus/Poet_SN.json")  # 4

all_unique_data = [poet_en, poet_sn]
position_arr = [2, 4]


def is_english(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def boost_field(phrase):
    boost_array = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    if is_english(phrase):
        for field in range(0, 2):
            boost_array[field] = 2
    else:
        for field in range(2, 10):
            boost_array[field] = 2

    phrase_list = phrase.strip().split()

    for word in phrase_list:
        for i in range(0, 2):
            if any(word.lower() in x.lower() for x in all_unique_data[i]):
                boost_array[position_arr[i]] = boost_array[position_arr[i]] + 1

    return boost_array
