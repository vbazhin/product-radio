from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/<int:radio_product_id>')
def show_products(radio_product_id):
    # Mock data. Request the API here.
    product_data = {
        'product_id': 'product id',
        'product_name': 'Mock product_name',
        'image_url': 'http://flask.pocoo.org/docs/1.0/_static/flask.png',
        'description': 'Mock description'
    }
    products = [product_data]*5
    # return 'Showing products for {}'.format(radio_product_id)
    return render_template(
        'base.html',
        products=products,
        radio_id=radio_product_id
   )

if __name__ == '__main__':
   app.run(debug=True)