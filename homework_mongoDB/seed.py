import os
import json
from mongoengine.errors import NotUniqueError

from models import Author, Quote
current_directory = os.path.dirname(os.path.abspath(__file__))

authors_file_path = os.path.join(current_directory, 'authors.json')
quotes_file_path = os.path.join(current_directory, 'quotes.json')


if __name__ == '__main__':
    with open(authors_file_path, encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            try:
                author = Author(fullname=el.get('fullname'), born_date=el.get('born_date'),
                                born_location=el.get('born_location'), description=el.get('description'))
                author.save()
            except NotUniqueError:
                print(f"The author exists {el.get('fullname')}")



    with open(quotes_file_path, encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            author, *_ = Author.objects(fullname=el.get('author'))
            quote = Quote(quote=el.get('quote'), tags=el.get('tags'), author=author)
            quote.save()

