Com Docker Compose

docker compose up -d

Sem Docker Compose

python -m venv .venv

pip install -r requirements.txt

python manage.py migrate

python manage.py makemigrations

python manage.py createsuperuser

python manage.py runserver





## Executar o job localmente
python manage.py crontab add

python manage.py crontab show
o retorno do comando acima é esse: c79761ab81ac3ff73e3857bc3f50585e -> ('*/30 * * * *', 'api.tasks.export_data_to_power_bi')

pegue o uuid e utilize no comando abaixo

python manage.py crontab run c79761ab81ac3ff73e3857bc3f50585e