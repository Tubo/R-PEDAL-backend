# Generated by Django 3.0.5 on 2020-04-22 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_lesion_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='Entry',
            new_name='MriEntry',
        ),
        migrations.RenameModel(
            old_name='Lesion',
            new_name='MriLesion',
        ),
    ]