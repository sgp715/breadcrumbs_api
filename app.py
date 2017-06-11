from flask import Flask
from flask_restful import Resource, Api, reqparse
import googlemaps
import json
from pprint import pprint
from datetime import datetime
import requests
import base64
import argparse


app = Flask(__name__)
api = Api(app)

with open("config.json") as config_file:
    config = json.load(config_file)

gmaps = googlemaps.Client(key=config["key"])

# class Coordinates(Resource):
#
#     def get(self):
#         address_parser = reqparse.RequestParser()
#         address_parser.add_argument("street_number", type=str, required=True)
#         address_parser.add_argument("street", type=str, required=True)
#         address_parser.add_argument("city", type=str, required=True)
#         address_parser.add_argument("state", type=str, required=True)
#         args = address_parser.parse_args()
#         address = ' '.join((args["street_number"],
#                             args["street"],
#                             args["city"],
#                             args["state"])
#                             )
#         goecoded = gmaps.geocode(address)
#         return goecoded

def get_location_crumbs(origin, destination):

    now = datetime.now()
    directions_result = gmaps.directions(origin,
                                     destination,
                                     mode="walking",
                                     departure_time=now)
    step = directions_result[0]["legs"][0]["steps"][0]

    return [ step["start_location"], step["end_location"] ]

def get_image_crumb(lat, lng, size="600x600"):

    base_url = "https://maps.googleapis.com/maps/api/streetview?"
    size= "size=" + size
    location = "location=" + str(lat) + ',' + str(lng)
    key = "key=" + config["key"]

    r = requests.get(base_url + '&'.join((size, location, key)))
    image = base64.b64encode(r.content)

    return image.decode("utf-8")

class Crumbs(Resource):

    def get(self):
        crumbs_parser = reqparse.RequestParser()
        crumbs_parser.add_argument("origin", type=str, required=True)
        crumbs_parser.add_argument("destination", type=str, required=True)
        crumbs_parser.add_argument("size", type=str, required=False)
        args = crumbs_parser.parse_args()

        location_crumbs = get_location_crumbs(args["origin"], args["destination"])

        print(location_crumbs)

        first_crumb = get_image_crumb(location_crumbs[0]["lat"], location_crumbs[0]["lng"])
        second_crumb = get_image_crumb(location_crumbs[1]["lat"], location_crumbs[1]["lng"])

        return { "images": { "first_crumb": first_crumb,
                             "second_crumb": second_crumb } }

# class Images(Resource):"
#
#     def get(self):
#         crumbs_parser = reqparse.RequestParser()
#         crumbs_parser.add_argument("size", type=str, required=False) # optionally specify size
#         crumbs_parser.add_argument("lat", type=str, required=True)
#         crumbs_parser.add_argument("long", type=str, required=True)
#         args = crumbs_parser.parse_args()
#
#         base_url = "https://maps.googleapis.com/maps/api/streetview?"
#         size= "size=" + args["size"]
#         location = "location=" + args["lat"] + ',' + args["long"]
#         key = "key=" + config["key"]
#
#         r = requests.get(base_url + '&'.join((size, location, key)))
#         image = base64.b64encode(r.content) # get the binary data and encode it
#         return { "image": image.decode("utf-8") }

base_api_url = "/api/v1"
api.add_resource(Crumbs, '/'.join((base_api_url,"crumbs")))
# api.add_resource(Coordinates, '/'.join((base_api_url, "coordinates")))
# api.add_resource(Coordinates, "/coordinates/<string:address>")
# api.add_resource(Images, '/'.join((base_api_url,"images")))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--production", help="run app in production", action="store_true")
    args = parser.parse_args()
    if args.production:
        app.run()
    else:
        app.run(debug="True")
