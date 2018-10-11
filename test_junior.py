import re
from collections import Counter
import sys


def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as file_with_txt:
        return file_with_txt.read()


def find_hashtag(text):
    return re.findall(r'[#][а-яa-z0-9A-ZА-Я_ёЁ]+', text)


def find_meaningful_word(text):
    return re.findall(r'[а-яa-zA-ZА-ЯёЁ]+',  
        re.sub(r'[#][а-яa-zA-ZА-Я_ёЁ]+', '', text).lower())
    

def get_most_frequent_hashtag(data, number_words=10):
    return Counter(data).most_common(number_words)
 

def convert_to_list(top_popular_hashtag):
    list_hashtag = []
    for hashtag, count in top_popular_hashtag:
        list_hashtag.append(hashtag)
    return list_hashtag


def print_result(counted_words, hashtag_dict):
    print(counted_words)
    for hashtag in counted_words:
        print('{} => {!r}'.format(hashtag, hashtag_dict[hashtag]))


def find_most_popular_words(top_popular_hashtag, filename):
    hashtag_dict = {}
    for hashtag in top_popular_hashtag:
        result_data = ''
        with open(filename, 'r', encoding='utf-8') as f:
            while True:
                data = f.readline()
                if not data:
                    break
                if hashtag in data:
                    result_data += data
            hashtag_dict = entry_dict(hashtag, result_data, hashtag_dict)
    return hashtag_dict        


def entry_dict(hashtag, data_for_hashtag, hashtag_dict):
    meaningful_word = ''
    if data_for_hashtag:
        meaningful_word = convert_to_list(get_most_frequent_hashtag(find_meaningful_word(data_for_hashtag), number_words=5))
    hashtag_dict[hashtag] = meaningful_word
    return hashtag_dict


if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        #filename = 'in.txt'
        data_from_file = load_data(filename)
    except IndexError:
        print('Error: Не добавлен файл для поиска!')
    except FileNotFoundError:
        print('Error: Данный файл не существует!')
    else:
        list_hashtag = find_hashtag(data_from_file)
        if list_hashtag:
            popular_hashtag = convert_to_list(get_most_frequent_hashtag(list_hashtag))
            hashtag_dict =  find_most_popular_words(popular_hashtag, filename)
            print_result(popular_hashtag, hashtag_dict)
        else:
            print('Info: В файле нет хэштегов.')