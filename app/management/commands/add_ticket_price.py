from django.core.management.base import BaseCommand
from app.models import Bus

class Command(BaseCommand):
    help = 'Update missing prices for buses in the database'

    def handle(self, *args, **options):
        # Define price mapping for buses that are missing prices
        price_map = {
            'Royal Rider': 2000,
            'Night Falcon': 1500,
            'Emerald Voyager': 1200,
            'Night Rider': 1800,
            'Shatabdi Express': 1500,
            'Royal Travels': 1200,
            'Kesari Tours': 1300,
            'VRL Travels': 1400,
            'SRS Travels': 1600,
            'Sharma Tours': 1700,
            'Redbus Partners': 1400,
            'First Class Travel': 1300,
            'Budget Express': 1800,
            'Economy Travel': 1900,
            'Local Express': 2000,
            'City Transport': 2100,
            'Night Runner Sleeper': 800,
            'Comfort Sleep Express': 900,
            'Dream Journey': 750,
            'Rapid Transport': 1650,
            'Star Travels': 1100,
            'Green Transport': 2200,
            'Jet Airways Bus': 1000,
            'Mountain Explorer': 1500,
        }

        updated_count = 0
        missing_count = 0

        for bus_name, price in price_map.items():
            try:
                bus = Bus.objects.get(name=bus_name)
                
                # Check if price is missing (null or 0)
                if not bus.price or bus.price == 0:
                    bus.price = price
                    bus.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"✓ Updated: {bus.name} - Price: ₹{price}")
                    )
                else:
                    self.stdout.write(f"⚠ Already has price: {bus.name} - ₹{bus.price}")
                    
            except Bus.DoesNotExist:
                missing_count += 1
                self.stdout.write(
                    self.style.WARNING(f"✗ Bus not found: {bus_name}")
                )

        self.stdout.write(self.style.SUCCESS(f'\n✓ Update completed!'))
        self.stdout.write(f"  Updated: {updated_count} buses")
        self.stdout.write(f"  Not found: {missing_count} buses")