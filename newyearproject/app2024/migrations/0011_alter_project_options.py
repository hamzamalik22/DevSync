# Generated by Django 5.0 on 2024-01-08 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app2024', '0010_alter_project_options_review_owner_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-vote_ratio', '-vote_total']},
        ),
    ]