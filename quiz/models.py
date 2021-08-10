from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Source(models.Model):
    name = models.CharField(max_length=255)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Quote(models.Model):
    text = models.TextField()
    source = models.ForeignKey(Source, on_delete=models.CASCADE)


class QuestionSet(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class Question(models.Model):
    quote_id = models.ForeignKey(Quote, on_delete=models.CASCADE)
    source_1_id = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='source_1')
    source_2_id = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='source_2')
    source_3_id = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='source_3')
    source_4_id = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='source_4')
    question_set_id = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)



