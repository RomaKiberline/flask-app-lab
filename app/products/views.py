from flask import render_template
from app.products import products_bp

@products_bp.route('/')
def list_products():
    products = ["Ноутбук", "Телефон", "Навушники"]
    return render_template('products/product.html', products=products)
