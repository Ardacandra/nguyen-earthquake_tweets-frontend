# Generated by Django 3.1.7 on 2021-03-06 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('tweet_id', models.CharField(max_length=50)),
                ('tweet_text', models.CharField(max_length=300)),
                ('screen_name', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('is_relevant', models.BooleanField(default=False)),
            ],
        ),
    ]
