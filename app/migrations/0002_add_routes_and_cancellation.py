# Generated migration for adding Route model and booking status fields

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        # Create Route model
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_city', models.CharField(max_length=100)),
                ('destination_city', models.CharField(max_length=100)),
                ('origin_latitude', models.FloatField(blank=True, null=True)),
                ('origin_longitude', models.FloatField(blank=True, null=True)),
                ('destination_latitude', models.FloatField(blank=True, null=True)),
                ('destination_longitude', models.FloatField(blank=True, null=True)),
            ],
        ),
        
        # Add unique constraint to Route
        migrations.AlterUniqueTogether(
            name='route',
            unique_together={('origin_city', 'destination_city')},
        ),
        
        # Add route field to Bus
        migrations.AddField(
            model_name='bus',
            name='route',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.route'),
        ),
        
        # Update Booking model - remove old payment_status choices, add status and refund fields
        migrations.RemoveField(
            model_name='booking',
            name='payment_status',
        ),
        
        migrations.AddField(
            model_name='booking',
            name='payment_status',
            field=models.CharField(
                choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')],
                default='pending',
                max_length=20
            ),
        ),
        
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(
                choices=[('BOOKED', 'Booked'), ('CANCELLED', 'Cancelled'), ('REFUNDED', 'Refunded')],
                default='BOOKED',
                max_length=20
            ),
        ),
        
        migrations.AddField(
            model_name='booking',
            name='refund_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        
        migrations.AddField(
            model_name='booking',
            name='refund_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        
        migrations.AddField(
            model_name='booking',
            name='refund_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        
        migrations.AddField(
            model_name='booking',
            name='cancellation_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
