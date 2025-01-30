from elasticsearch import Elasticsearch
import pymongo

class NetflixTop10Pipeline:
    def open_spider(self, spider):
        if spider.name == 'netflix_top10':
            # Connexion à MongoDB
            self.client = pymongo.MongoClient("mongodb://root:example@mongodb:27017/")
            self.client.drop_database("netflix_data")
            self.db = self.client["netflix_data"]
            self.collection = self.db["top10"]

    def close_spider(self, spider):
        if spider.name == 'netflix_top10':
            self.client.close()

    def process_item(self, item, spider):
        if spider.name == 'netflix_top10':
            # Insérer les données dans la collection MongoDB
            self.collection.insert_one(dict(item))
        return item

class NetflixTop10Pipelinecountry:
    def __init__(self):
        # Créer une instance de client Elasticsearch
        self.es = Elasticsearch("http://elasticsearch:9200")  # Assurez-vous que l'URL correspond à votre instance Elasticsearch
        self.index_name = 'netflix_top10'  # Nom de l'index dans Elasticsearch
        if self.es.indices.exists(index=self.index_name):
            self.es.indices.delete(index=self.index_name)
    def open_spider(self, spider):
        # Ce code est appelé quand la spider commence à tourner
        self.titles = {}  # Dictionnaire pour stocker les titres, sources et catégories

    def close_spider(self, spider):
        # Ce code est appelé quand la spider est terminée, on n'a pas besoin de stocker les données dans un fichier JSON
        pass

    def process_item(self, item, spider):
        title = item['title']
        source = item['source']
        categorie = item['categorie']

        # Si le titre existe déjà dans le dictionnaire, on ajoute la source et la catégorie
        if title in self.titles:
            if source not in self.titles[title][0]:
                self.titles[title][0].append(source)
            if categorie not in self.titles[title][1]:
                self.titles[title][1].append(categorie)
        else:
            # Sinon, on crée une nouvelle entrée avec la source et la catégorie dans des listes
            self.titles[title] = [[source], [categorie]]

        # Ajouter les données dans Elasticsearch
        document = {
            'title': title,
            'sources': self.titles[title][0],
            'categorie': self.titles[title][1],
        }

        # Indexer le document dans Elasticsearch
        self.es.index(index=self.index_name, document=document)

        return item