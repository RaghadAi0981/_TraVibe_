from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("country", "name")

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class Place(models.Model):
    CATEGORY_CHOICES = [
    ("hotel", "Hotel"),
    ("restaurant", "Restaurant"),
    ("cafe", "Coffee"),
    ("mountain", "Mountain"),
    ("nature", "Nature"),
    ("attraction", "Attraction"),
    ("coworking", "Coworking"),
    ]
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="places")
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    address = models.CharField(max_length=255, blank=True)
    maps_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    google_place_id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.name} ({self.city.name})"


class Rating(models.Model):
    GOOD_BAD_CHOICES = [("good", "Good"), ("bad", "Bad")]

    place = models.OneToOneField(Place, on_delete=models.CASCADE, related_name="rating")
    good_or_bad = models.CharField(max_length=10, choices=GOOD_BAD_CHOICES)

    elderly_score = models.PositiveSmallIntegerField(default=3)
    young_score = models.PositiveSmallIntegerField(default=3)
    work_score = models.PositiveSmallIntegerField(default=3)
    nature_score = models.PositiveSmallIntegerField(default=3)

    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.place.name} - {self.good_or_bad}"

# Run migrations (these will create tables inside Supabase):
# python3 manage.py makemigrations
# python3 manage.py migrate
# comeback later
# python3 -c "import dotenv; print('dotenv OK')"
# python3 -c "import psycopg2; print('psycopg2 OK')"
# cd /Users/ragedalharby/_TraVibe_/travel_project
# nano .env
# CTRL + O then Enter
# CTRL + X