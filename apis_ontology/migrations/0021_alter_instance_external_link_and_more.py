# Generated by Django 4.1.10 on 2023-09-07 00:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "apis_ontology",
            "0020_instance_alternative_names_instance_tibschol_ref_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="instance",
            name="external_link",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="person",
            name="external_link",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="place",
            name="external_link",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="work",
            name="external_link",
            field=models.TextField(blank=True, null=True),
        ),
    ]
