from typing import List, Any
from bson.objectid import ObjectId
from models import Author, Quote


def find_by_tag(tag: str) -> list[str | None]:
    print(f"Find by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result

def find_by_author(author: str) -> list[list[Any]]:
    print(f"Find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


def main():
    while True:
        command = input("Enter your command (name: fullname, tag: tag , tags: tag1,tag2, exit): ").lower()
        if command.startswith('name:'):
            author = command.split(':')[1].strip() 
            print(find_by_author(author)) 
        elif command.startswith('tag:'):
            tag = command.split(':')[1].strip()
            print(find_by_tag(tag))
        elif command.startswith('tags:'):
            tags = command.split(':')[1].strip().split(",")
            # quotes = []
            for tag in tags:
                print( find_by_tag(tag.strip()))
        elif command == 'exit':
            print("goodbye")
            break
        else:
            print("Unknown command")



if __name__ =="__main__":
    main()

