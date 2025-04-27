from encodings import utf_16
from bs4 import BeautifulSoup
import requests
import sqlite3

connection = sqlite3.connect('database_cocktail.db')
cursor = connection.cursor()
cursor.execute(''' create table if not exists cocktail (
id integer primary key,
name text unique
)
''')
cursor.execute(''' create table if not exists ingredient (
id integer primary key,
name text unique
)
''')
cursor.execute(''' create table if not exists cocktail_ingredient (
cocktail_id integer,
ingredient_id integer,
amount text,
unit text 
)
''')

url = 'https://ru.inshaker.com/collections/150-alkogolnye-kokteyli?page=56'
headers = {
    "Accept": "*/*", "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }
req = requests.get(url, headers=headers)
src = req.text
soup = BeautifulSoup(src, 'lxml')
all_cocktails_href = soup.find_all('a', class_ = 'cocktail-item-preview')
count = 0

for item in all_cocktails_href:
    
        cocktail_href = 'https://ru.inshaker.com' + item.get('href')
        req = requests.get(cocktail_href, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        cocktail_name = soup.find('em').text
        rating_cocktail = soup.find('span', class_ = 'present total')
        all_cocktail_ing = soup.find('div', class_='ingredient-tables').find('table').find_all("tr")
        print(cocktail_name)
        print("Cocktail rating:", rating_cocktail.text)
        cursor.execute(' insert or ignore into cocktail (name) values (?) ', (cocktail_name, ))
        cursor.execute(' select id from cocktail where name = ?', (cocktail_name, ))
        cocktail_id = cursor.fetchone()
        for ing in  all_cocktail_ing[1:]:
           
                ing_name = ing.find('td', class_ = 'name').find('a').text
                ing_amount = ing.find('td', class_ = 'amount').text
                ing_unit = ing.find('td', class_ = 'unit').text
                cursor.execute(' insert or ignore into ingredient (name) values (?)', (ing_name, ))
                cursor.execute(' select id from ingredient where name = ?', (ing_name, ))
                ing_id = cursor.fetchone()
                cursor.execute('insert into cocktail_ingredient (cocktail_id, ingredient_id, amount, unit) values (?, ?, ?, ?)', (cocktail_id[0], ing_id[0], ing_amount, ing_unit, ))
                
                print(ing_name, ing_amount, ing_unit)
        connection.commit()
        print('-'*20)
 
    
connection.commit()
connection.close()


