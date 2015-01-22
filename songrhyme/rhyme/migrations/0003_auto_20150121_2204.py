# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rhyme', '0002_create_first_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='word',
            options={},
        ),
        migrations.RemoveField(
            model_name='word',
            name='parts_of_speech',
        ),
        migrations.AddField(
            model_name='word',
            name='pos',
            field=models.CommaSeparatedIntegerField(default=b'', max_length=255, choices=[(0, b'Noun'), (1, b'Verb'), (2, b'Adjective'), (3, b'Adverb')]),
            preserve_default=True,
        ),
    ]
