# Generated by Django 3.2.6 on 2021-08-16 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_quote_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='', upload_to='images/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='question_set_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.questionset'),
        ),
        migrations.AlterField(
            model_name='questionset',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_sets', to='quiz.category'),
        ),
        migrations.AlterField(
            model_name='quote',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotes', to='quiz.source'),
        ),
        migrations.AlterField(
            model_name='source',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sources', to='quiz.category'),
        ),
    ]
