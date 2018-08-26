import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import datetime as dt
import pandas_datareader.data as web
import pandas as pd

app = dash.Dash()

oTemperature = "Outdoor Temperature"
iTemperature = "Indoor Temperature"
df = pd.read_csv("oTemps.csv")
df2 = pd.read_csv("iTemps.csv")

colors = {
    "graphBackground": "#212529",
    "background": "#000000",
    "text": "#ffffff"
}

app.layout = html.Div(style={"backgroundColor": colors["background"]}, children=[
    html.H1(
        children="Home Temperature",
        style={
            "textAlign": "center",
            "color": colors["text"]
        }
    ),

    html.Div(children="Outdoor and indoor temperatures", style={
        "textAlign": "center",
        "color": colors["text"]
    }),

    html.Div(children="", style={
        "color": colors["background"]
    }),

    dcc.Graph(
        id="out-temp-graph",
        figure={
            "data": [
                {"x": df.date, "y": df.temperature, "type": "line", "name": oTemperature}, 
            ],
            "layout": {
                "title": oTemperature,
                "plot_bgcolor": colors["graphBackground"],
                "paper_bgcolor": colors["graphBackground"]
            }
        }
    ),

    dcc.DatePickerRange(
        id="date-picker-range",
        start_date=dt.datetime(2018, 5, 22),
        end_date=dt.datetime.now(),
        min_date_allowed=dt.datetime(2018, 5, 22),
        max_date_allowed=dt.datetime.now(),
        end_date_placeholder_text="Select a date"
    ),

    dcc.Graph(id="in-temp-graph")

])

@app.callback(
    Output("in-temp-graph", "figure"),
    [Input("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date")]
)
def update_graph(start_date, end_date):
    
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
 
    filtered_df = df2[df2.date.between(
        dt.datetime.strftime(start_date, "%Y-%m-%d"),
        dt.datetime.strftime(end_date, "%Y-%m-%d")
    )]

    trace1 = go.Scatter(
        x = filtered_df.date,
        y = filtered_df.temperature,
        mode = "lines",
        name = iTemperature
    )

    return {
        "data": [trace1],
        "layout": go.Layout(
            title = iTemperature,
            plot_bgcolor = colors["graphBackground"],
            paper_bgcolor = colors["graphBackground"]
        )
    }


if __name__ == "__main__":
    app.run_server(debug=True)