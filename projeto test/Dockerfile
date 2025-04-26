# Usar uma imagem base com Python
FROM python:3.9.16-alpine3.18

# Definir o diretório de trabalho
WORKDIR /app

# Criar o diretório para o volume do banco de dados
RUN mkdir -p /vol/bd

# Copiar os arquivos do projeto para o contêiner
COPY . /app

# Instalar dependências (se houver)
# Remova esta linha se não houver um arquivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Gerar o arquivo requirements.txt com as dependências instaladas
RUN pip freeze > requirements.txt

# Criar um usuário não-root para executar o programa
RUN useradd -m appuser
USER appuser

# Expor a porta (se necessário)
EXPOSE 8080

# Comando para executar o programa
CMD ["python", "Cliente-maneger.py"]

