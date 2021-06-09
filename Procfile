release: python manage.py migrate
web: daphne mySite.asgi:application --port 8000 --bind 0.0.0.0
worker: python manage.py runworker channel_layer