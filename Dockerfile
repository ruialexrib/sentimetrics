# Use a imagem base oficial do Python
FROM python:3.10-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências necessárias
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o conteúdo do diretório atual para o diretório de trabalho no contêiner
COPY . .

# Exponha a porta 5000 para acessar a aplicação Flask
EXPOSE 8081

# Comando para iniciar a aplicação Flask quando o contêiner for iniciado
CMD [ "python", "app.py" ]
