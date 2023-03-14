from models_hm import Authors, Quotes


def authors_id(name):
    authors = Authors.objects(fullname=name)
    for author in authors:
        return author.id


def quotes_by_name(id_):
    quotes = Quotes.objects(author=id_)
    for quote in quotes:
        print(quote.to_json())


def quotes_by_tag(tag_):
    quotes = Quotes.objects(tags=tag_)
    for quote in quotes:
        print(quote.to_json())


def quotes_by_tags(data):
    quotes = Quotes.objects(tags__in=data)
    for quote in quotes:
        print(quote.to_json())


def main():
    flag = 1
    while flag == 1:
        data = input('Please type command:value-> ')
        data = data.split(':')
        match data[0]:
            case "name":
                id_name = authors_id(data[1])
                quotes_by_name(id_name)
            case "tag":
                quotes_by_tag(data[1])
            case "tags":
                tags_r=data[1].split(',')
                quotes_by_tags(tags_r)
            case 'exit':
                flag = 0


if __name__ == "__main__":
    main()