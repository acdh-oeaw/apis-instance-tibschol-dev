# Generated by Django 4.1.10 on 2023-09-07 00:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("apis_ontology", "0023_remove_instance_sde_dge_ref_work_sde_dge_ref"),
    ]

    operations = [
        migrations.AlterField(
            model_name="instance",
            name="alternative_names",
            field=models.TextField(
                blank=True, null=True, verbose_name="Alternative names"
            ),
        ),
        migrations.AlterField(
            model_name="instance",
            name="external_link",
            field=models.TextField(
                blank=True, null=True, verbose_name="External links"
            ),
        ),
        migrations.AlterField(
            model_name="instance",
            name="tibschol_ref",
            field=models.CharField(
                blank=True, max_length=25, null=True, verbose_name="Tibschol reference"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="alternative_names",
            field=models.TextField(
                blank=True, null=True, verbose_name="Alternative names"
            ),
        ),
        migrations.AlterField(
            model_name="person",
            name="external_link",
            field=models.TextField(
                blank=True, null=True, verbose_name="External links"
            ),
        ),
        migrations.AlterField(
            model_name="place",
            name="alternative_names",
            field=models.TextField(
                blank=True, null=True, verbose_name="Alternative names"
            ),
        ),
        migrations.AlterField(
            model_name="place",
            name="external_link",
            field=models.TextField(
                blank=True, null=True, verbose_name="External links"
            ),
        ),
        migrations.AlterField(
            model_name="work",
            name="alternative_names",
            field=models.TextField(
                blank=True, null=True, verbose_name="Alternative names"
            ),
        ),
        migrations.AlterField(
            model_name="work",
            name="external_link",
            field=models.TextField(
                blank=True, null=True, verbose_name="External links"
            ),
        ),
        migrations.AlterField(
            model_name="work",
            name="sde_dge_ref",
            field=models.CharField(
                blank=True, max_length=25, null=True, verbose_name="Derge reference"
            ),
        ),
    ]
