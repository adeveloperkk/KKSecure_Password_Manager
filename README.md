
# 🔐 Django Password Manager – Norton Clone

A secure and modern **Password Manager** web application built with **Django**, inspired by **Norton Password Manager**. This project allows users to generate, store, and manage their credentials securely using advanced encryption and a responsive, user-friendly UI.

---

## 📸 Demo

> *Add your screenshots or a GIF demo here*

![Login Page](https://your-screenshot-link.com/login.png)
![Vault Dashboard](https://your-screenshot-link.com/vault.png)

---

## 🚀 Features

- ✅ Secure user authentication (Django built-in auth)
- 🔒 AES encryption for stored passwords
- 📁 Vault to manage saved credentials
- ➕ Add / ✏️ Edit / ❌ Delete password entries
- 🧠 Password strength indicator
- 🔐 Built-in password generator
- 📱 Fully responsive frontend
- 🛠 Admin dashboard (Django Admin)

---

## 🛠 Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Database**: SQLite (default), PostgreSQL (optional)
- **Security**: AES encryption, Django CSRF & session protection

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/adeveloperkk/Django-Password-Manager-Norton-Clone.git
   cd Django-Password-Manager-Norton-Clone
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate
   # On Windows:
   # env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory and add:
   ```ini
   SECRET_KEY=your-django-secret-key
   DEBUG=True
   ```

5. **Apply migrations & run the server**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

---

## 🧪 Features to Improve (Future Scope)

- 🔁 Two-Factor / Multi-Factor Authentication (2FA / MFA)
- 📱 PWA version for mobile access
- ☁️ Cloud backup & synchronization
- 🔎 Vault search functionality
- 📩 Email-based account recovery
- 🧾 Export/import passwords (CSV / JSON)

---

## 🤝 Contributing

Pull requests are welcome! To contribute:

1. Fork the repository  
2. Create a new branch  
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit  
4. Push and open a pull request

---

## 🛡️ Disclaimer

This application is intended for educational and demo purposes only. Do not use it in production or store sensitive real-world credentials unless fully audited for security.

---

## 📬 Contact

**Developer:** Krishnaveer Singh (DeveloperKK)  
**Email:** [info@developerkk.in](mailto:info@developerkk.in)  
**GitHub:** [@adeveloperkk](https://github.com/adeveloperkk)
