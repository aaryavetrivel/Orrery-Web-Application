# Orrery Web App that Displays Near-Earth Objects

## Description
This interactive orrery web app visualizes the orbits of celestial bodies, including planets and Near-Earth Objects (NEOs), in a dynamic 3D environment. Utilizing data from NASA's Near-Earth Object API, the app calculates and displays the positions of these bodies relative to the Sun, allowing users to explore their movements and characteristics. The orrery is designed to educate users about our solar system and promote awareness of NEOs, including potentially hazardous asteroids. With user-friendly controls, you can start and stop animations, adjust the speed of orbits, and click on celestial bodies for detailed information.

## Installation Instructions

1. **Download and Install Python**: 
   - Go to the [official Python website](https://www.python.org/downloads/) and download the latest version of Python.
   - Follow the installation instructions for your operating system.

2. **Obtain Your Gemini API Key**:
   - Visit the [Gemini API documentation](https://ai.google.dev/gemini-api/docs/api-key) to sign up for an API key.
   - After obtaining your API key, copy it to your clipboard.

3. **Configure the API Key**:
   - Open the `main.py` script in a code editor.
   - Locate the line that says:
     ```python
     genai.configure(api_key="API_KEY")  # Use the API key directly
     ```
   - Replace `"API_KEY"` with your actual API key, so it looks like this:
     ```python
     genai.configure(api_key="YOUR_ACTUAL_API_KEY")
     ```

4. **Install Required Modules**:
   - To install the necessary libraries, run the following command in your terminal:
     ```bash
     pip install -r requirements.txt
     ```

5. **Run the Program**:
   - Save your changes to the `main.py` script.
   - Open a terminal or command prompt, navigate to the directory containing `main.py`, and run the program using the command:
     ```
     python main.py
     ```
   - After the program starts, open the link provided in the terminal to access the Orrery Web App.

By following these steps, you'll be ready to explore the interactive orrery and learn about celestial bodies! 🌌🚀

## Usage

To use the Orrery Web App:

1. **Start the App**: Run the app by executing the main Python script. Ensure all dependencies are installed as per the installation instructions.

2. **Explore the 3D Environment**:
   - **Animation Controls**: Use the **"Start Animation"** button to begin the animation of celestial bodies orbiting the Sun. Click **"Stop Animation"** to pause.
   - **Adjust Speed**: Move the **speed slider** to change the speed of the orbits. The range is from 1 (slowest) to 10 (fastest).

3. **Interact with Celestial Bodies**:
   - Click on any celestial body (planets or NEOs) in the 3D space. This will display detailed information about that body, including its name, size, and other relevant characteristics.
   - Potentially Hazardous Asteroids (PHAs) will be highlighted in red.

4. **Visualize Orbits**: Observe the orbits of planets and NEOs around the Sun, helping you understand their relative positions and movements.

5. **Learn More**: The app provides a unique opportunity to learn about the solar system and the significance of NEOs in our environment.

## Sources and Citations

### Libraries Used
1. **Dash**: [Dash Documentation](https://dash.plotly.com/)
2. **Plotly**: [Plotly Graphing Library](https://plotly.com/python/)
3. **NumPy**: [NumPy Documentation](https://numpy.org/doc/stable/)
4. **Requests**: [Requests Documentation](https://docs.python-requests.org/en/latest/)
5. **Google Generative AI**: [Google Generative AI](https://cloud.google.com/generative-ai/docs)

### Datasets
1. **NASA Near-Earth Object Data**: [NASA NEO API](https://api.nasa.gov/neo/)
2. **Small Body Database**: [NASA Small Body Database](https://ssd.jpl.nasa.gov/sbdb_query.cgi)

### Tutorials and Examples
1. **Creating Interactive Dash Apps**: [Dash Tutorial](https://dash.plotly.com/)
2. **3D Visualization with Plotly**: [3D Scatter Plot Documentation](https://plotly.com/python/3d-scatter-plots/)
3. **Orbital Mechanics Basics**: [NASA Kepler’s Laws](https://solarsystem.nasa.gov/planets/overview/)
