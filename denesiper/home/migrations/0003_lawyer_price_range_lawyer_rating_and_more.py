# Generated by Django 5.1.3 on 2024-12-30 20:53

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_lawyer_photo_alter_lawyer_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawyer',
            name='price_range',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='lawyer',
            name='rating',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AddField(
            model_name='lawyer',
            name='years_of_experience',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=100)),
                ('review_text', models.TextField()),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('lawyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='home.lawyer')),
            ],
        ),
    ]