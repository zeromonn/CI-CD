# Usar uma imagem Ubuntu
FROM ubuntu:22.04

# Atualizar pacotes e instalar dependências básicas
RUN apt-get update && apt-get install -y \
    curl \
    git \
    vim \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Definir um usuário não-root
RUN useradd -m diego && echo "diego:password" | chpasswd && adduser diego sudo

# Definir diretório de trabalho
WORKDIR /home/diego

# Comando padrão do contêiner
CMD ["/bin/bash"]
