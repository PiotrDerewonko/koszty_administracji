#!/bin/bash

# Wykonaj migracje Django
echo "Wykonywanie migracji Django..."
python manage.py migrate

# Załaduj dane z pliku db.json
echo "Ładowanie danych z db.json..."
python manage.py loaddata /app/db.json

# Uruchom serwer Django
echo "Uruchamianie serwera Django..."
python manage.py runserver 0.0.0.0:8000 &

# Uruchom Streamlit
echo "Uruchamianie aplikacji Streamlit..."
streamlit run /app/reports/main.py --server.address=0.0.0.0
