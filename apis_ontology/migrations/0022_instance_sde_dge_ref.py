# Generated by Django 4.1.10 on 2023-09-07 00:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("apis_ontology", "0021_alter_instance_external_link_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="instance",
            name="sde_dge_ref",
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
