release: python manage.py makemigrations account && python manage.py migrate account &&  python manage.py makemigrations && python manage.py migrate
web: gunicorn config.wsgi:application
