# Budgeta - A Full Stack Expense Management Project Using Django Framework and Deployed in PythonAnyWhere.

## Introduction
Budgeta is a robust expense management system built with Django and Docker, designed to help users efficiently track, manage, and analyze their financial expenses. The application provides a user-friendly interface for logging daily expenses, categorizing them, and viewing detailed expense summaries. The project is containerized using Docker, ensuring consistent deployment and easy scalability across different environments.

## Deployed URL
[https://bharath121.pythonanywhere.com](https://bharath121.pythonanywhere.com/)

## Features
- **Django Framework Integration**: Secure user authentication and registration.
- **Static Files Handling**: Proper configuration for serving static files using Whitenoise.
- **Automated Superuser Creation**: Simplified superuser setup during deployment.
- **Expense Management**:
  - Add, edit, and delete expenses with descriptions, categories, and payment status.
  - Filter expenses by month and year.
  - View monthly and yearly expense summaries.

## Prerequisites

- Python 3.12+
- Django 5.0.7+
- whitenoise 6.7.0
- gunicorn 22.0.0
- Git

## Future Improvements
- Integrating AI Chatbot for easy access.
- Integrating Machine Learning predictions for future expenses.
- Enhanced analytics for expense tracking.
- Multi-user support with role-based access control.

## Usage
### Setting Up Locally

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mbharath246/budgeta.git
   cd budgeta
   ```
2. **Create and activate a virtual environment:**
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```
3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    Optional: (install docker)
    ```
    [https://docs.docker.com/desktop/setup/install/windows-install/](https://docs.docker.com/desktop/setup/install/windows-install/)
    

4. **Run the development server:**
    ```bash
    Windows: python manage.py runserver
          (or)
    Docker : docker compose up
    
    http://127.0.0.1:8000/
    ```
5. **Additional Steps**
    - Create User
    - Add daily expenses.
    - Manage monthly expenses.
    - Check Filters for which part is spending more.

## Screenshots
- **Login Page**
![image](https://github.com/user-attachments/assets/8d421a57-d9ad-4841-acb7-eb5969cb8a31)
    
- **Register Page:**
![image](https://github.com/user-attachments/assets/c4ba8c6d-72f5-4529-b375-d680d3426af1)

- **Home Page**
![image](https://github.com/user-attachments/assets/b8df27f4-0263-4ab7-8d52-9972b57dd1b1)

- **Add Expenses**
![image](https://github.com/user-attachments/assets/aa0887b0-a7d0-414b-a673-0f62a56603b0)

- **Add By Category**
![image](https://github.com/user-attachments/assets/e303c4f9-6ea3-4a7b-a739-2ac8007fbc76)

- **Add By Payment Type**
![image](https://github.com/user-attachments/assets/a5510bb5-28f6-4cde-8788-d38e3786b297)

- **Monthly Spending**
![image](https://github.com/user-attachments/assets/429186c1-7c7c-4961-b6f8-4adf624c9cd3)

- **Yearly Spending**
![image](https://github.com/user-attachments/assets/babbec2f-2774-48fb-9859-48e5a82e55ef)

- **Edit Expense**
![image](https://github.com/user-attachments/assets/d11e0b00-83a0-4f61-a680-bc3da8c84261)

- **Delete Expense**
![image](https://github.com/user-attachments/assets/b10e95c8-7139-4926-b6cf-fbe30a7af731)

- **Filters**
![image](https://github.com/user-attachments/assets/fd02f117-e93a-4d4f-862b-394806c351dc)
