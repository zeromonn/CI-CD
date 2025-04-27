FROM ubuntu:22.04

# Atualizar e instalar pacotes necessários
RUN apt-get update && apt-get install -y \
    curl \
    git \
    vim \
    dos2unix \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho
WORKDIR /app

# Copiar arquivos necessários para o contêiner
COPY . /app

# Comando padrão
CMD ["/bin/bash"]