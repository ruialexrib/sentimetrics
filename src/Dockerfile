# Use a imagem base oficial do Python
FROM python:3.12-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências necessárias
RUN pip install --root-user-action=ignore --no-cache-dir -r requirements.txt

# Copie todo o conteúdo do diretório atual para o diretório de trabalho no contêiner
COPY . .

# Exponha a porta 5000 para acessar a aplicação Flask
EXPOSE 8082

# Comando para iniciar a aplicação Flask quando o contêiner for iniciado
CMD [ "python", "app.py" ]
