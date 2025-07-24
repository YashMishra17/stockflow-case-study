from flask import Blueprint, request, jsonify
from app import db
from models import Product, Inventory, Warehouse, Sales, ProductThreshold, Supplier, ProductSupplier
from utils import get_avg_daily_sales
from decimal import Decimal
from datetime import datetime, timedelta

main = Blueprint('main', __name__)

@main.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()
    required = ['name', 'sku', 'price', 'warehouse_id', 'initial_quantity']
    for field in required:
        if field not in data:
            return {"error": f"Missing field: {field}"}, 400

    try:
        price = Decimal(str(data['price']))
    except:
        return {"error": "Invalid price format"}, 400

    if Product.query.filter_by(sku=data['sku']).first():
        return {"error": "SKU already exists"}, 409

    try:
        product = Product(name=data['name'], sku=data['sku'], price=price)
        db.session.add(product)
        db.session.flush()

        inventory = Inventory(product_id=product.id, warehouse_id=data['warehouse_id'], quantity=data['initial_quantity'])
        db.session.add(inventory)
        db.session.commit()

        return {"message": "Product created", "product_id": product.id}, 201
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

@main.route('/api/companies/<int:company_id>/alerts/low-stock')
def low_stock_alerts(company_id):
    cutoff = datetime.utcnow() - timedelta(days=30)
    recent_sales = db.session.query(Sales.product_id).join(Inventory).join(Warehouse)\
        .filter(Warehouse.company_id == company_id, Sales.sold_at >= cutoff).distinct().subquery()

    alerts = db.session.query(
        Product.id, Product.name, Product.sku, Warehouse.id.label("warehouse_id"),
        Warehouse.name.label("warehouse_name"), Inventory.quantity, ProductThreshold.threshold,
        Supplier.id.label("supplier_id"), Supplier.name.label("supplier_name"), Supplier.contact_email
    ).join(Inventory).join(Warehouse).join(ProductThreshold)\
     .join(ProductSupplier).join(Supplier)\
     .filter(Warehouse.company_id == company_id)\
     .filter(Product.id.in_(recent_sales))\
     .filter(Inventory.quantity < ProductThreshold.threshold).all()

    result = {"alerts": [], "total_alerts": 0}

    for a in alerts:
        avg_sales = get_avg_daily_sales(a.id, a.warehouse_id)
        days_left = int(a.quantity / avg_sales) if avg_sales else None

        result["alerts"].append({
            "product_id": a.id,
            "product_name": a.name,
            "sku": a.sku,
            "warehouse_id": a.warehouse_id,
            "warehouse_name": a.warehouse_name,
            "current_stock": a.quantity,
            "threshold": a.threshold,
            "days_until_stockout": days_left,
            "supplier": {
                "id": a.supplier_id,
                "name": a.supplier_name,
                "contact_email": a.contact_email
            }
        })

    result["total_alerts"] = len(result["alerts"])
    return jsonify(result)
