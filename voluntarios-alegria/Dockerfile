# Etapa 1: Usar uma imagem base do Python
FROM python:3.12-slim

# Etapa 2: Definir o diretório de trabalho dentro do container
WORKDIR /app

# Etapa 3: Copiar o arquivo de dependências (requirements.txt) para o diretório de trabalho
COPY requirements.txt /app/

# Etapa 4: Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 5: Copiar o código do projeto e o entrypoint para dentro do container
COPY . /app/

# Etapa 6: Copiar o script de entrypoint
COPY entrypoint.sh /entrypoint.sh

# Etapa 7: Dar permissão de execução ao script
RUN chmod +x /entrypoint.sh

# Etapa 8: Definir as variáveis de ambiente
ENV PYTHONUNBUFFERED=1

# Etapa 9: Expor a porta 8000 (porta padrão do Django)
EXPOSE 8000

# Etapa 10: Usar o script de entrypoint
ENTRYPOINT ["/entrypoint.sh"]
