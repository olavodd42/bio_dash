# Bio Dash: National Park Species Observations

A Dash web application that visualizes biodiversity data across national parks, allowing users to explore species observations and conservation statuses through interactive charts.

## Overview

Bio Dash provides a visual interface to explore and analyze species observation data across various national parks. The application allows filtering by park and species category, displaying information through intuitive charts and visualizations.

## Features

- **Interactive Filtering**: Select one or multiple parks and filter by species categories
- **Visual Data Exploration**: View species observations across three visualization types:
  - Observations per species with conservation status highlighting
  - Conservation status distribution through pie charts
  - Category-based observation counts
- **Dark-themed UI**: User-friendly interface with a modern dark color scheme
- **Environment Configuration**: Customizable default settings through .env file
- **Responsive Design**: Adapts to various screen sizes

## Data Sources

The application uses two primary datasets:
- observations.csv: Contains observation counts of species across parks
- species_info.csv: Contains detailed information about species, including conservation status

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bio_dash.git
cd bio_dash
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. (Optional) Create a .env file with default settings:
```
DEFAULT_PARK=Yellowstone
DEFAULT_CATEGORIES=Mammal,Bird,Reptile
```

## Usage

Run the application:

```bash
python app.py
```

Navigate to http://127.0.0.1:8050/ in your web browser to use the application.

## Deployment

The application includes a Procfile for deployment to platforms like Heroku or Render.

For Heroku deployment:
```bash
heroku create
git push heroku master
```

## Troubleshooting

If you encounter import errors with Dash components, make sure you have the correct versions:

For modern Dash versions (>=2.0):
```python
from dash import Dash, dcc, html, Input, Output
```

For older Dash versions (<2.0):
```python
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
```

## License

MIT License