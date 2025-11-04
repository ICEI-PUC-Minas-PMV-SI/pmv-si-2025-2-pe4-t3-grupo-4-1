#!/bin/sh

# Rodar as migrations para o app de autenticação
python manage.py makemigrations

# Rodar as migrações
python manage.py migrate

# Criar o superusuário automaticamente usando as variáveis de ambiente
python manage.py createsuperuser --noinput || true

# Rodar o servidor do Django
python manage.py runserver 0.0.0.0:8000
