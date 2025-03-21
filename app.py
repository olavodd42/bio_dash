import dash
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
DEFAULT_PARK = os.getenv("DEFAULT_PARK")
DEFAULT_CATEGORIES = os.getenv("DEFAULT_CATEGORIES", "").split(",")

# Load and clean datasets
obs_df = pd.read_csv("observations.csv")
species_df = pd.read_csv("species_info.csv")
obs_df = obs_df.dropna(subset=["scientific_name", "park_name"]).drop_duplicates()
species_df = species_df.dropna(subset=["scientific_name", "category"]).drop_duplicates()
species_df["conservation_status"] = species_df["conservation_status"].fillna("Non-threatened")

# Merge datasets
merged_df = pd.merge(obs_df, species_df, on="scientific_name", how="inner")

# Init app
app = Dash(__name__)
server = app.server

# Set defaults from .env or fallback
default_park_value = [DEFAULT_PARK] if DEFAULT_PARK in merged_df["park_name"].unique() else [merged_df["park_name"].unique()[0]]
default_category_value = [cat for cat in DEFAULT_CATEGORIES if cat in merged_df["category"].unique()] or list(merged_df["category"].unique())

# Layout with dark theme styling
app.layout = html.Div([
    html.H1("National Park Species Observations", style={"textAlign": "center", "color": "#FFFFFF"}),

    html.Div([
        html.Label("Select Parks:", style={"color": "#FFFFFF"}),
        dcc.Dropdown(
            id="park-dropdown",
            options=[{"label": park, "value": park} for park in sorted(merged_df["park_name"].unique())],
            value=default_park_value,
            multi=True,
            style={"backgroundColor": "#333", "color": "#FFF"}
        ),

        html.Label("Filter by Category:", style={"color": "#FFFFFF", "marginTop": "20px"}),
        dcc.Checklist(
            id="category-filter",
            options=[{"label": cat, "value": cat} for cat in sorted(merged_df["category"].unique())],
            value=default_category_value,
            labelStyle={"display": "inline-block", "marginRight": "10px", "color": "#FFFFFF"}
        )
    ], style={"padding": 20, "backgroundColor": "#222", "borderRadius": "8px"}),

    html.Div([
        dcc.Graph(id="observations-graph")
    ], style={"marginTop": "20px"})

], style={"backgroundColor": "#111", "minHeight": "100vh", "padding": "30px", "fontFamily": "Arial"})

# Callback
@app.callback(
    Output("observations-graph", "figure"),
    [Input("park-dropdown", "value"),
     Input("category-filter", "value")]
)
def update_figure(parks, categories):
    if not parks or not categories:
        return go.Figure(layout={
            "paper_bgcolor": "#111",
            "plot_bgcolor": "#111",
            "font": {"color": "#FFF"},
            "annotations": [{
                "text": "Please select park(s) and category(ies)",
                "xref": "paper", "yref": "paper",
                "showarrow": False,
                "font": {"size": 18},
                "x": 0.5, "y": 0.5, "xanchor": "center", "yanchor": "middle"
            }]
        })

    df = merged_df[merged_df["park_name"].isin(parks) & merged_df["category"].isin(categories)]

    if df.empty:
        return go.Figure(layout={
            "paper_bgcolor": "#111",
            "plot_bgcolor": "#111",
            "font": {"color": "#FFF"},
            "annotations": [{
                "text": "No data available for selected filters",
                "xref": "paper", "yref": "paper",
                "showarrow": False,
                "font": {"size": 18},
                "x": 0.5, "y": 0.5, "xanchor": "center", "yanchor": "middle"
            }]
        })

    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{"type": "xy"}, {"type": "domain"}, {"type": "xy"}]],
        subplot_titles=["Observations per Species", "Conservation Status", "Observations per Category"]
    )

    sp = px.bar(df, x="scientific_name", y="observations", color="conservation_status")
    for trace in sp.data:
        fig.add_trace(trace, row=1, col=1)
    fig.update_traces(marker_line_width=0)

    pie_data = df.groupby("conservation_status")["observations"].sum().reset_index()
    pie = px.pie(pie_data, names="conservation_status", values="observations")
    for trace in pie.data:
        fig.add_trace(trace, row=1, col=2)

    cat = df.groupby("category")["observations"].sum().reset_index()
    cat_chart = px.bar(cat, x="category", y="observations", color="category")
    for trace in cat_chart.data:
        fig.add_trace(trace, row=1, col=3)

    fig.update_layout(
        title="Species Observations across Selected Parks",
        height=600,
        paper_bgcolor="#111",
        plot_bgcolor="#111",
        font=dict(color="#FFF")
    )
    return fig

if __name__ == "__main__":
    app.run(debug=True)
