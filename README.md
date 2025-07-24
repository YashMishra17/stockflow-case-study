#  StockFlow Case Study – B2B Inventory Management (Python + Flask)

This repository contains my technical solution for the **StockFlow Case Study**, which evaluates backend system design skills for a B2B SaaS inventory management platform.

---

##  Case Study Breakdown

The case study was divided into **3 parts**:

### 1.  Code Review & Debugging
- Identified issues like duplicate SKUs, lack of atomic transactions, and poor validation.
- Rewrote the product creation logic to ensure data consistency and better error handling.

### 2.  Database Design
- Designed scalable schema with products, inventory, suppliers, bundles, and history tracking.
- Used composite keys, indexes, and normalized relations for performance and maintainability.

### 3.  API Implementation
- Built a `/low-stock` alert API that:
  - Considers product-level thresholds
  - Filters only products with recent sales
  - Returns supplier contact info and days until stockout

---

## 🧪 How to Run This Project Locally

> 💡 This assumes Python 3.10+ and pip are installed.

### 1. Clone the repo
bash
git clone https://github.com/your-username/stockflow-case-study.git
cd stockflow-case-study

### 2.Set up a virtual environment
python -m venv venv

### 3.Activate the environment
venv\Scripts\activate.bat













### 4.Install dependencies
pip install -r requirements.txt

### 5.Run the Flask app
flask run

