import requests
from django.shortcuts import render, get_object_or_404
from .models import Country, City, Place
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect


def countries_list(request):
    countries = Country.objects.all().order_by("name")
    return render(request, "countries.html", {"countries": countries})


def cities_list(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    cities = country.cities.all().order_by("name")
    return render(request, "cities.html", {
        "country": country,
        "cities": cities
    })


def places_list(request, city_id):
    city = get_object_or_404(City, id=city_id)
    places = city.places.select_related("rating").all()

    # ✅ Search (by place name)
    q = request.GET.get("q", "").strip()
    if q:
        places = places.filter(name__icontains=q)

    # ✅ Filters
    if request.GET.get("nature"):
        places = places.filter(category="nature")

    if request.GET.get("good"):
        places = places.filter(rating__good_or_bad="good")

    if request.GET.get("elderly"):
        places = places.filter(rating__elderly_score__gte=4)

    if request.GET.get("work"):
        places = places.filter(rating__work_score__gte=4)

    context = {
        "city": city,
        "places": places,
        "q": q,  # pass back to template to keep input filled
    }
    return render(request, "places.html", context)


def place_detail(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    return render(request, "place_detail.html", {"place": place})
def nominatim_search(query: str):
    """
    Search OpenStreetMap Nominatim.
    IMPORTANT: Nominatim requires a valid User-Agent.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "addressdetails": 1,
        "limit": 10,
    }
    headers = {
        "User-Agent": "TraVibe-Django/1.0 (local-dev)",
        "Accept-Language": "en",
    }
    r = requests.get(url, params=params, headers=headers, timeout=10)
    r.raise_for_status()
    return r.json()


def add_place_search(request, city_id):
    city = get_object_or_404(City, id=city_id)

    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "attraction")

    results = []
    error = None

    # GET: search results
    if q:
        try:
            # Add city + country to improve search accuracy
            full_query = f"{q}, {city.name}, {city.country.name}"
            results = nominatim_search(full_query)
        except Exception as e:
            error = str(e)

    # POST: save selected result as a Place
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        lat = request.POST.get("lat", "").strip()
        lon = request.POST.get("lon", "").strip()
        display_name = request.POST.get("display_name", "").strip()
        category_post = request.POST.get("category", "attraction").strip()

        if not name or not lat or not lon:
            messages.error(request, "Missing location data. Please try again.")
            return redirect(reverse("add_place", args=[city.id]))

        # Create a maps link (OpenStreetMap)
        maps_url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=17/{lat}/{lon}"

        place = Place.objects.create(
            city=city,
            name=name,
            category=category_post,
            address=display_name[:255],
            latitude=lat,
            longitude=lon,
            maps_url=maps_url,
        )

        messages.success(request, f"Saved: {place.name}")
        return redirect("place_detail", place_id=place.id)

    return render(request, "add_place.html", {
        "city": city,
        "q": q,
        "category": category,
        "results": results,
        "error": error,
    })


def edit_place_location(request, place_id):
    place = get_object_or_404(Place, id=place_id)

    q = request.GET.get("q", "").strip()
    results = []
    error = None

    if q:
        try:
            full_query = f"{q}, {place.city.name}, {place.city.country.name}"
            results = nominatim_search(full_query)
        except Exception as e:
            error = str(e)

    if request.method == "POST":
        lat = request.POST.get("lat", "").strip()
        lon = request.POST.get("lon", "").strip()
        display_name = request.POST.get("display_name", "").strip()

        if not lat or not lon:
            messages.error(request, "Missing lat/lon. Please try again.")
            return redirect("edit_place_location", place_id=place.id)

        place.latitude = lat
        place.longitude = lon
        place.address = display_name[:255]
        place.maps_url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=17/{lat}/{lon}"
        place.save()

        messages.success(request, "Location updated.")
        return redirect("place_detail", place_id=place.id)

    return render(request, "edit_location.html", {
        "place": place,
        "q": q,
        "results": results,
        "error": error,
    })
def nominatim_search(query: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "addressdetails": 1,
        "limit": 10,
    }
    headers = {
        "User-Agent": "TraVibe-Django/1.0 (local-dev)",
        "Accept-Language": "en",
    }
    r = requests.get(url, params=params, headers=headers, timeout=10)
    r.raise_for_status()
    return r.json()


def add_place_search(request, city_id):
    city = get_object_or_404(City, id=city_id)

    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "attraction").strip()

    results = []
    error = None

    # GET: search results
    if q and request.method == "GET":
        try:
            full_query = f"{q}, {city.name}, {city.country.name}"
            results = nominatim_search(full_query)
        except Exception as e:
            error = str(e)

    # POST: save selected result
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        lat = request.POST.get("lat", "").strip()
        lon = request.POST.get("lon", "").strip()
        display_name = request.POST.get("display_name", "").strip()
        category_post = request.POST.get("category", "attraction").strip()

        if not name or not lat or not lon:
            messages.error(request, "Missing location data. Please try again.")
            return redirect("add_place", city_id=city.id)

        maps_url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=17/{lat}/{lon}"

        place = Place.objects.create(
            city=city,
            name=name[:150],
            category=category_post,
            address=display_name[:255],
            latitude=lat,
            longitude=lon,
            maps_url=maps_url,
        )

        messages.success(request, f"Saved: {place.name}")
        return redirect("place_detail", place_id=place.id)

    return render(request, "add_place.html", {
        "city": city,
        "q": q,
        "category": category,
        "results": results,
        "error": error,
    })


def edit_place_location(request, place_id):
    place = get_object_or_404(Place, id=place_id)

    q = request.GET.get("q", "").strip()
    results = []
    error = None

    if q and request.method == "GET":
        try:
            full_query = f"{q}, {place.city.name}, {place.city.country.name}"
            results = nominatim_search(full_query)
        except Exception as e:
            error = str(e)

    if request.method == "POST":
        lat = request.POST.get("lat", "").strip()
        lon = request.POST.get("lon", "").strip()
        display_name = request.POST.get("display_name", "").strip()

        if not lat or not lon:
            messages.error(request, "Missing lat/lon. Please try again.")
            return redirect("edit_place_location", place_id=place.id)

        place.latitude = lat
        place.longitude = lon
        place.address = display_name[:255]
        place.maps_url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=17/{lat}/{lon}"
        place.save()

        messages.success(request, "Location updated.")
        return redirect("place_detail", place_id=place.id)

    return render(request, "edit_location.html", {
        "place": place,
        "q": q,
        "results": results,
        "error": error,
    })
