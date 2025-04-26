FROM ubuntu:22.04

# Atualizar pacotes e instalar dependências
RUN apt-get update && apt-get install -y curl git vim sudo

# Adicionar usuário com variáveis de ambiente
ARG USERNAME
ARG PASSWORD
RUN useradd -m $USERNAME && echo "$USERNAME:$PASSWORD" | chpasswd && adduser $USERNAME sudo

# Definir diretório de trabalho
WORKDIR /home/$USERNAME

# Comando padrão
CMD ["/bin/bash"]