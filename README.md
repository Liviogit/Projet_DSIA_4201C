# Projet_DSIA_4201C : Statistiques des contenus Netflix dans le top 10  

## Description  

Le projet **Projet_DSIA_4201C** a pour objectif d'afficher des statistiques sur les films et séries présents dans le top 10 Netflix à l'échelle mondiale et pour chaque pays.  

Ce projet repose sur un pipeline de **scraping**,du**stockage sur une BDD** et une **visualisation dynamique**, le tout organisé en plusieurs conteneurs Docker.  

- **Scrapy** récupère les données sur le site Netflix Top 10.  
- **MongoDB** stocke les données du top 10 mondial.  
- **Elasticsearch** stocke les classements des 93 pays disponibles.  
- **Dash** permet de visualiser et d'interagir avec ces données via une interface web.  

L'ensemble des conteneurs est orchestré par **Docker Compose** pour simplifier le déploiement ainsi que sa portabilitée.  

---

## Architecture du Projet  

Le projet est organisé en **4 types de conteneurs** interconnectés :  

### 1️⃣ **Scrapy (Python) : Extraction des données**  

Scrapy est utilisé pour extraire les données depuis [https://www.netflix.com/tudum/top10](https://www.netflix.com/tudum/top10). Deux spiders ont été créées :  

- **`netflix_top10`** :  
  - Scrape le top 10 mondial des films et séries.  
  - Stocke ces données dans **MongoDB** via une pipeline Scrapy.  

- **`netflix_top10_country`** :  
  - Scrape les classements pour chacun des **93 pays**.  
  - Stocke ces données dans **Elasticsearch** via une autre pipeline Scrapy.  

**Pipelines Scrapy :**  
Les pipelines permettent d’envoyer automatiquement les données scrappées vers la base de données correspondante.  

- **MongoDBPipeline** : Insère uniquement les **top 10 mondiaux** dans MongoDB.  
- **ElasticsearchPipeline** : Stocke les données des **93 pays** dans Elasticsearch.  

---

### 2️⃣ **MongoDB : Stockage des données simplifiées**  

MongoDB est utilisé pour stocker **uniquement** le top 10 **mondial** (films et séries).  

- Contenu stocké :  
  - `title` : Nom du film/série.  
  - `category` : Film ou série.  
  - `rank` : Position dans le top 10 mondial.  
  - `week` : Nombre de semaines dans le top 10.  

MongoDB est principalement utilisé pour **générer des graphiques en barres** simples.  

---

### 3️⃣ **Elasticsearch : Indexation et recherche**  

Elasticsearch stocke les **top 10 des 93 pays** sous forme d'index permettant une recherche rapide.  

- Contenu stocké :  
  - `title` : Nom du film/série.  
  - `categorie` : Film ou série.  
  - `sources` : Pays du top 10.

**Utilisation d’Elasticsearch :**  
- Recherche d’un titre dans les **top 10 de tous les pays**.  
- Génération de graphiques à partir des **données textuelles**.  

---

### 4️⃣ **Dash (Python) : Interface de visualisation**  

Dash est utilisé pour afficher les données sous forme interactive.  

**Fonctionnalités de Dash :**  
- **Graphiques personnalisables** : Filtrer les films/séries selon différentes catégories (anglais/non-anglais).  
- **Recherche de titres** : Vérifier si un film/série figure dans un top 10 d’un pays.  
- **Affichage dynamique** : Les données sont récupérées en temps réel depuis MongoDB et Elasticsearch.  

L’interface est accessible à l’URL : [http://localhost:8051](http://localhost:8051).  

---

## 🔧 Gestion des Conteneurs avec Docker  

Le projet est entièrement conteneurisé avec **Docker Compose**, permettant de déployer tous les services en une seule commande.  

## 📥 Installation et Exécution  

### **1️⃣ Prérequis**  
Avant de commencer, assurez-vous d’avoir :  
- **Docker** installé 
- **Git** installé  

### **2️⃣ Cloner le projet**  
```bash
git clone https://github.com/Liviogit/Projet_DSIA_4201C
cd Projet_DSIA_4201C
```

### **3️⃣ Lancer les conteneurs**  
Exécutez la commande suivante pour **construire et démarrer tous les services** :  
```bash
docker-compose up --build
```

### **4️⃣ Accéder à l’interface**  
Une fois les conteneurs lancés, ouvrez un navigateur et allez sur :  
[http://localhost:8051](http://localhost:8051)  

---

## 📂 Organisation du projet  

```
Projet_DSIA_4201C/
├── dash_app/                   #Conteneur générant l'interface dash
│   ├── ...
├── netflix_scraper/            #Contiens les 2 spiders, 2 conteneurs seront créés à partir de ce dossier
│   ├── ...
├── .gitignore
├── Pipfile
├── Pipfile.lock
├── README.md
├── docker-compose.yml          #Permet la structuration des conteneurs, ainsi que leurs interconnections
└── requirements.txt

```

---

## 📌 Fonctionnement Technique  

### **Scrapy et les Pipelines**  
1. Scrapy se connecte à **https://www.netflix.com/tudum/top10**.  
2. Il extrait les données et les envoie vers la **pipeline MongoDB ou Elasticsearch**.  
3. MongoDB stocke uniquement les **top 10 mondiaux**.  
4. Elasticsearch indexe les **top 10 de tous les pays**.  

### **Docker et l’Orchestration**  
- **`docker-compose up --build`** démarre tous les conteneurs simultanément.  
- **Les dépendances sont gérées automatiquement** (Scrapy attend MongoDB et Elasticsearch avant de s'exécuter).  
- **Isolation des services** : Chaque composant tourne dans son propre conteneur.  

---

## 👤 Contributeur  
- **Livio Daninthe** (Unique contributeur)  

---

## 📜 Licence  
Ce projet est open-source.  

---