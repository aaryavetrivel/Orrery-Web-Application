import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objs as go
import requests
import numpy as np
import google.generativeai as genai

# Configure the Gemini client with your API key
genai.configure(api_key="AIzaSyBIT4jc4-dfO8zoffUrCYKqhwuJer6TuTY")  # Use the API key directly

# Function to calculate orbital positions for NEOs
def calculate_orbital_positions(neo, theta):
    try:
        if 'orbital_data' not in neo:
            return None

        a = float(neo['orbital_data'].get('semi_major_axis', 0))
        e = float(neo['orbital_data'].get('eccentricity', 0))
        i = np.radians(float(neo['orbital_data'].get('inclination', 0)))
        omega = np.radians(float(neo['orbital_data'].get('argument_of_periapsis', 0)))
        Omega = np.radians(float(neo['orbital_data'].get('ascending_node_longitude', 0)))

        if a == 0:
            return None

        x_prime = a * (np.cos(theta) - e)
        y_prime = a * np.sqrt(1 - e ** 2) * np.sin(theta)

        x = (x_prime * (np.cos(Omega) * np.cos(omega) - np.sin(Omega) * np.sin(omega) * np.cos(i))
              - y_prime * (np.cos(Omega) * np.sin(omega) + np.sin(Omega) * np.cos(omega) * np.cos(i)))
        y = (x_prime * (np.sin(Omega) * np.cos(omega) + np.cos(Omega) * np.sin(omega) * np.cos(i))
              + y_prime * (np.sin(Omega) * np.sin(omega) - np.cos(Omega) * np.cos(omega) * np.cos(i)))
        z = (x_prime * np.sin(i) * np.sin(omega) + y_prime * np.sin(i) * np.cos(omega))

        return x, y, z

    except (KeyError, ValueError) as e:
        return None

# Function to calculate positions for planets
def calculate_planet_positions(planet_data, theta):
    a = planet_data["a"]
    x = a * np.cos(theta)
    y = a * np.sin(theta)
    z = 0
    return x, y, z

# NASA API endpoint for Near-Earth Objects
neo_url = "https://api.nasa.gov/neo/rest/v1/neo/browse"
params = {'api_key': 'XQXoQBRcfOiCUxMJCwb1HVUxzI4PNhQmICskpYSy', 'size': 20}
response = requests.get(neo_url, params=params)

near_earth_objects = []  # Initialize the near_earth_objects list
if response.status_code == 200:
    data = response.json()
    near_earth_objects.extend(data['near_earth_objects'])
    print(f"Retrieved {len(near_earth_objects)} NEOs.")  # Confirmation output
else:
    print("Failed to fetch NEO data:", response.status_code)

# Define planetary data (semi-major axis in AU)
planets = {
    "Mercury": {"a": 0.39, "color": "gray"},
    "Venus": {"a": 0.72, "color": "orange"},
    "Earth": {"a": 1.00, "color": "blue"},
    "Mars": {"a": 1.52, "color": "tan"},
    "Jupiter": {"a": 5.20, "color": "brown"},
    "Saturn": {"a": 9.58, "color": "gold"},
    "Uranus": {"a": 19.18, "color": "lightblue"},
    "Neptune": {"a": 30.07, "color": "darkblue"}
}

# Create Dash app
app = dash.Dash(__name__)

# Create a list to hold the names of celestial bodies for reference
celestial_body_names = []

# Function to fetch detailed NEO data
def fetch_neo_details(neo_id):
    neo_url = f"https://api.nasa.gov/neo/rest/v1/neo/{neo_id}?api_key=XQXoQBRcfOiCUxMJCwb1HVUxzI4PNhQmICskpYSy"
    response = requests.get(neo_url)
    return response.json() if response.status_code == 200 else None

# Function to format NEO data for Gemini
def format_neo_data(neo):
    data = {
        "name": neo.get('name', 'Unknown'),
        "diameter": neo['estimated_diameter']['meters']['estimated_diameter_max'],  # Max diameter in meters
        "miss_distance": neo['close_approach_data'][0]['miss_distance']['kilometers'],  # Distance in km
        "hazardous": neo['is_potentially_hazardous_asteroid'],
        "orbital_data": neo['orbital_data'],
    }
    return data

# Create the initial figure
def create_figure(theta_offset=0):
    orbit_data = []
    point_data = []
    num_points = 500
    theta_orbit = np.linspace(0, 2 * np.pi, num_points)

    # Plot planetary orbits
    for planet_name, planet_data in planets.items():
        x_orbit = planet_data["a"] * np.cos(theta_orbit + theta_offset)
        y_orbit = planet_data["a"] * np.sin(theta_orbit + theta_offset)
        z_orbit = np.zeros_like(x_orbit)

        orbit_data.append(go.Scatter3d(
            x=x_orbit, y=y_orbit, z=z_orbit, mode='lines',
            line=dict(color=planet_data["color"], width=3),
            name=f"{planet_name} Orbit"
        ))

        x, y, z = calculate_planet_positions(planet_data, theta_offset)
        point_data.append(go.Scatter3d(
            x=[x], y=[y], z=[z], mode='markers',
            marker=dict(size=8, color=planet_data["color"]),
            name=planet_name, hoverinfo='text', text=planet_name  # Add hover info here
        ))

        # Store the planet name
        celestial_body_names.append(planet_name)

    # Plot NEOs
    for neo in near_earth_objects:
        x_positions, y_positions, z_positions = [], [], []

        for theta in theta_orbit:
            position = calculate_orbital_positions(neo, theta + theta_offset)
            if position is not None:
                x_positions.append(position[0])
                y_positions.append(position[1])
                z_positions.append(position[2])

        if len(x_positions) > 0:
            neo_name = neo.get('name', 'Unknown')  # Get the name for hover info
            # Check if the NEO is a Potentially Hazardous Asteroid (PHA)
            color = 'red' if neo.get('is_potentially_hazardous_asteroid', False) else 'yellow'

            orbit_data.append(go.Scatter3d(
                x=x_positions, y=y_positions, z=z_positions, mode='lines',
                line=dict(color=color, width=2),
                name=neo_name + " Orbit"
            ))

            # Latest position
            latest_position = calculate_orbital_positions(neo, theta_orbit[-1] + theta_offset)
            if latest_position is not None:
                point_data.append(go.Scatter3d(
                    x=[latest_position[0]], y=[latest_position[1]], z=[latest_position[2]],
                    mode='markers', marker=dict(size=5, color=color),
                    name='Latest ' + neo_name,
                    hoverinfo='text', text=neo_name  # Set the hover info here
                ))

                # Store the NEO name
                celestial_body_names.append(neo_name)

    # Add the Sun at the center
    orbit_data.append(go.Scatter3d(
        x=[0], y=[0], z=[0], mode='markers',
        marker=dict(size=20, color='yellow'), name='Sun'
    ))

    layout = go.Layout(
        scene=dict(
            xaxis=dict(title="X (AU)", backgroundcolor="black", gridcolor="gray"),
            yaxis=dict(title="Y (AU)", backgroundcolor="black", gridcolor="gray"),
            zaxis=dict(title="Z (AU)", backgroundcolor="black", gridcolor="gray"),
            bgcolor='black'
        ),
        title="Asteroid and Planetary Orbits",
        legend=dict(x=0, y=1)
    )

    return go.Figure(data=orbit_data + point_data, layout=layout)

# Layout of the app
app.layout = html.Div([
    html.H1("Interactive Orrery"),
    dcc.Graph(id='orrery'),
    html.Button("Start Animation", id='start-button', n_clicks=0),
    html.Button("Stop Animation", id='stop-button', n_clicks=0),
    dcc.Interval(id='interval', interval=100, disabled=True),
    dcc.Slider(id='speed-slider', min=1, max=10, value=5, marks={i: str(i) for i in range(1, 11)}, step=1),
    html.Div(id='info', style={'margin-top': '20px'})
])

# Callback for updating the figure and displaying information
@app.callback(
    Output('orrery', 'figure'),
    Output('info', 'children'),
    Input('interval', 'n_intervals'),
    Input('start-button', 'n_clicks'),
    Input('stop-button', 'n_clicks'),
    Input('speed-slider', 'value'),
    Input('orrery', 'clickData'),
    State('interval', 'disabled')
)
def update_orrery(n_intervals, start_clicks, stop_clicks, speed_value, clickData, interval_disabled):
    try:
        ctx = dash.callback_context

        if n_intervals is None:
            n_intervals = 0

        speed = 1000 // speed_value  # Adjust speed based on slider
        theta_offset = n_intervals * (0.05 * speed_value)  # Calculate theta offset based on intervals

        # Create figure with updated positions
        figure = create_figure(theta_offset)

        # Handle button clicks
        if ctx.triggered:
            if 'start-button' in ctx.triggered[0]['prop_id']:
                pass
            elif 'stop-button' in ctx.triggered[0]['prop_id']:
                return figure, "Animation Stopped"

        # Handle click events to display info about celestial bodies
        if clickData:
            curve_number = clickData['points'][0]['curveNumber']
            if curve_number < len(celestial_body_names):
                name = celestial_body_names[curve_number]
                neo_id = near_earth_objects[curve_number - len(planets)]['id'] if curve_number >= len(planets) else None

                if neo_id:
                    neo_details = fetch_neo_details(neo_id)
                    if neo_details:
                        model = genai.GenerativeModel("gemini-1.5-flash")
                        response = model.generate_content(f"Provide detailed information about {name}. Clearly and concisely.")
                        additional_info = response.text if response else "No additional info available."
                        return figure, f"You clicked on: {name}\n{additional_info}"

        return figure, "Click on a celestial body for more information."

    except Exception as e:
        print(f"Error in update_orrery: {e}")
        return create_figure(), "Error occurred."

# Run the app   
if __name__ == '__main__':
    app.run_server(debug=False)
    