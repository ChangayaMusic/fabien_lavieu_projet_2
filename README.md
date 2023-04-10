# Projet 2 Fabien Lavieu


[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)]

Un script pour scraper les informations du site : http://books.toscrape.com/
Il est possible de scrapper : livre / categories / tous les livres

## Pour commencer

Nous allons devoir interroger un site en temps réel, une connexion internet est nécessaire.


### Pré-requis



- Python 3.9
- Une console
- Les packages cités dans requierements.txt

### Installation


- Installer les packages avec pip install -r /path/to/requirements.txt


## Démarrage

- Dans la console : python3 main.py
- Vous serez interrogé à chaque étapes qui suivent sur les actions que vous voulez effectuer.
- Scraper un livre
- Scraper toutes les catégories
- Scrapper une seule catégorie

## Eléments scrappés

- product_page_url
- universal_ product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url
- image.jpg


## Datas

Les datas sont enregistrées suivant :
- CSV : /data/"categorie"/
- Images : /data/"categorie"/images
- Les livres seuls seront enregistré comme /data/"titre du livre"



## Fabriqué avec


* Pycharm Community



## Auteurs

Fabien Lavieu

## License

Ce projet est open source.


