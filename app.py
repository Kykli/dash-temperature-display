import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
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
        min_date_allowed=dt.datetime(2018, 5, 22),
        max_date_allowed=dt.datetime.now(),
        end_date_placeholder_text="Select a date"
    ),

    dcc.Graph(
        id="in-temp-graph")
#        figure={
#            "data": [
#                {"x": df.date, "y": df.temperature, "type": "line", "name": iTemperature}, 
#            ],
#            "layout": {
#                "title": iTemperature,
#                "plot_bgcolor": colors["graphBackground"],
#                "paper_bgcolor": colors["graphBackground"]
#            }
#        }
#    )

])

@app.callback(
    Output("in-temp-graph", "figure"),
    [Input("date-picker-range", "start_date")]
)
def update_graph(select_date_value):
    #dff = df2[df2["date"] == select_date_value]
    return {
        "data": [
            {"x": df2.date, "y": df2.temperature}
        ]
    }


if __name__ == "__main__":
    app.run_server(debug=True)