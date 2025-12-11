import requests
from django.shortcuts import render, redirect
from .models import Favorite
from datetime import datetime
import zoneinfo

def index(request):
    classification = request.GET.get("classification", "")
    city = request.GET.get("city", "")
    events = []
    error = ""

    if classification or city:
        url = "https://app.ticketmaster.com/discovery/v2/events.json"
        params = {
            "apikey": "4yf4goLdxhVQWXiEtNDf0tiQjoYrzGsG",
            "classificationName": classification,
            "city": city,
            "size": 50
        }
        response = requests.get(url, params=params)
        data = response.json()

        if "_embedded" not in data:
            error = "No events found for your search."
        else:
            eastern = zoneinfo.ZoneInfo("America/New_York")

            for e in data["_embedded"]["events"]:
                name = e.get("name", "")
                images = e.get("images", [])
                image = images[0]["url"] if images else ""
                url_tickets = e.get("url", "")

                venue = e["_embedded"]["venues"][0]
                venue_name = venue.get("name", "")
                address = venue.get("address", {}).get("line1", "")
                city_name = venue.get("city", {}).get("name", "")
                state = venue.get("state", {}).get("stateCode", "")

                date_info = e.get("dates", {}).get("start", {})
                date_str = date_info.get("dateTime", "")
                if date_str:
                    utc_time = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                    local_time = utc_time.astimezone(eastern)
                    day = local_time.strftime("%a")
                    date_fmt = local_time.strftime("%b %d, %Y")
                    time_fmt = local_time.strftime("%I:%M %p")
                else:
                    day = ""
                    date_fmt = ""
                    time_fmt = ""

                events.append({
                    "id": e.get("id", ""),
                    "name": name,
                    "image": image,
                    "url": url_tickets,
                    "venue": venue_name,
                    "address": address,
                    "city": city_name,
                    "state": state,
                    "day": day,
                    "date": date_fmt,
                    "time": time_fmt
                })

    fav_ids = set(Favorite.objects.values_list("event_id", flat=True))

    return render(request, "index.html", {
        "events": events,
        "favorites": fav_ids,
        "error": error
    })


def add_favorite(request):
    if request.method == "POST":
        Favorite.objects.get_or_create(
            event_id=request.POST["event_id"],
            defaults={
                "name": request.POST["name"],
                "image": request.POST["image"],
                "url": request.POST["url"],
                "venue": request.POST["venue"],
                "address": request.POST["address"],
                "city": request.POST["city"],
                "state": request.POST["state"],
                "day": request.POST["day"],
                "date": request.POST["date"],
                "time": request.POST["time"]
            }
        )
    return redirect("index")


def remove_favorite(request, event_id):
    Favorite.objects.filter(event_id=event_id).delete()
    return redirect("index")


def update_favorite(request, event_id):
    if request.method == "POST":
        note = request.POST.get("note", "")
        Favorite.objects.filter(event_id=event_id).update(note=note)
    return redirect("favorites")


def favorites(request):
    favs = Favorite.objects.all()
    return render(request, "favorites.html", {"favorites": favs})
