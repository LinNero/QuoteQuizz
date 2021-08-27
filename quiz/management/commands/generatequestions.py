from django.core.management.base import BaseCommand
from quiz.models import Category, Question, QuestionSet
from random import choice


class Command(BaseCommand):
    help = 'Generate the questions and questions sets'

    def __init__(self):
        super().__init__()
        self.current_question_set = None

    def get_random_object(self, queryset):
        pks = queryset.values_list('pk', flat=True)
        random_pk = choice(pks)
        return queryset.get(pk=random_pk)

    def handle(self, *args, **options):
        for category in Category.objects.all():
            if not category.sources.exists():
                continue

            self.current_question_set = self.create_question_set(category)

            for source in category.sources.all():
                self.create_questions_for_source(category, source)

    def create_questions_for_source(self, category, source):
        quotes = source.quotes.order_by('-rating')[:10]
        for quote in quotes:
            self.create_question_for_quote(category, quote, source)

    def create_question_set(self, category):
        question_set = category.question_sets.last()
        if not question_set:
            question_set = QuestionSet(category_id=category, name="Question Set")
            question_set.save()
        return question_set

    def create_question_for_quote(self, category, quote, source):
        if self.current_question_set.questions.count() >= 10:
            self.current_question_set = QuestionSet(category_id=category, name="Question Set")
            self.current_question_set.save()
        answers = self.create_answers_list_for_question(category, source)
        q = Question(quote_id=quote,
                     question_set_id=self.current_question_set,
                     source_1_id=category.sources.get(pk=answers[0]),
                     source_2_id=category.sources.get(pk=answers[1]),
                     source_3_id=category.sources.get(pk=answers[2]),
                     source_4_id=category.sources.get(pk=answers[3]),
                     )
        q.save()

    def create_answers_list_for_question(self, category, source):
        answers = {source.id,
                   self.get_random_object(category.sources).id,
                   self.get_random_object(category.sources).id,
                   self.get_random_object(category.sources).id
                   }
        while len(answers) < 4:  # цикл для несовпадения ответов
            answers.add(self.get_random_object(category.sources).id)
        answers = list(answers)
        return answers
