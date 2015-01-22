# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rhyme', '0003_auto_20150121_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='synonyms',
            field=models.ManyToManyField(related_name='synonym', to='rhyme.Word'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='word',
            name='pos',
            field=models.CommaSeparatedIntegerField(default=b'', max_length=255, choices=[(0, b'Noun'), (1, b'Verb'), (2, b'Adjective'), (3, b'Adverb'), (4, b'Preposition')]),
            preserve_default=True,
        ),
    ]
