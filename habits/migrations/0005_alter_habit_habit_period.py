# Generated by Django 4.2.6 on 2023-10-29 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0004_prize_prize_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='habit_period',
            field=models.CharField(choices=[('ежедневно', 'ежедневно'), ('еженедельно', 'еженедельно')], default='ежедневно', max_length=20, verbose_name='периодичность привычки'),
        ),
    ]