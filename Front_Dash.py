import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import pymysql


def fetch_data():
    db = pymysql.connect(host='localhost', user='root', password='test123', database='weather_dataWarehouse',
                         charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute("""
        SELECT * 
        FROM Weather_Fact 
        INNER JOIN Station_Dim ON Weather_Fact.StationID = Station_Dim.StationID 
        INNER JOIN Date_Dim ON Weather_Fact.Date_ID = Date_Dim.Date_ID
    """)
    rows = cursor.fetchall()
    cursor.close()
    db.close()
    return pd.DataFrame(rows)


df = fetch_data()

measure_descriptions = {
    'PRCP': 'Precipitations (mm)',
    'TAVG': 'Average Temperature (°C)',
    'TMAX': 'Maximum Temperature (°C)',
    'TMIN': 'Minimum Temperature (°C)',
    'SNWD': 'Snow Depth (mm)',
    'PGTM': 'Atmospheric Pressure (hPa)',
    'SNOW': 'Snowfall (mm)',
    'WDFG': 'Wind Direction (°)',
    'WSFG': 'Maximum Wind Speed (km/h)'
}

external_stylesheets = [
    'C:/Users/mredh/PycharmProjects/DataWarehouse2/custom.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    children=[
        html.Div(
            className='header',
            children=[
                html.H1('Weather Data Dashboard')
            ]
        ),
        html.Div(
            className='container',
            children=[
                dcc.Dropdown(
                    id='station-dropdown',
                    options=[{'label': i, 'value': i} for i in df['Name'].unique()],
                    value=df['Name'].iloc[0],
                    className='dropdown'
                ),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': i, 'value': i} for i in df['Year'].unique()],
                    value=df['Year'].min(),
                    className='dropdown'
                ),
                dcc.Dropdown(
                    id='season-dropdown',
                    options=[{'label': i, 'value': i} for i in ['Spring', 'Summer', 'Autumn', 'Winter']],
                    value='Winter',
                    className='dropdown'
                ),
                dcc.Dropdown(
                    id='quarter-dropdown',
                    options=[{'label': 'Q' + str(i), 'value': i} for i in range(1, 5)],
                    value=1,
                    className='dropdown'
                ),
                dcc.Dropdown(
                    id='month-dropdown',
                    options=[{'label': i, 'value': i} for i in df['Month'].unique()],
                    value=df['Month'].min(),
                    className='dropdown'
                ),
                dcc.Dropdown(
                    id='measure-dropdown',
                    options=[{'label': v, 'value': k} for k, v in measure_descriptions.items()],
                    value='TMAX',
                    className='dropdown'
                )
            ]
        ),
        html.Div(
            className='graph-container',
            children=[
                html.Div('Weather Measure Over Time', className='graph-title'),
                dcc.Graph(id='weather-graph')
            ]
        ),
        html.Div(
            className='graph-container',
            children=[
                html.Div('Distribution of Weather Measure', className='graph-title'),
                dcc.Graph(id='weather-histogram')
            ]
        )
    ]
)


@app.callback(
    Output('weather-graph', 'figure'),
    [Input('station-dropdown', 'value'),
     Input('year-dropdown', 'value'),
     Input('season-dropdown', 'value'),
     Input('quarter-dropdown', 'value'),
     Input('month-dropdown', 'value'),
     Input('measure-dropdown', 'value')]
)
def update_weather_graph(selected_station, selected_year, selected_season, selected_quarter, selected_month,
                         selected_measure):
    season_months = {
        'Spring': [3, 4, 5],
        'Summer': [6, 7, 8],
        'Autumn': [9, 10, 11],
        'Winter': [12, 1, 2]
    }

    quarter_months = {
        1: [1, 2, 3],
        2: [4, 5, 6],
        3: [7, 8, 9],
        4: [10, 11, 12]
    }

    filtered_df = df[
        (df['Name'] == selected_station) &
        (df['Year'] == selected_year) &
        (df['Month'].isin(season_months[selected_season])) &
        (df['Month'].isin(quarter_months[selected_quarter])) &
        (df['Month'] == selected_month)
        ]
    fig = px.line(filtered_df, x='Day', y=selected_measure, title=f'{measure_descriptions[selected_measure]} Over Days',
                  template='plotly_dark')
    fig.update_traces(line=dict(color='#ff6347'))
    fig.update_layout(paper_bgcolor='white', plot_bgcolor='white')
    return fig


@app.callback(
    Output('weather-histogram', 'figure'),
    [Input('station-dropdown', 'value'),
     Input('year-dropdown', 'value'),
     Input('season-dropdown', 'value'),
     Input('quarter-dropdown', 'value'),
     Input('month-dropdown', 'value'),
     Input('measure-dropdown', 'value')]
)
def update_weather_histogram(selected_station, selected_year, selected_season, selected_quarter, selected_month,
                             selected_measure):
    season_months = {
        'Spring': [3, 4, 5],
        'Summer': [6, 7, 8],
        'Autumn': [9, 10, 11],
        'Winter': [12, 1, 2]
    }

    quarter_months = {
        1: [1, 2, 3],
        2: [4, 5, 6],
        3: [7, 8, 9],
        4: [10, 11, 12]
    }

    filtered_df = df[
        (df['Name'] == selected_station) &
        (df['Year'] == selected_year) &
        (df['Month'].isin(season_months[selected_season])) &
        (df['Month'].isin(quarter_months[selected_quarter])) &
        (df['Month'] == selected_month)
        ]
    fig = px.histogram(filtered_df, x=selected_measure,
                       title=f'Distribution of {measure_descriptions[selected_measure]}', template='plotly_dark')
    fig.update_traces(marker_color='#ff6347')
    fig.update_layout(paper_bgcolor='white', plot_bgcolor='white')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
