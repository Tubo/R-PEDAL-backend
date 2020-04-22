from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from api.models import Location


class Command(BaseCommand):
    help = "Load prebuilt data"

    def add_arguments(self, parser):
        parser.add_argument('--locations', action='store_true')

    def handle(self, *args, **options):
        if options.get('locations'):
            objects = []
            laterality = ("L", "R")
            levels = Location.level_choices
            zones = Location.zone_choices

            for lat in laterality:
                objects.append(Location(laterality=lat, level="BASE", zone="CZ"))
                objects.append(Location(laterality=lat, level="SV", zone="SV"))
                for (lvl, _) in levels:
                    if lvl in ("SV", "URETHRA"):
                        continue
                    for (z, _) in zones:
                        if z in ("SV", "URETHRA", "CZ"):
                            continue
                        location = Location(laterality=lat, level=lvl, zone=z, )
                        objects.append(location)
            objects.append(Location(level="URETHRA", zone="URETHRA"))
            try:
                Location.objects.bulk_create(objects)
            except IntegrityError:
                print("\nStopping...")
                print("The command has probably been ran before.")

