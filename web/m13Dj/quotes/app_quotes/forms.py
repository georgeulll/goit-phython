from django.forms import ModelForm, CharField, TextInput, DateField, DateInput, ModelChoiceField, \
    ModelMultipleChoiceField, SelectMultiple, Select

from .models import Tag, Author, Quotes


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Tag
        fields = ['name']


class QuotesForm(ModelForm):
    quote_text = CharField(required=True,
                           widget=TextInput(attrs={"class": "form-control"}))
    author = ModelChoiceField(queryset=Author.objects.all().order_by('fullname'),
                              widget=Select(attrs={"class": "form-select"}))
    tags = ModelMultipleChoiceField(queryset=Tag.objects.all().order_by('name'),
                                    widget=SelectMultiple(attrs={"class": "form-select", "size": "7"}))

    class Meta:
        model = Quotes
        fields = ['quote_text', 'author', 'tags']

# class QuotesForm(ModelForm):
#     author = ModelChoiceField(queryset=Author.objects.none())  # noqa
#     tags = ModelMultipleChoiceField(queryset=Tag.objects.none())  # noqa
#
#     class Meta:
#         model = Quotes
#         fields = ['quote', 'author', 'tags']
#
#     def __init__(self, user: User, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['author'].queryset = Author.objects.filter(user=user)  # noqa
#         self.fields['tags'].queryset = Tag.objects.all()  # noqa


class AuthorForm(ModelForm):
    fullname = CharField(max_length=100, required=True,
                         widget=TextInput(attrs={"class": "form-control"}))
    born_date = DateField(widget=DateInput(attrs={"class": "form-control", "placeholder": "Year-Month-day"}))
    born_location = CharField(max_length=100, required=True,
                              widget=TextInput(attrs={"class": "form-control"}))
    description = CharField(required=True, widget=TextInput(attrs={"class": "form-control"}))

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']