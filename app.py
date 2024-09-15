from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Configurations for the database - sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init SQLAlchemy
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    category = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Product {self.id}'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'category': self.category
        }
    




@app.route('/addAllProducts', methods=['POST'])
def addAll ():
    products = request.json # analoguely products could be loaded from a file 

    # constructing a list of products
    productsList = []

    for i, dat in enumerate(products):
        new_product = Product(name = products[i]['name'],
                        price = products[i]['price'],
                        description = products[i]['description'],
                        category = products[i]['category'])
        productsList.append(new_product)

    db.session.add_all(productsList)
    db.session.commit()

    return "successful products addition", 201






@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.json
    new_product = Product(name = data['name'],
                          price = data['price'],
                          description = data['description'],
                          category = data['category'])
    db.session.add(new_product)
    db.session.commit()
    return "successful product addition", 201



@app.route('/present_products', methods = ['GET'])
def send_products():
    list_to_send = []
    allProducts = Product.query.all()
    
    for product in allProducts:
        list_to_send.append({'id': product.id, 'name' : product.name, 'price' : product.price, 'description' : product.description, 'category' : product.category})
    list_to_send   

    return list_to_send



@app.route('/present_product_by_id/<int:id>', methods = ['GET'])
def productByID(id):
    product_by_id = Product.query.get(id)
    return product_by_id.to_dict()



@app.route('/update_product/<int:id>', methods = ['POST'])
def updateProduct(id):
    data = request.json
    product = Product.query.get(id)
    if(product):
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.description = data.get('description', product.description)
        product.category = data.get('category', product.category)
        db.session.commit()
        return "Great Success!"
    else:
        return "Great failure!"




@app.route('/delete_product/<int:id>', methods = ['POST'])
def deleteProduct(id):
    product = Product.query.get(id)
    if(product):
        db.session.delete(product)
        db.session.commit()
        return "Great Success!"
    else:
        return "Great failure!"
    




if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)



