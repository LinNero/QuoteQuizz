# Generated by Django 3.2.6 on 2021-08-23 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0005_auto_20210816_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersQuestions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_correct', models.BooleanField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='users',
            field=models.ManyToManyField(through='quiz.UsersQuestions', to=settings.AUTH_USER_MODEL),
        ),
    ]