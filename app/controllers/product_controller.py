from flask import request, jsonify
from bson import ObjectId
from flasgger import swag_from

from app.models.product_model import ProductModel
from app import mongo

product_model = ProductModel(mongo)

def create_product():
    data = request.json
    print('product--',data)
    product_data = {
        "img": data['img'],
        "title": data['Title'],
        "price": data['price'],
        "priceDisc": data['priceDiscount'],
        "category": data['category'],
        "description": data['description']
    }
    product_id = product_model.create(product_data)
    return jsonify({"message": "Product added successfully", "product_id": str(product_id)}), 201

def get_products():
    products = product_model.find({})
    if not products:
        return jsonify({'message': 'No Products found'}), 404
    
    for product in products:
        product['_id'] = str(product['_id'])
    
    return jsonify(products), 200

def get_product(product_id):
    product = product_model.find_one({'_id': ObjectId(product_id)})
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    product['_id'] = str(product['_id'])
    return jsonify(product), 200

def update_product(product_id):
    data = request.json
    product = product_model.find_one({'_id': ObjectId(product_id)})
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    product_data = {
        "img": data['img'],
        "title": data['Title'],
        "price": data['price'],
        "priceDisc": data['priceDiscount'],
        "category": data['category'],
        "description": data['description']
    }
    result = product_model.update({'_id': ObjectId(product_id)},product_data)
    
    if result.modified_count == 0:
        return jsonify({'error': 'Product update failed'}), 500
    
    return jsonify({'message': 'Product updated successfully'}), 200

def delete_product(product_id):
    result = product_model.delete({'_id': ObjectId(product_id)})
    if result.deleted_count == 0:
        return jsonify({'error': 'Product not found or delete failed'}), 404
    
    return jsonify({'message': 'Product deleted successfully'}), 200



