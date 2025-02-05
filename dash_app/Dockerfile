# 1️⃣ Utiliser une image Python avec Scrapy
FROM python:3.9

# 2️⃣ Définir le dossier de travail dans le conteneur
WORKDIR /dash_app

# 3️⃣ Copier les fichiers du projet dans l'image Docker
COPY . .

# 4️⃣ Installer Scrapy et les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ Attendre que MongoDB soit prêt avant d'exécuter Scrapy
CMD ["sh", "-c", "./wait-for-it.sh elasticsearch:9200 -- python app.py"]