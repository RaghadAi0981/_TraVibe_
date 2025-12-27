from django.contrib import admin
from .models import Country, City, Place, Rating

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Place)
admin.site.register(Rating)

# python3 manage.py createsuperuser
# python3 manage.py runserver
# later 3,4