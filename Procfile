release: python manage.py migrate
web: daphne mySite.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker --settings=mySite.settings -v2