from django.core.management.base import BaseCommand
from app.models import Bus, Route

class Command(BaseCommand):
    help = 'Add sample buses to the database'

    def handle(self, *args, **options):
        buses = [
            {'name': 'Shatabdi Express', 'owner': 'Shatabdi Co', 'seats': 42},
            {'name': 'Royal Travels', 'owner': 'Royal Co', 'seats': 36},
            {'name': 'Kesari Tours', 'owner': 'Kesari Co', 'seats': 40},
            {'name': 'VRL Travels', 'owner': 'VRL Co', 'seats': 42},
            {'name': 'SRS Travels', 'owner': 'SRS Co', 'seats': 48},
            {'name': 'Sharma Tours', 'owner': 'Sharma Co', 'seats': 50},
            {'name': 'Redbus Partners', 'owner': 'Redbus Co', 'seats': 48},
            {'name': 'First Class Travel', 'owner': 'FirstClass Co', 'seats': 50},
            {'name': 'Budget Express', 'owner': 'Budget Co', 'seats': 52},
            {'name': 'Economy Travel', 'owner': 'Economy Co', 'seats': 55},
            {'name': 'Local Express', 'owner': 'Local Co', 'seats': 54},
            {'name': 'City Transport', 'owner': 'CityCo', 'seats': 56},
            {'name': 'Night Runner Sleeper', 'owner': 'NightRun Co', 'seats': 24},
            {'name': 'Comfort Sleep Express', 'owner': 'Comfort Co', 'seats': 28},
            {'name': 'Dream Journey', 'owner': 'Dream Co', 'seats': 24},
            {'name': 'Rapid Transport', 'owner': 'Rapid Co', 'seats': 49},
            {'name': 'Star Travels', 'owner': 'Star Co', 'seats': 38},
            {'name': 'Green Transport', 'owner': 'Green Co', 'seats': 58},
            {'name': 'Jet Airways Bus', 'owner': 'JetBus Co', 'seats': 35},
            {'name': 'Mountain Explorer', 'owner': 'Mountain Co', 'seats': 45},
        ]

        # Map some sample buses to existing routes (origin, destination)
        route_map = {
            'Shatabdi Express': ('Delhi', 'Mumbai'),
            'Royal Travels': ('Delhi', 'Jaipur'),
            'Kesari Tours': ('Delhi', 'Agra'),
            'VRL Travels': ('Mumbai', 'Pune'),
            'SRS Travels': ('Bangalore', 'Chennai'),
            'Sharma Tours': ('Bangalore', 'Hyderabad'),
            'Redbus Partners': ('Bangalore', 'Mysore'),
            'First Class Travel': ('Chennai', 'Bangalore'),
            'Budget Express': ('Mumbai', 'Goa'),
            'Economy Travel': ('Pune', 'Mumbai'),
            'Local Express': ('Goa', 'Bangalore'),
            'City Transport': ('Kolkata', 'Delhi'),
            'Night Runner Sleeper': ('Jaipur', 'Delhi'),
            'Comfort Sleep Express': ('Ahmedabad', 'Mumbai'),
            'Dream Journey': ('Lucknow', 'Delhi'),
            'Rapid Transport': ('Hyderabad', 'Bangalore'),
            'Star Travels': ('Mumbai', 'Ahmedabad'),
            'Green Transport': ('Mysore', 'Bangalore'),
            'Jet Airways Bus': ('Kolkata', 'Patna'),
            'Mountain Explorer': ('Delhi', 'Lucknow'),
        }

        for bus_data in buses:
            # attempt to attach a Route foreign key when possible
            route = None
            mapped = route_map.get(bus_data['name'])
            if mapped:
                origin, destination = mapped
                try:
                    route = Route.objects.get(origin_city=origin, destination_city=destination)
                except Route.DoesNotExist:
                    route = None
            defaults = {
                'owner': bus_data.get('owner', ''),
                'seats': bus_data.get('seats', 0),
            }
            if route:
                defaults['route'] = route

            bus, created = Bus.objects.get_or_create(
                name=bus_data['name'],
                defaults=defaults,
            )
            status = "✓ Created" if created else "⚠ Already exists"
            route_info = f" → {bus.route.origin_city}→{bus.route.destination_city}" if getattr(bus, 'route', None) else ''
            self.stdout.write(f"{status}: {bus.name} (owner: {bus.owner}) - {bus.seats} seats{route_info}")

        self.stdout.write(self.style.SUCCESS('\n✓ Bus data import completed!'))
