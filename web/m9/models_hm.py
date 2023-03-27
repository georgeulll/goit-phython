from mongoengine import connect, Document, StringField, ReferenceField, ListField, CASCADE


connect(host="mongodb+srv://NickGoit:Dp_ua_1989@clusterlearn.5mbivax.mongodb.net/HomeWork_Module9", ssl=True)


class Authors(Document):
    fullname = StringField(required=True, max_length=50)
    born_date = StringField(required=True,max_length=50)
    born_location = StringField(required=True, max_length=100)
    description = StringField(required=True)


class Quotes(Document):
    tags = ListField(StringField())
    author = ReferenceField(Authors, reverse_delete_rule=CASCADE)
    quote = StringField(required=True)
    meta = {'allow_inheritance': True}
