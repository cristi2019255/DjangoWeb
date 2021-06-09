web: daphne -p $PORT -b 0.0.0.0 my_config.asgi:application
worker: celery worker --app=my_config.celery.app -l DEBUG