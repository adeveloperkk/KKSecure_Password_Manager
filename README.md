
# 🔐 Django Password Manager – Norton Clone

A secure and modern **Password Manager** web application built with **Django**, inspired by **Norton Password Manager**. This project allows users to generate, store, and manage their credentials securely using advanced encryption and a responsive, user-friendly UI.

---

## 📸 Demo

> *Add your screenshots or a GIF demo here*

![Login Page]![image](https://github.com/user-attachments/assets/ed46154f-fd93-484c-aa34-bace84895082)


![Vault Dashboard]![image]([https://github.com/user-attachments/assets/2db1299c-41e1-46a4-8b70-c59cb16f0a5f])

![image](https://github.com/user-attachments/assets/55c6b0bd-28cb-4b62-a4af-7dfed108d8a9)

![Screenshot 2025-06-24 143127](https://github.com/user-attachments/assets/8b03405b-cee2-4fd3-8a00-9ac663222732)

![Screenshot 2025-06-24 143702](https://github.com/user-attachments/assets/e55a1b5e-0977-470b-961c-3a57f8efcd62)

![image](https://github.com/user-attachments/assets/92bad8b9-7999-4cfd-806e-b08691d360f8)

![image](https://github.com/user-attachments/assets/dacca035-6d1a-42e8-bbcf-c311d39e57c4)

![image](https://github.com/user-attachments/assets/3265e5a9-a181-4909-9d04-f9c75cdb4c7a)

![image](https://github.com/user-attachments/assets/3584e94c-8b1a-4aba-8a98-b726bb8550fc)


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
