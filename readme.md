# Public Website

[https://cinemacousas.braudelserveur.com](https://cinemacousas.braudelserveur.com)

# 🛠️ Setup Instructions

## 📦 Install Python 3.12 (very important)

## 📦 Install Dependencies

### 💻 macOS / Linux Users

```bash
python3 -m venv ADMIN/.venv && ADMIN/.venv/bin/pip install Flask==3.0.0 Flask-CORS==4.0.0 mysql-connector-python==8.2.0 python-dotenv==1.0.0 && python3 -m venv USER/.venv && USER/.venv/bin/pip install Flask==3.0.0 mysql-connector-python==8.2.0 Werkzeug==3.0.1 python-dotenv==1.0.0 APScheduler==3.10.4 email-validator==2.1.0 reportlab==4.0.4 Pillow==10.1.0
```

### 🪟 Windows Users

```powershell
python -m venv ADMIN\.venv; ADMIN\.venv\Scripts\pip install Flask==3.0.0 Flask-CORS==4.0.0 mysql-connector-python==8.2.0 python-dotenv==1.0.0; python -m venv USER\.venv; USER\.venv\Scripts\pip install Flask==3.0.0 mysql-connector-python==8.2.0 Werkzeug==3.0.1 python-dotenv==1.0.0 APScheduler==3.10.4 email-validator==2.1.0 reportlab==4.0.4 Pillow==10.1.0
```

---

## 🚀 Launch Websites

### ▶️ Launch Admin Website

* **macOS / Linux :**

```bash
ADMIN/.venv/bin/python3 ADMIN/server_admin.py
```

* **Windows:**

```powershell
ADMIN\.venv\Scripts\python ADMIN\server_admin.py
```

---

### ▶️ Launch User Website

* **macOS / Linux:**

```bash
USER/.venv/bin/python3 USER/app.py
```

* **Windows:**

```powershell
USER\.venv\Scripts\python USER\app.py
```# 🛠️ Setup Instructions

## 📦 Install Python 3.12 (very important)

## 📦 Install Dependencies

### 💻 macOS / Linux Users

```bash
python3 -m venv ADMIN/.venv && ADMIN/.venv/bin/pip install Flask==3.0.0 Flask-CORS==4.0.0 mysql-connector-python==8.2.0 python-dotenv==1.0.0 && python3 -m venv USER/.venv && USER/.venv/bin/pip install Flask==3.0.0 mysql-connector-python==8.2.0 Werkzeug==3.0.1 python-dotenv==1.0.0 APScheduler==3.10.4 email-validator==2.1.0 reportlab==4.0.4 Pillow==10.1.0
```

### 🪟 Windows Users

```powershell
python -m venv ADMIN\.venv; ADMIN\.venv\Scripts\pip install Flask==3.0.0 Flask-CORS==4.0.0 mysql-connector-python==8.2.0 python-dotenv==1.0.0; python -m venv USER\.venv; USER\.venv\Scripts\pip install Flask==3.0.0 mysql-connector-python==8.2.0 Werkzeug==3.0.1 python-dotenv==1.0.0 APScheduler==3.10.4 email-validator==2.1.0 reportlab==4.0.4 Pillow==10.1.0
```

---

## 🚀 Launch Websites

### ▶️ Launch Admin Website

* **macOS / Linux :**

```bash
ADMIN/.venv/bin/python3 ADMIN/server_admin.py
```

* **Windows:**

```powershell
ADMIN\.venv\Scripts\python ADMIN\server_admin.py
```

---

### ▶️ Launch User Website

* **macOS / Linux:**

```bash
USER/.venv/bin/python3 USER/app.py
```

* **Windows:**