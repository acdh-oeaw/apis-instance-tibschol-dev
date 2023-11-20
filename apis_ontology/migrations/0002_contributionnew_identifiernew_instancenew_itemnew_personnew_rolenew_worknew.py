# Generated by Django 3.1.14 on 2022-02-04 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apis_entities', '0001_initial'),
        ('apis_ontology', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContributionNew',
            fields=[
                ('tempentityclass_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='apis_entities.tempentityclass')),
            ],
            options={
                'abstract': False,
            },
            bases=('apis_entities.tempentityclass',),
        ),
        migrations.CreateModel(
            name='IdentifierNew',
            fields=[
                ('tempentityclass_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='apis_entities.tempentityclass')),
            ],
            options={
                'abstract': False,
            },
            bases=('apis_entities.tempentityclass',),
        ),
        migrations.CreateModel(
            name='InstanceNew',
            fields=[
                ('tempentityclass_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='apis_entities.tempentityclass')),
            ],
            options={
                'abstract': False,
            },
            bases=('apis_entities.tempentityclass',),
        ),
        migrations.CreateModel(
            name='ItemNew',
            fields=[
                ('tempentityclass_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='apis_entities.tempentityclass')),
            ],
            options={
                'abstract': False,
            },
            bases=('apis_entities.tempentityclass',),
        ),
        migrations.CreateModel(
            name='PersonNew',
            fields=[
                ('tempentityclass_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='apis_entities.tempentityclass')),
            ],
            options={
                'abstract': False,
            },
            bases=('apis_entities.tempentityclass',),
        ),
        migrations.CreateModel(
            name='RoleNew',
            fields=[
                ('tempentityclass_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='apis_entities.tempentityclass')),
            ],
            options={
                'abstract': False,
            },
            bases=('apis_entities.tempentityclass',),
        ),
        migrations.CreateModel(
            name='WorkNew',
            fields=[
                ('tempentityclass_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='apis_entities.tempentityclass')),
            ],
            options={
                'abstract': False,
            },
            bases=('apis_entities.tempentityclass',),
        ),
    ]
