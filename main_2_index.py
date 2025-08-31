import os
import yaml

dirname = os.path.dirname(__file__)

def get_list():
    full_dir = f'{dirname}/out'
    files = os.listdir(full_dir)
    files = [f'{dirname}/out/{f}' for f in files]
    return files

def read_yml(full_path):
    with open(full_path) as f:
        return yaml.safe_load(f)

# word_index = {
#   'word1': [
#       {name_file, id_project, tag_card},
#   ],
# }

def main():
    word_index = {}
    item_file = get_list()[0]
    item_obj = read_yml(item_file)
    for key_project, item_project in item_obj.items():

        for item_text in item_project['text']:
            for item_word in item_text.split(' '):
                item_word = item_word.lower()
                if item_word not in word_index:
                    word_index[item_word] = []
                word_index[item_word].append({
                    'name_file': item_file,
                    'id_project': key_project,
                    'tag_card': 'text',
                })
    word_index_arr = []
    for item_word in word_index.keys():
        word_index_arr.append([ item_word, len(word_index[item_word]) ])
    for item in sorted(word_index_arr, key=lambda x: x[1]):
        if len(item[0]) < 4:
            continue
        print(item)
    #  with open(f'{dirname}/word_index.yml', 'w') as f:
        #  yaml.safe_dump(word_index, f, encoding='utf-8', allow_unicode=True)

if __name__ == '__main__':
    main()
