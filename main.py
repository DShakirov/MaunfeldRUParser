import requests
import json
import pandas as pd
import os


def get_site_data():
    url = 'https://www.maunfeld.ru/api/v1/cache/catalogProduction.getItems.json'
    response = requests.get(url=url)
    data = response.json()
    #with open('catalog.json', 'w', encoding='UTF-8') as file:
        #json.dump(data, file, indent=2, ensure_ascii=False)
    results_list = []
    for product in data:
        try:
            if product['canBuy'] == True:
                canbuy = 'В наличии'
            else:
                canbuy = 'Нет в наличии'
        except:
            canbuy = 'Нет в наличии'
        if product['isSale']:
            is_sale = 'Акционный товар'
        else:
            is_sale = 'Товар без акции'
        try:
            price_discount = f"{product['priceDiscount']}"
        except:
            price_discount = 'Нет скидки'
        results_list.append(
            {
            "Наименование":product['name'],
            "Img": f"https://www.maunfeld.ru/{product['thumb']['src']}",
            "Артикул": product['article'],
            "Доступность": canbuy,
            "Акция": is_sale,
            "Популярность": product['popularity'],
            "Цена": product['price'],
            "Цена со скидкой": price_discount
            }
        )

    if not os.path.exists('results'):
        os.mkdir('results')

    df = pd.DataFrame(results_list)
    writer = pd.ExcelWriter('results/results.xlsx')
    df.to_excel(writer, 'result')
    writer.book.save('results/results.xlsx')

if __name__ == '__main__':
    get_site_data()