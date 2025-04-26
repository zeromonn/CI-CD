# Usar uma imagem Ubuntu
FROM ubuntu:22.04

# Atualizar pacotes e instalar dependências básicas
RUN apt-get update && apt-get install -y \
    curl=7.81.0-1ubuntu1.10 \
    git=1:2.34.1-1ubuntu1.10 \
    vim=2:8.2.3995-1ubuntu2.10 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Criar um usuário não-root (sem senha)
RUN useradd -m diego

# Definir diretório de trabalho
WORKDIR /home/diego

# Comando padrão do contêiner
CMD ["/bin/bash"]
