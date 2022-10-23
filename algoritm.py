from collections import Counter
from functools import lru_cache

import datrie
import numpy as np
import pandas as pd


def get_products():
    dataframe = pd.read_excel('cte.xlsx', index_col=None)

    return dataframe


def create_trie(data_products):
    trie = datrie.Trie('abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя1234567890-:')

    for product in np.array(data_products[['id', 'name']].sample(n=500)):
        for key in product[1].lower().split(' '):
            if key not in trie.keys():
                trie[key] = [product[0]]
            else:
                trie[key].append(product[0])

    return trie


def get_product(search, trie, data_products):
    prefixes = search.lower().split(' ')
    product_ids = []

    for prefix in prefixes:
        layout = dict(zip(map(ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                                   'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'),
                        "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                        'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'))
        prefix_values = trie.values(prefix)

        if prefix_values:
            ids = prefix_values

            for id_list in ids:
                product_ids.append(id_list)

        else:
            ids = trie.values(prefix.translate(layout))

            for id_list in ids:
                product_ids.append(id_list)

    id_products_list = []

    if product_ids:
        id_products_list.extend(list(set(product_ids[0]).intersection(*[set(ids) for ids in product_ids[0:]])))
    else:
        return 'Не найден ни один товар.'

    products = data_products.loc[data_products['id'].isin(id_products_list)]
    products_items = []

    for product in np.array(products):
        products_items.append([product[1], product[0]])

    pre_results = list(sorted(products_items, key=lambda product: product[0], reverse=True))

    return pre_results


if __name__ == '__main__':
    products = get_products()
    trie = create_trie(products)
    print('Префиксное дерево создано.')
    print(trie.items())

    while True:
        prefix = str(input('Введите префикс: '))

        if prefix == 'end':
            break
        else:
            print(get_product(prefix, trie, products))
