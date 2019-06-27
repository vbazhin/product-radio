from flask import Flask
from flask import render_template
import psycopg2


app = Flask(__name__)


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


def get_products_ids(radio_id):
    conn = psycopg2.connect(dbname='radio', user='radio', password='radio', host='127.0.0.1')
    cursor = conn.cursor()
    cursor.execute('select e_prod_id from "sandbox.tmp_hack_similarities" where r_prod_id = \'{}\' '
                   'order by cos_simil desc limit 5;'.format(radio_id))
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return [i[0] for i in records]


def get_product_data(product_id):
    # Mock method.
    # TODO: Must reequest the Hammer API.
    product_data = {
        'product_id': product_id,
        'product_name': 'Mock product_name',
        'image_url': 'http://flask.pocoo.org/docs/1.0/_static/flask.png',
        'description': 'Mock description'
    }
    return product_data


if __name__ == '__main__':
   app.run(debug=True)