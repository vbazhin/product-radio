from flask import Flask
app = Flask(__name__)

@app.route('/<int:radio_product_id>')
def show_products(radio_product_id):
    return 'Showing products for {}'.format(radio_product_id)

if __name__ == '__main__':
   app.run(debug=True)