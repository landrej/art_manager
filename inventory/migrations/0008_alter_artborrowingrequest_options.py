# Generated by Django 4.1.1 on 2022-09-29 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_alter_artborrowingrequest_requester'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='artborrowingrequest',
            options={'permissions': [('delete_own_request', 'User can delete own borrowing request')]},
        ),
    ]
