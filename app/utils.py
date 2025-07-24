from . import db
from .models import Sales
from datetime import datetime, timedelta

def get_avg_daily_sales(product_id, warehouse_id, last_days=30):
    since = datetime.utcnow() - timedelta(days=last_days)
    total = db.session.query(db.func.sum(Sales.quantity))\
        .filter(Sales.product_id == product_id, Sales.sold_at >= since)\
        .scalar()
    return (total or 0) / last_days
