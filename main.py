from pyproj import Proj, transform
import folium
from folium import plugins
from folium.plugins import Geocoder

from flask import Flask, render_template
from FlightRadar24 import FlightRadar24API


app = Flask(__name__, static_url_path='/static', template_folder='templates')


before = Proj(init='epsg:4326')
after = Proj(init='epsg:3857')


class FrAPIHandler(FlightRadar24API):

    def __init__(self):
        print(FlightRadar24API)
        self.fr_api = FlightRadar24API()
        self.flights = self.fr_api.get_flights()

    def frapi_now_flight_position(self) -> list:
        coordinates = []
        for i in self.flights:
            coord = transform(before, after, i.longitude, i.latitude)
            # print(coord)
            coordinates.append([coord[0], coord[1]])
        return coordinates

    def frapi_now_path_flight_line(self, flight) -> dict:

        return self.fr_api.get_flight_details(flight)

    def fr_handling(self, m):
        fr_group = folium.FeatureGroup(name='FlightRadar', show=False).add_to(m)

        position_results = self.frapi_now_flight_position()
        for postion in position_results:
            marker = folium.Marker(
                location=[postion.latitude, postion.longitude],
                tooltip=f"""
                항공기명: {postion.registration}
                aircraft_code: {postion.aircraft_code}
                고도: {postion.altitude}
                ground_speed: {postion.ground_speed}
                """,
                # popup = f'<input type="text" value=" id="myInput"><button onclick="myFunction()">Copy location</button>',
                icon=plugins.BeautifyIcon(
                    icon='plane',
                    border_color='transparent',
                    background_color='transparent',
                    border_width=1,
                    text_color='#003EFF',
                    inner_icon_style='margin:0px;font-size:2em;transform: rotate({0}deg);'.format(postion.heading)
                )
            )
            # marker.add_child(folium.Popup("헤헤"))
            marker.add_to(fr_group)


@app.route('/')
def main():
    value_list = FrAPIHandler().frapi_now_flight_position()
    return render_template('marker.html', values=value_list)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
