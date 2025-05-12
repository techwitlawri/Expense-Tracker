# 📊 Expense Tracker
Welcome to my **Expense Tracker**, a web app that helps users track and manage their daily spending, 
with user authentication, category-based expense tracking, and visual spending reports.  
This is part of my journey as an aspiring backend developer. 

**Live demo**: https://expense-tracker-kvgt.onrender.com

**GitHub Repo**: [Expense Tracker] https://github.com/techwitlawri/Expense-Tracker
____________________________________________________________________________________
## 💡 Project Overview

This project allows users to:
- Sign up and log in
- Add, update, and delete expenses
- Assign categories to spending
- View timestamps for each entry

It was built using **Python (Flask)** with **SQLAlchemy** for database management, and deployed via **Render**.

 ## Features
 
- User Registration & Login

- Add, Edit, Delete Expenses

- Track Spending by Category

- Reports with Chart Visualizations

- Currency Selection Based on Country

- Clean and Responsive UI


 ## Tech Stack
 
 **Backend**: Python, Flask, SQLAlchemy

**Database**: PostgreSQL (Render Free Tier)

**Frontend**: HTML, CSS (Bootstrap), Jinja2 Templates

**Authentication**: Flask-Login

**Deployment**: Render
________________________________________________________________________
## Project Structure

expense-tracker/

│

├── app/

│ 
├── __init__.py

│ ├── models.py

│ ├── routes.py

│  ├── expenses.py                           


│ ├── auth.py                                 


│ └── templates/

│

├── static/

│

├── run.py

├── config.py

├── requirements.txt

└── .env
_________________________________________________________________________
## Installation (For Local Development)
  1. **Clone the repo**

  '''bash

git clone https://github.com/techwitlawri/Expense-Tracker.git

cd Expense-Tracker
___________________________________________________________________________
  2. **Create a virtual environment & activate it**

python -m venv venv

.\venv\Scripts\activate 
_____________________________________________________________________________
  3. **Install dependencies:**

pip install -r requirements.txt
_____________________________________________________________________________
  4. **Run locally (using SQLite):**

 run.py
 ___________________________________________________________________________________
 login page.
 ![login](https://github.com/user-attachments/assets/a595b662-6591-43d9-8fc9-f2eb3e0eb63f)

 __________________________________________________________________________________________
 dashboard page
 
![dashboard](https://github.com/user-attachments/assets/db1e7b41-9593-4967-b471-4ec384b619de)
______________________________________________________________________________________________
Report page



_________![report](https://github.com/user-attachments/assets/d9a20f06-0954-49be-98c7-ae52900ccd32)
______________________________________________________________________
### Testing
To run the tests for the project, you can use pytest. 
If you don’t have pytest installed, you can install it using:


pip install pytest
______________________________________________________________

to run the test:

pytest

### Test Configuration


The tests are configured to use an in-memory SQLite database for quick setup and teardown during tests.
_________________________________________________________________________
### About Me


Hi! I’m Mmachi, an aspiring backend developer based in the UK, 
passionate about building real-world projects with Python.
I’m continuously learning and open to opportunities or feedback.
____________________________________________________________________________
**Contact**

Feel free to reach out via LinkedIn or GitHub if you have feedback or want to collaborate.

Linkedin -  www.linkedin.com/in/mmachi-ezeh-3a77a21b2
_____________________________________________________________________________________
 **Contributing**
 
Contributions are welcome! Feel free to fork the repo and submit a pull request.
_________________________________________________________________________________
**License**
This project is licensed under the MIT License — see the LICENSE file for details.






