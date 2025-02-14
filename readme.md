# Google Sheets API with Django Rest Framework

This project provides a RESTful API to interact with Google Sheets. It allows authenticated users to read and write data to Google Sheets dynamically.

## Features
- ✅ Read data from a Google Sheet
- ✅ Write data to a Google Sheet
- ✅ Automatic sheet creation if it does not exist

## Prerequisites

Ensure you have the following installed:
- Python 3.8+
- Django & Django REST Framework
- Google API Client
- Dotenv for environment variable management

## Installation

1. Clone the repository:
   ```sh
  git clone  https://github.com/shariqsajad88/generic_view.git
   ```

2. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate 
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up `.env` file with the following content:
   ```ini
   GOOGLE_SHEETS_CREDENTIALS=path/to/your/service-account.json
   GOOGLE_SHEET_ID=your-google-sheet-id
   ```

5. Apply migrations:
   ```sh
   python manage.py migrate
   ```

6. Create a superuser (optional for admin access):
   ```sh
   python manage.py createsuperuser
   ```

7. Run the server:
   ```sh
   python manage.py runserver
   ```


