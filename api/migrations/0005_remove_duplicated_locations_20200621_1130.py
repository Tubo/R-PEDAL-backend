# Generated by Django 3.0.5 on 2020-06-21 11:30

from django.db import migrations

def remove_duplicate(apps, schema_editor):
    Location = apps.get_model('api', 'PiradLocation')
    existing = []
    to_delete = []
    for loc in Location.objects.all():
        label = loc.label
        if label in [label for label in existing]:
            to_delete.append(loc)
            first = Location.objects.filter(label=label).first()
            for lesion in loc.psmalesion_set.all():
                # replace PSMA lesions to first location
                first.psmalesion_set.add(lesion)
                loc.psmalesion_set.remove(lesion)
            for lesion in loc.mrilesion_set.all():
                # replace MRI lesions to first location
                first.mrilesion_set.add(lesion)
                loc.mrilesion_set.remove(lesion)
        existing.append(label)
    for loc in to_delete:
        loc.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200505_0956'),
    ]

    operations = [
        migrations.RunPython(remove_duplicate, reverse_code=migrations.RunPython.noop)
    ]