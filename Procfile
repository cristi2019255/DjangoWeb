web: daphne -p $PORT -b 0.0.0.0 mySite.asgi:application
worker: celery worker --app=mySite.celery.app -l DEBUG