# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-20 20:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_auto_20160220_1049'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('game', 'user')]),
        ),
        migrations.AlterIndexTogether(
            name='membership',
            index_together=set([('game', 'user')]),
        ),
    ]