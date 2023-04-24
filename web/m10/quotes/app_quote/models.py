from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Author(models.Model):
    fullname = models.CharField(max_length=100, null=False, unique=True)
    born_date = models.DateField(max_length=100, null=False)
    born_location = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.fullname


class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='tag of username')]

    def __str__(self):
        return f"{self.name}"


class Quotes(models.Model):
    quote_text = models.TextField(null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=False)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.quote_text}:{self.author}"