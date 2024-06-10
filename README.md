1 - pip install -r requirements.txt
2 - .env:
SECRET_KEY='django-insecure-ktgynhv!)84(qff(hqq5mqisb)6p)eegb&ed7o$xb7z@vbcq6@'
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=test_samirk
DB_USER=postgres
DB_PASS= your_password
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
3 - python manage.py makimigrations
4 - python manage.py migrate
4 - python manage.py runserver 
