python manage.py collectstatic --noinput
gunicorn etf.wsgi --bind=0.0.0.0