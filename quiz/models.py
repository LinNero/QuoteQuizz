from django.db import models
import random
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name


class Source(models.Model):
    name = models.CharField(max_length=255)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="sources")
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Quote(models.Model):
    text = models.TextField()
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name="quotes")
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.rating}: {self.text}"

class QuestionSet(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="question_sets")
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Question(models.Model):
    quote_id = models.ForeignKey(Quote, on_delete=models.CASCADE)
    source_1_id = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='source_1')
    source_2_id = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='source_2')
    source_3_id = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='source_3')
    source_4_id = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='source_4')
    question_set_id = models.ForeignKey(QuestionSet, on_delete=models.CASCADE, related_name='questions')
    users = models.ManyToManyField(User, through='UsersQuestions')

    def __str__(self):
        return self.quote_id.text[:500]

    def get_randomized_source_list(self):
        result = [self.source_1_id, self.source_2_id, self.source_3_id, self.source_4_id]
        random.shuffle(result)
        return result


class UsersQuestions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField()

