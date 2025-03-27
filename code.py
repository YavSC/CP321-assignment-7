import dash
from dash import html, dcc, Output, Input
import plotly.express as px
import pandas as pd

#1 FIFA World cup winners and runnerups dataset
data = pd.DataFrame({
    "winners": ["Uruguay", "Italy", "Italy", "Uruguay", "Germany", "Brazil", "Brazil", "England", "Brazil", "Germany", "Argentina", "Italy", "Argentina", "Germany", "Brazil", "France", "Brazil", "Italy", "Spain", "Germany", "France", "Argentina"],
    "runnerups": ["Argentina", "Czech Replublic", "Hungary", "Brazil", "Hungary", "Sweden", "Czech Replublic", "Germany", "Italy", "Netherlands", "Netherlands", "Germany", "Germany", "Argentina", "Italy", "Brazil", "Germany", "France", "Netherlands", "Argentina", "Croatia", "France"],
    "year": [1930, 1934, 1938, 1950, 1954, 1958, 1962, 1966, 1970, 1974, 1978, 1982, 1986, 1990, 1994, 1998, 2002, 2006, 2010, 2014, 2018, 2022],
})
dataUnique = pd.DataFrame({
    "uniqueWinners": ["Brazil", "Germany", "Italy", "Argentina", "France", "Uruguay", "England", "Spain"],
    "totalWins": [5, 4, 4, 3, 2, 2, 1, 1]
})

app = dash.Dash()

#this line is for the code to work on the server
server = app.server

app.layout = html.Div([
    html.H1("FIFA World Cup Statistics Dashboard"),
    dcc.RadioItems(options=["All Winners", "By Year:"], value="All Winners", id="options"),
    dcc.Dropdown(
        id="year",
        value=1930,
        options = data.year,
        clearable = False,
        style={"width": '200px'}
    ),
    dcc.Graph(id="graph")
], style = {'background-color': 'white'})

@app.callback(
    Output(component_id="graph", component_property="figure"),
    Input(component_id="options", component_property="value"),
    Input(component_id="year", component_property="value")
)

def updateGraph(option, year):
    if option == "All Winners":
        fig = px.choropleth(
            dataUnique,
            locations="uniqueWinners",
            locationmode="country names",
            color="totalWins",
            color_continuous_scale="Viridis",
            scope="world",
            title="All FIFA World Cup Winners"
        )
    else:
        x = 0
        for i in data.year:
            if i == year:
                break
            else:
                x += 1

        fig = px.choropleth(
            locations=[data.winners.iloc[x], data.runnerups.iloc[x]],
            locationmode="country names",
            color=["Winner", "Runnerup"],
            scope="world",
            title=f"Winner and Runnerup for FIFA World Cup {year}"
        )
    return fig

app.run()
