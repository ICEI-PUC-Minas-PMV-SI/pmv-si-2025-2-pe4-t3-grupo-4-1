Com Docker Compose

docker compose up -d


Sem Docker Compose

python -m venv .venv

pip install -r requirements.txt

python manage.py migrate

python manage.py makemigrations

python manage.py runserver