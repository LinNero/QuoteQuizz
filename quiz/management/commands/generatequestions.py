from django.core.management.base import BaseCommand
from quiz.models import Category, Question, QuestionSet
from random import choice


class Command(BaseCommand):
    help = 'Generate the questions and questions sets'

    def get_random_object(self, queryset):
        pks = queryset.values_list('pk', flat=True)
        random_pk = choice(pks)
        return queryset.get(pk=random_pk)


    def handle(self, *args, **options):
        for category in Category.objects.all():
            if not category.sources.exists():
                continue

            question_set = category.question_sets.last()
            if not question_set:
                question_set = QuestionSet(category_id=category, name="Question Set")
                question_set.save()

            for source in category.sources.all():
                quotes = source.quotes.order_by('-rating')[:10]
                for quote in quotes:
                    if question_set.questions.count() >= 10:
                        question_set = QuestionSet(category_id=category, name="Question Set")
                        question_set.save()

                    q = Question(quote_id=quote,
                                 question_set_id=question_set,
                                 source_1_id=source,
                                 source_2_id=self.get_random_object(category.sources),
                                 source_3_id=self.get_random_object(category.sources),
                                 source_4_id=self.get_random_object(category.sources),
                                 )
                    q.save()



