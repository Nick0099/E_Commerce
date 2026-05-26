# 🛒 E-Commerce API

A production-grade REST API backend for an e-commerce platform built with Django and Django REST Framework.

[![CI](https://github.com/Nick0099/E_Commerce/actions/workflows/django.yml/badge.svg)](https://github.com/Nick0099/E_Commerce/actions)

---

## 🚀 Live Demo

- **API Docs:** coming soon on Render
- **Frontend:** [ecommerce-frontend](https://github.com/Nick0099/ecommerce-frontend)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, Django |
| API | Django REST Framework |
| Auth | JWT (simplejwt) + token blacklisting |
| Database | PostgreSQL (prod), SQLite (dev) |
| Images | Pillow |
| API Docs | drf-spectacular (Swagger) |
| Testing | pytest — 35 tests passing |
| Container | Docker + docker-compose |
| CI/CD | GitHub Actions |
| Deployment | Render |

---

## 📂 Project Structure
ecommerce/
├── users/        # Custom user model, JWT auth, profile
├── products/     # Products, categories, custom permissions
├── cart/         # Shopping cart — add, update, remove, clear
├── reviews/      # Product reviews, signals for avg_rating
├── orders/       # Checkout, order history, cancel, stock management
├── wishlist/     # Save products for later, toggle add/remove
├── coupons/      # Discount codes — percentage or fixed amount
└── e_commerce/   # Project settings, urls, wsgi

---

## 🔑 Key Features

- **JWT Authentication** — register, login, logout with token blacklisting and auto refresh
- **Custom User Model** — email-based login, seller/buyer roles
- **Products** — CRUD with category filtering, search, pagination, custom seller permissions
- **Shopping Cart** — add, update quantity, remove items, stock validation
- **Orders** — checkout with stock deduction, order history, cancel with stock restore
- **Reviews** — one review per product per user, signals auto-update avg rating
- **Wishlist** — toggle add/remove
- **Coupons** — percentage and fixed discount, expiry and usage limit validation
- **Async Emails** — order confirmation sent in background thread
- **Race Condition Protection** — select_for_update() on checkout
- **Swagger Docs** — full API documentation at /api/docs/

---

## 📡 API Endpoints
POST   /api/auth/register/
POST   /api/auth/login/
POST   /api/auth/logout/
GET    /api/auth/profile/
GET    /api/products/
POST   /api/products/create/
GET    /api/products/<id>/
GET    /api/products/<id>/reviews/
POST   /api/products/<id>/reviews/add/
POST   /api/cart/add/
GET    /api/cart/
DELETE /api/cart/
PUT    /api/cart/<id>/
DELETE /api/cart/<id>/
POST   /api/orders/checkout/
GET    /api/orders/
GET    /api/orders/<id>/
POST   /api/orders/<id>/cancel/
GET    /api/wishlist/
POST   /api/wishlist/toggle/
POST   /api/coupons/validate/
GET    /api/docs/

---

## 🏃 Running Locally

**1. Clone the repo**
```bash
git clone https://github.com/Nick0099/E_Commerce.git
cd E_Commerce
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run migrations**
```bash
python manage.py migrate
python manage.py createsuperuser
```

**4. Start the server**
```bash
python manage.py runserver
```

**5. Visit API docs**

http://localhost:8000/api/docs/

---

## 🐳 Running with Docker

```bash
docker-compose up --build
docker-compose exec web python manage.py createsuperuser
```

---

## 🧪 Running Tests

```bash
pytest --tb=short
```

35 tests across users, products, cart, orders and coupons.

---

## 🔧 Environment Variables

| Key | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | True/False |
| `DATABASE_URL` | PostgreSQL connection URL |

---

## 📬 Contact

Nischal Neupane — nischalneupane45@gmail.com

[![GitHub](https://img.shields.io/badge/GitHub-Nick0099-181717?style=flat&logo=github)](https://github.com/Nick0099)
