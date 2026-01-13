from django.core.management.base import BaseCommand
from app.models import Bus, Route

class Command(BaseCommand):
    help = 'Add sample buses to the database'

    def handle(self, *args, **options):
        buses = [
            {'name': 'Royal Rider', 'owner': "KPN Classic Travels", 'seats': 100, 'price': 2000},
            {'name': 'Night Falcon', 'owner': "Orange Star Bus Services", 'seats': 60, 'price': 1500},
            {'name': 'Emerald Voyager', 'owner': "GreenLine Express", 'seats': 50 , 'price': 1200},
            {'name': 'Night Rider', 'owner': "KPN Classic Travels", 'seats': 60 , 'price': 1800},
            {'name': 'Shatabdi Express', 'owner': 'Shatabdi Co', 'seats': 42, 'price': 1500},
            {'name': 'Royal Travels', 'owner': 'Royal Co', 'seats': 36, 'price': 1200},
            {'name': 'Kesari Tours', 'owner': 'Kesari Co', 'seats': 40, 'price': 1300},
            {'name': 'VRL Travels', 'owner': 'VRL Co', 'seats': 42, 'price': 1400},
            {'name': 'SRS Travels', 'owner': 'SRS Co', 'seats': 48, 'price': 1600},
            {'name': 'Sharma Tours', 'owner': 'Sharma Co', 'seats': 50, 'price': 1700},
            {'name': 'Redbus Partners', 'owner': 'Redbus Co', 'seats': 48},
            {'name': 'First Class Travel', 'owner': 'FirstClass Co', 'seats': 50},
            {'name': 'Budget Express', 'owner': 'Budget Co', 'seats': 52, 'price': 1800},
            {'name': 'Economy Travel', 'owner': 'Economy Co', 'seats': 55, 'price': 1900},
            {'name': 'Local Express', 'owner': 'Local Co', 'seats': 54, 'price': 2000},
            {'name': 'City Transport', 'owner': 'CityCo', 'seats': 56, 'price': 2100},
            {'name': 'Night Runner Sleeper', 'owner': 'NightRun Co', 'seats': 24, 'price': 800},
            {'name': 'Comfort Sleep Express', 'owner': 'Comfort Co', 'seats': 28, 'price': 900},
            {'name': 'Dream Journey', 'owner': 'Dream Co', 'seats': 24, 'price': 750},
            {'name': 'Rapid Transport', 'owner': 'Rapid Co', 'seats': 49, 'price': 1650},
            {'name': 'Star Travels', 'owner': 'Star Co', 'seats': 38, 'price': 1100},
            {'name': 'Green Transport', 'owner': 'Green Co', 'seats': 58, 'price': 2200},
            {'name': 'Jet Airways Bus', 'owner': 'JetBus Co', 'seats': 35, 'price': 1000},
            {'name': 'Mountain Explorer', 'owner': 'Mountain Co', 'seats': 45, 'price': 1500},
        ]

        # Map some sample buses to existing routes (origin, destination)
        route_map = {
            'Royal Rider': ('Delhi', 'Mumbai'),
            'Night Falcon': ('Delhi', 'Agra'),
            'Emerald Voyager': ('Bangalore', 'Hyderabad'),
            'Night Rider': ('Mumbai', 'Goa'),
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
