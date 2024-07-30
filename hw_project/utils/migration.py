# import os
# import django
#
# from pymongo import MongoClient
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw_project.settings")
# django.setup()
#
# from quotes.models import Quote, Tag, Author # noqa
#
# client = MongoClient("mongodb://localhost")
#
# db = client.hw_django
#
# authors = db.authors.find()
#
# for author in authors:
#     Author.objects.get_or_create(
#         fullname=author['fullname'],
#         born_date=author['fullname'],
#         born_location=author['fullname'],
#         description=author['fullname']
#     )

# import os
# import sys
# import django
# import logging
#
# logging.basicConfig(level=logging.DEBUG)
#
# from pymongo import MongoClient
#
# # Додавання кореневої директорії проекту до PYTHONPATH
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# logging.debug(f"sys.path: {sys.path}")
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw_project.settings")
# logging.debug(f"DJANGO_SETTINGS_MODULE: {os.environ['DJANGO_SETTINGS_MODULE']}")
#
# try:
#     django.setup()
# except Exception as e:
#     logging.error(f"Error setting up Django: {e}")
#     sys.exit(1)
#
# from quotes.models import Author # noqa
#
# client = MongoClient("mongodb://localhost")
#
# db = client.hw_django
#
# authors = db.authors.find()
#
# for author in authors:
#     try:
#         Author.objects.get_or_create(
#             fullname=author['fullname'],
#             born_date=author['born_date'],
#             born_location=author['born_location'],
#             description=author['description']
#         )
#     except Exception as e:
#         logging.error(f"Error processing author {author['fullname']}: {e}")


import os
import sys
import django
import logging



logging.basicConfig(level=logging.DEBUG)

from pymongo import MongoClient

# Додавання кореневої директорії проекту до PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
logging.debug(f"sys.path: {sys.path}")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hw_project.settings")
logging.debug(f"DJANGO_SETTINGS_MODULE: {os.environ['DJANGO_SETTINGS_MODULE']}")

try:
    django.setup()
except Exception as e:
    logging.error(f"Error setting up Django: {e}")
    sys.exit(1)

from quotes.models import Quote, Tag, Author # noqa

client = MongoClient("mongodb://localhost")

db = client.hw_django

# Перевірка наявності колекції
if 'authors' not in db.list_collection_names():
    logging.error("Collection 'authors' does not exist in MongoDB")
    sys.exit(1)

authors = db.authors.find()

for author in authors:
    Author.objects.get_or_create(
        fullname=author['fullname'],
        born_date=author['born_date'],
        born_location=author['born_location'],
        description=author['description']
    )

quotes = db.quotes.find()

for quote in quotes:
    tags = []
    for tag in quote['tags']:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)
    print(tags)


exist_quote =bool(len(Quote.objects.filter(quote=quote['quote'])))

if not exist_quote:
    author = db.authors.find_one({'_id': quote['author']})
    a = Author.objects.get(fullname=author['fullname'])
    q = Quote.objects.create(
        quote=quote['quote'],
        author=a
    )
    for tag in tags:
        q.tags.add(tag)



    # except Exception as e:
    #     logging.error(f"Error processing author {author.get('fullname', 'unknown')}: {e}")
