from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import geolocate, nearest_major_location, reverse_geocode

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        address1 = request.form.get("address1")
        address2 = request.form.get("address2")
        if not address1 or not address2:
            return redirect("/")

        addresses = [address1, address2]
        if len(addresses) > 6:
            flash("Please limit the number of addresses to 6.")
            return redirect("/")

        counter = 3

        while True:
            additional_address = request.form.get(f"address{counter}")
            if not additional_address:
                break
            addresses.append(additional_address)
            counter += 1

        coordinates = []
        for address in addresses:
            geolocation = geolocate(address)
            if "error" in geolocation:
                flash(f"Address '{address}' not found")
                return redirect("/")
            #latitude and longitude of address
            coordinates.append((geolocation["lat"], geolocation["lng"]))


        #calculate midpoint
        midpoint_lat = sum(lat for lat, lng in coordinates) / len(coordinates)
        midpoint_lng = sum(lng for lat, lng in coordinates) / len(coordinates)
        midpoint = {"lat": midpoint_lat, "lng": midpoint_lng}

        nearest_location = nearest_major_location(midpoint_lat, midpoint_lng)

        major_location = reverse_geocode(midpoint_lat, midpoint_lng)

        return render_template("midpoint.html", midpoint=midpoint, addresses=addresses, major_location=major_location)
    else:
        return render_template("index.html")


@app.route("/activities", methods=["GET", "POST"])
def activities():
    major_location = request.args.get("major_location")
    if not major_location:
        return "Nearest location not found in session!", 400
    return render_template("activities.html", major_location=major_location)

