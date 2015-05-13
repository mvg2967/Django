# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_auto_20141231_2102'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('total', models.DecimalField(max_digits=100, decimal_places=2)),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('products', models.ManyToManyField(to='product.Product', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
