import os

from flask import Flask
from flask import render_template
import psycopg2
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)


DEFAULT_IMAGE_URL = 'https://www.decolore.net/wp-content/uploads/2017/04/Free-Protein-Supplement-Powder-Packaging-Mockup-PSD.jpg'


@app.route('/<radio_id>')
def show_products(radio_id):
    records = get_products_ids(radio_id)
    products = []
    for product_id in records:
        product_data = get_product_data(product_id)
        products.append(product_data)
    return render_template(
        'base.html',
        products=products,
        radio_id=radio_id
    )


def get_connection():
    load_dotenv(dotenv_path='/home/leo/.deployment-config', override=True)

    db_name = os.getenv('DB_DATABASE')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_port = int(os.getenv('DB_PORT'))
    db_host = os.getenv('DB_HOST')

    return psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port)


def get_products_ids(radio_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('select e_prod_id from sandbox.tmp_hack_similarities where slugified = \'{}\' '
                   'order by cos_simil desc limit 5;'.format(radio_id))
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return [i[0] for i in records]


def get_product_data(product_id):
    product_url, product_name = get_product_url(product_id)
    image_url = get_image_from_page(product_url)
    if image_url is None:
        image_url = DEFAULT_IMAGE_URL
    product_data = {
        'product_id': product_id,
        'product_name': product_name,
        'image_url': image_url,
        'product_url': product_url
    }
    return product_data


def get_image_from_page(product_url):
    result = requests.get(product_url)
    soup = BeautifulSoup(result.text, features="html.parser")
    imgs = soup.find_all('img', class_='slider-img')
    if imgs:
        first_url = imgs[0].attrs['src']
        return first_url
    return None

def get_product_url(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f'''
        select "ProductURL", "productName" from datamarts."dimProduct" where "productId" = {product_id} and "labelId" = 1; 
    ''')
    product_url, product_name = cursor.fetchone()
    cursor.close()
    conn.close()
    return f'https://master.test.vakantieveilingen.nl/{product_url}', product_name

if __name__ == '__main__':
    app.run(debug=True)