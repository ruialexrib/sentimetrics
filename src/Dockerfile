FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --root-user-action=ignore --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8082

CMD [ "python", "app.py" ]
