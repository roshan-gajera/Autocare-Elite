# 🚗 AutoCare Pro — Car Maintenance & Towing Management System

A multi-role Django web platform connecting vehicle owners with local service shops for scheduled maintenance bookings and emergency towing — with online payments, OTP-based confirmation, and dedicated dashboards for clients, service providers, and super admins.

**Tech Stack:** Django · MySQL · Stripe · HTML/CSS (server-rendered templates)

---

## ✨ Features

### For Clients
- 🔐 Account registration & login
- 🏪 Select a preferred service shop
- 🛠️ Browse and book maintenance services (oil change, repairs, etc.)
- 🚛 Request emergency towing with live pickup address & coordinates
- 💳 Pay online via Stripe or choose cash-on-service
- 🔑 OTP-based booking/towing confirmation
- 📩 Contact shops directly with inquiries
- 📖 Read shop blog posts and updates

### For Service Shops (Admin Panel)
- 📊 Fleet performance dashboard — live counts for orders, service requests, tow requests, and messages
- 🧾 Manage service listings (add/edit/delete offerings & pricing)
- 📦 View and update service order & towing order statuses
- 💬 Inbox for customer messages
- 👤 Shop profile management

### For Super Admin
- 🏢 Onboard and manage service providers
- 📋 Platform-wide visibility into services and towing activity

---

## 🏗️ Architecture

The project is split into five Django apps, each scoped to a specific role or concern:

```
car-maintence-system/
├── car_maintenance/       # Project settings & root URL config
├── core/                  # Shared authentication (signup, login, logout)
├── portal/                # Client-facing: bookings, towing, blog, payments, OTP
├── servicesite/           # Service shop admin dashboard & profile
├── superAdmin/            # Platform-level admin (manage providers)
├── maintenance/           # Client dashboard & shop selection
├── templates/             # Server-rendered HTML templates (per app)
└── static/                # CSS assets
```

**Key models:**
- `adminProfile` (servicesite) — service shop profile (name, address, contact)
- `selectShop` (maintenance) — links a client to their chosen shop
- `ServiceOffering`, `ServiceBooking` (portal) — services & bookings, with Stripe payment tracking and OTP confirmation
- `TowingRequest` (portal) — towing requests with GPS coordinates, status tracking, and OTP verification
- `BlogPost`, `ContactMessage` (portal) — shop content & customer inquiries

---

## 🔑 Authentication & Roles

Role separation is handled through Django's built-in `is_staff` / `is_superuser` flags combined with a custom `user_required` decorator (`portal/decorators.py`) that restricts client-only views to regular (non-staff) users. On login, users are redirected to the appropriate dashboard based on their role.

---

## 💳 Payments & OTP Flow

1. Client selects services and chooses **Pay Online** or **Cash on Service**.
2. For online payments, a Stripe `PaymentIntent` is created server-side and the client completes payment via Stripe's hosted checkout.
3. On successful payment, the backend re-verifies the payment status directly with Stripe's API before marking the booking as paid.
4. A 6-digit OTP is generated and shown to the client to confirm the booking/towing job in person with the service provider.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- MySQL Server
- A Stripe account (test mode keys are fine for local development)

### 1. Clone the repository
```bash
git clone https://github.com/roshan-gajera/Autocare-Elite.git
cd car-maintence-system
```

### 2. Set up a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install django python-decouple mysqlclient stripe
```
> 💡 Recommended: freeze these into a `requirements.txt` with `pip freeze > requirements.txt` for easier setup on other machines.

### 4. Configure environment variables
Create a `.env` file in the project root with :
```env
SECRET_KEY=your-django-secret-key
DEBUG=True
NAME=your-mysql-db-name
USER=your-mysql-username
PASSWORD=your-mysql-password
PORT=3306
STRIPE_PUBLIC_KEY=pk_test_xxxxxxxxxxxx
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxx
```

### 5. Create the MySQL database
```sql
CREATE DATABASE your_mysql_db_name;
```

### 6. Run migrations & start the server
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Visit `http://localhost:8000`

---

## 🧭 Known Limitations & Roadmap

- [ ] **Data isolation:** booking, towing, and message list views currently return all records rather than filtering by the logged-in user/shop — needs a `filter(user=request.user)` fix
- [ ] Add `requirements.txt` for dependency management
- [ ] Remove committed `__pycache__` files (`git rm -r --cached **/__pycache__`)
- [ ] Implement actual password reset logic (currently a static page)
- [ ] Add automated tests for booking, towing, and payment flows
- [ ] Add pagination for admin dashboard lists as data grows
- [ ] Migrate to Stripe webhooks for payment confirmation instead of client-triggered verification

---

## ⚠️ Disclaimer

This project was built as an academic minor project for learning purposes. Stripe integration runs in **test mode** — no real payments are processed.

---

## 👤 Author

**Roshan Gajera**
M.Sc. IT, Silver Oak University, Ahmedabad
- GitHub: [@roshan-gajera](https://github.com/roshan-gajera)
- LinkedIn: [Roshan-Gajera](https://www.linkedin.com/in/roshan-gajera-10aa72332/)