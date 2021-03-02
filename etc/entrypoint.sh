#!/bin/sh
python manage.py flush --no-input
python manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@api.com', 'admin')" | python manage.py shell
exec "$@"