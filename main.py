from bs4 import BeautifulSoup

import csv
import requests
import os

def main():

    print("Start IPhone scrape..")
    
    with open('iphones.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',', lineterminator='\n')

        writer.writerow(["Name", "Short description", "Last price", "New price", "Image name"])

        for num in range(1, 30):
            url = f'https://darwin.md/ru/telefoane/smartphone/apple-iphone?brand%5B3%5D%5B%5D=apple&page={num}'
            content = requests.get(url)
            soup = BeautifulSoup(content.text, 'html.parser')

            cards = soup.find_all(class_='col-6 col-md-4 col-lg-3 night-mode')

            for card in cards:
                name = card.find(class_='d-block mb-2 ga-item')['title']
                descr = get_text(card, 'specification d-block')
                last_price = get_text(card, 'last-price')
                price = get_text(card, 'price-new')
                
                image_url = card.find(class_='card-image')['src']
                image_data = requests.get(image_url).content

                # Extracting the name from the URL to create a proper image filename
                image_name = image_url.split('/')[-1].split('.')[0]
                image_path = os.path.join('iphone_images', f'image{image_name}.jpg')

                with open(image_path, 'wb') as handler:
                    handler.write(image_data)

                writer.writerow([name, descr, last_price, price, f'{image_name}.jpg'])
        else:
            print("All IPhones parsed!")

    print("Start Phones scrape..")
    
    with open('phones.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',', lineterminator='\n')

        writer.writerow(['Name', 'Short description', 'Last price', 'New price', 'Image name'])

        for num in range(1, 110):
            url = f'https://darwin.md/ru/telefoane?page={num}'
            content = requests.get(url)
            soup = BeautifulSoup(content.text, 'html.parser')

            cards = soup.find_all(class_='col-6 col-md-4 col-lg-3 night-mode')

            for card in cards:
                name = card.find(class_='d-block mb-2 ga-item')['title']
                descr = get_text(card, 'specification d-block')
                last_price = get_text(card, 'last-price')
                price = get_text(card, 'price-new')

                image_url = card.find(class_='card-image')['src']
                image_data = requests.get(image_url).content

                # Extracting the name from the URL to create a proper image filename
                image_name = image_url.split('/')[-1].split('.')[0]
                image_path = os.path.join('phone_images', f'image{image_name}.jpg')

                with open(image_path, 'wb') as handler:
                    handler.write(image_data)

                writer.writerow([name, descr, last_price, price])
        else:
            print("All Phones parsed!")
        

def get_text(object, _class):
    element = object.find(class_=_class)
    return element.text.strip() if element else 'None'

if __name__ == "__main__":
    main()