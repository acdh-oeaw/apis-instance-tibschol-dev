# Generated by Django 3.1.14 on 2022-11-30 07:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apis_entities', '0001_initial'),
        ('apis_ontology', '0006_auto_20220204_1021'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('tempentityclass_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='apis_entities.tempentityclass')),
            ],
            options={
                'abstract': False,
            },
            bases=('apis_entities.tempentityclass',),
        ),
        migrations.AddField(
            model_name='instance',
            name='citation',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='citation'),
        ),
        migrations.AddField(
            model_name='work',
            name='subject',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='subject'),
        ),
    ]
