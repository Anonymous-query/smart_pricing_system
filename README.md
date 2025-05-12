
# 🛒 Dynamic Pricing and Discount System

## 📌 Objective

This project is developed to simulate a dynamic pricing and discount system. It uses object-oriented programming principles (inheritance, polymorphism) and exposes the functionality via a RESTful API using Django and Django REST Framework.

---

## 🧠 Project Overview

The system supports different types of products and discounts, calculating prices dynamically depending on season, quantity, or product type. It also supports managing customer orders and applying multiple discounts with conflict resolution based on priority.


## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Anonymous-query/smart_pricing_system.git
cd smart_pricing_system
```

### 2. Create Virtual Environment

```bash
python3.12 -m venv pricing_system_env
source pricing_system_env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Load Sample Data

```bash
python scripts/populate_test_data.py
```

### 6. Run the Server

```bash
python manage.py runserver
```

---

## 🔌 RESTful API Usage via Postman

A ready-to-use Postman collection is provided to test all API endpoints.

### 📁 File
**Smart_Pricing_System_postman_collection.json**

### 🚀 How to Use

1. Open [Postman](https://www.postman.com/downloads/).
2. Click on **Import** in the top-left corner.
3. Select **File**, then browse and choose `Smart_Pricing_System_postman_collection.json`.
4. Click **Import**.

---

## 🧪 Testing (Optional but Recommended)

Wrote unit tests for:

- Product logic
- Discount logic
- Order total logic

Run them using:

```bash
pytest
```

## 🧑‍💻 Author: Nilesh

Developed for **Dynamic Pricing and Discount System**  
Language: Python 3.12.3

---

## 📬 Contact

For issues or suggestions, please create an issue or pull request on the GitHub repository.
