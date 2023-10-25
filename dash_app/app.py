import json
import base64
from aerofiles.igc import Reader
import io
import dash
from dash import Dash, dcc, html, Input, Output
import pydeck
import plotly.graph_objects as go
import requests
import datetime

app = dash.Dash(__name__)

pydeck.settings.token = 'pk.eyJ1Ijoic2lyLXZpdm9yIiwiYSI6ImNsanUxZzMwNzAyMjgzaW4xYnB3cnhrMjMifQ.VwQFf-qVUlkZQhkC7V4qog'
api_url = 'https://alp65prlv8.execute-api.eu-central-1.amazonaws.com/default/igc-file'

# Function for processing the IGC file
def process_igc_file(api_url, data):
    date = data['comment_records'][1][1]['comment'][11:21]
    gps_data = data['fix_records'][1]

    response = requests.get(f'{api_url}/{date}', data=data, headers={"Content-Type": "application/octet-stream"}, verify=False)
    response.raise_for_status()  # Check for success status

    # Generate GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": []
                }
            }
        ]
    }

    for i in gps_data:
        if all(key in i for key in ['lon', 'lat', 'gps_alt']):
            lon = i['lon']
            lat = i['lat']
            gps_alt = i['gps_alt']
            geojson["features"][0]["geometry"]["coordinates"].append([lon, lat, gps_alt])
    return geojson, data

# Function for loading initial view state
def get_initial_view_state(geojson):
    if geojson.get("features"):
        gps_start_lat = geojson["features"][0]["geometry"]["coordinates"][0][1]
        gps_start_lon = geojson["features"][0]["geometry"]["coordinates"][0][0]
    else:
        # Default values if GeoJSON is empty
        gps_start_lat, gps_start_lon = 0.0, 0.0
    return gps_start_lat, gps_start_lon

# Function to create altitude figure
def create_altitude_fig(geojson, data):
    if geojson and geojson.get("features") and len(geojson["features"]) > 0:
        altitude_data = [point[2] for point in geojson["features"][0]["geometry"]["coordinates"]]
        time_values = [entry['time'].strftime('%H:%M:%S') for entry in data['fix_records'][1]]
        fig = go.Figure(data=go.Scatter(y=altitude_data, x=time_values))
        fig.update_layout(title="Altitude Line Chart", xaxis_title="Time", yaxis_title="Altitude")
        fig.update_xaxes(tickangle=65)
    else:
        # Create a default altitude figure if geojson data is not valid
        altitude_data = [0]
        time_values = [""]
        fig = go.Figure(data=go.Scatter(y=altitude_data, x=time_values))
        fig.update_layout(xaxis_title="Time", yaxis_title="Altitude")
        fig.update_xaxes(tickangle=65)
    return fig

# Upload component for Drag & Drop
upload_component = dcc.Upload(
    id='upload-data',
    children=html.Div([
        'Drag and Drop or ',
        html.A('Select Files')
    ]),
    style={
        'fontFamily': 'Georgia, serif',
        'fontSize': '25px',
        'width': '50%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '5px',
        'borderStyle': 'solid',
        'borderRadius': '20px',
        'textAlign': 'center',
        'margin': '10px auto',
    },
    # Allowed file types
    multiple=True
)

# Putting the deck component and the graph in separate divs within cards
app.layout = html.Div(
    children=[
        upload_component,
        html.Div(
            className="card",
            style={
                "height": "500px",
                "overflow": "hidden"
            },
            children=[
                html.H3(
                    "Altitude Line Chart",
                    style={
                        "fontFamily": "Georgia, serif",
                        "textAlign": "center",
                    }),
                dcc.Graph(id='altitude-graph'),
            ],
        ),
        html.Div(
            className="card",
            style={
                "height": "500px",
                "overflow": "hidden",
                "display": "flex",
                "flexDirection": "column",
                "align-items": "center",
                "justifyContent": "center"
            },
            children=[
                html.H3(
                    "Map", style={
                        "fontFamily": "Georgia, serif",
                        "textAlign": "center",
                        "marginBottom": "10px"
                    }),
                html.Iframe(
                    id='deck-gl',
                    srcDoc="",
                    sandbox="allow-scripts allow-popups allow-same-origin allow-top-navigation allow-forms",
                    style={
                        "width": "95%",
                        "height": "95%",
                        "margin": "auto",
                    },
                ),
            ],
        ),
    ],
    className="container",
)

# Callback to process the uploaded file
@app.callback(
    Output('deck-gl', 'srcDoc'),
    Output('altitude-graph', 'figure'),
    Input('upload-data', 'contents')
)

def update_deck(contents_list):
    if contents_list is not None and len(contents_list) > 0:
        content_string = contents_list[0].split(',')[1]
        decoded = base64.b64decode(content_string).decode()

        igc_file_content = Reader().read(io.StringIO(decoded))
        date_string = igc_file_content['comment_records'][1][1]['comment'][11:21]
        date_string_to_object = datetime.datetime.strptime(date_string, "%Y-%m-%d")#.strftime('%d.%m.%Y')
        date = date_string_to_object.strftime('%d.&m.&Y')

        # Process the uploaded file
        response = requests.post(api_url, data=decoded, params={'date': date})
        response.raise_for_status()  # Check for success status
        geojson, data = process_igc_file(api_url, igc_file_content)  # Update the IGC file content
        lat_lon = get_initial_view_state(geojson)
        print(lat_lon)
        altitude_fig = create_altitude_fig(geojson, data)

    # Create the updated Deck component
        geojson_layer = pydeck.Layer(
            "GeoJsonLayer",
            data=geojson,
            get_line_color=[255, 0, 0],
            get_line_width=1.5,
            line_width_scale=10,
            opacity=0.8,
            filled=True
        )

        INITIAL_VIEW_STATE = pydeck.ViewState(
            latitude=lat_lon[0], longitude=lat_lon[1], zoom=12, max_zoom=16, pitch=55, bearing=180
        )

        r = pydeck.Deck(
            layers=[geojson_layer],
            initial_view_state=INITIAL_VIEW_STATE,
            api_keys={
                "mapbox": "pk.eyJ1Ijoic2lyLXZpdm9yIiwiYSI6ImNsanUxZzMwNzAyMjgzaW4xYnB3cnhrMjMifQ.VwQFf-qVUlkZQhkC7V4qog"
            },
            map_style="satellite",
            map_provider="mapbox"
        )

        deck_code = r.to_html(as_string=True)  # Convert DeckGL object to HTML

        return deck_code, altitude_fig
    else:
        return None, create_altitude_fig([], [])


if __name__ == '__main__':
    app.run_server(debug=True)
