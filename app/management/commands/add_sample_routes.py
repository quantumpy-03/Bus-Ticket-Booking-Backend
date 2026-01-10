from django.core.management.base import BaseCommand
from app.models import Route

class Command(BaseCommand):
    help = 'Add sample bus routes'

    def handle(self, *args, **options):
        routes = [
            # North India Routes
            {
                'origin_city': 'Delhi',
                'destination_city': 'Mumbai',
                'origin_latitude': 28.6139,
                'origin_longitude': 77.2090,
                'destination_latitude': 19.0760,
                'destination_longitude': 72.8777,
            },
            {
                'origin_city': 'Delhi',
                'destination_city': 'Jaipur',
                'origin_latitude': 28.6139,
                'origin_longitude': 77.2090,
                'destination_latitude': 26.9124,
                'destination_longitude': 75.7873,
            },
            {
                'origin_city': 'Delhi',
                'destination_city': 'Agra',
                'origin_latitude': 28.6139,
                'origin_longitude': 77.2090,
                'destination_latitude': 27.1767,
                'destination_longitude': 78.0081,
            },
            {
                'origin_city': 'Delhi',
                'destination_city': 'Lucknow',
                'origin_latitude': 28.6139,
                'origin_longitude': 77.2090,
                'destination_latitude': 26.8467,
                'destination_longitude': 80.9462,
            },
            # South India Routes
            {
                'origin_city': 'Bangalore',
                'destination_city': 'Chennai',
                'origin_latitude': 12.9716,
                'origin_longitude': 77.5946,
                'destination_latitude': 13.0827,
                'destination_longitude': 80.2707,
            },
            {
                'origin_city': 'Bangalore',
                'destination_city': 'Hyderabad',
                'origin_latitude': 12.9716,
                'origin_longitude': 77.5946,
                'destination_latitude': 17.3850,
                'destination_longitude': 78.4867,
            },
            {
                'origin_city': 'Bangalore',
                'destination_city': 'Mysore',
                'origin_latitude': 12.9716,
                'origin_longitude': 77.5946,
                'destination_latitude': 12.2958,
                'destination_longitude': 76.6394,
            },
            {
                'origin_city': 'Chennai',
                'destination_city': 'Bangalore',
                'origin_latitude': 13.0827,
                'origin_longitude': 80.2707,
                'destination_latitude': 12.9716,
                'destination_longitude': 77.5946,
            },
            {
                'origin_city': 'Hyderabad',
                'destination_city': 'Bangalore',
                'origin_latitude': 17.3850,
                'origin_longitude': 78.4867,
                'destination_latitude': 12.9716,
                'destination_longitude': 77.5946,
            },
            # West India Routes
            {
                'origin_city': 'Mumbai',
                'destination_city': 'Pune',
                'origin_latitude': 19.0760,
                'origin_longitude': 72.8777,
                'destination_latitude': 18.5204,
                'destination_longitude': 73.8567,
            },
            {
                'origin_city': 'Mumbai',
                'destination_city': 'Ahmedabad',
                'origin_latitude': 19.0760,
                'origin_longitude': 72.8777,
                'destination_latitude': 23.0225,
                'destination_longitude': 72.5714,
            },
            {
                'origin_city': 'Mumbai',
                'destination_city': 'Goa',
                'origin_latitude': 19.0760,
                'origin_longitude': 72.8777,
                'destination_latitude': 15.3004,
                'destination_longitude': 73.8352,
            },
            {
                'origin_city': 'Pune',
                'destination_city': 'Mumbai',
                'origin_latitude': 18.5204,
                'origin_longitude': 73.8567,
                'destination_latitude': 19.0760,
                'destination_longitude': 72.8777,
            },
            {
                'origin_city': 'Goa',
                'destination_city': 'Bangalore',
                'origin_latitude': 15.3004,
                'origin_longitude': 73.8352,
                'destination_latitude': 12.9716,
                'destination_longitude': 77.5946,
            },
            # East India Routes
            {
                'origin_city': 'Kolkata',
                'destination_city': 'Delhi',
                'origin_latitude': 22.5726,
                'origin_longitude': 88.3639,
                'destination_latitude': 28.6139,
                'destination_longitude': 77.2090,
            },
            {
                'origin_city': 'Kolkata',
                'destination_city': 'Patna',
                'origin_latitude': 22.5726,
                'origin_longitude': 88.3639,
                'destination_latitude': 25.5941,
                'destination_longitude': 85.1376,
            },
            # More Popular Routes
            {
                'origin_city': 'Jaipur',
                'destination_city': 'Delhi',
                'origin_latitude': 26.9124,
                'origin_longitude': 75.7873,
                'destination_latitude': 28.6139,
                'destination_longitude': 77.2090,
            },
            {
                'origin_city': 'Ahmedabad',
                'destination_city': 'Mumbai',
                'origin_latitude': 23.0225,
                'origin_longitude': 72.5714,
                'destination_latitude': 19.0760,
                'destination_longitude': 72.8777,
            },
            {
                'origin_city': 'Lucknow',
                'destination_city': 'Delhi',
                'origin_latitude': 26.8467,
                'origin_longitude': 80.9462,
                'destination_latitude': 28.6139,
                'destination_longitude': 77.2090,
            },
            {
                'origin_city': 'Mysore',
                'destination_city': 'Bangalore',
                'origin_latitude': 12.2958,
                'origin_longitude': 76.6394,
                'destination_latitude': 12.9716,
                'destination_longitude': 77.5946,
            },
        ]

        for route_data in routes:
            route, created = Route.objects.get_or_create(
                origin_city=route_data['origin_city'],
                destination_city=route_data['destination_city'],
                defaults={
                    'origin_latitude': route_data['origin_latitude'],
                    'origin_longitude': route_data['origin_longitude'],
                    'destination_latitude': route_data['destination_latitude'],
                    'destination_longitude': route_data['destination_longitude'],
                }
            )
            status = "✓ Created" if created else "⚠ Already exists"
            self.stdout.write(f"{status}: {route_data['origin_city']} → {route_data['destination_city']}")