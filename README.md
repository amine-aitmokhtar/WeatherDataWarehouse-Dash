# WeatherDataWarehouse-Dash

## Description

This repository hosts a project designed to convert raw climate data into a structured data warehouse.

## Project Details

Key components include:

- **Implementation**: Developed exclusively using Python and MySQL.
- **Star Schema**: The data is organized into a star schema stored in a database named "Weather_DataWarehouse".
- **ETL Process**: The tables in the data warehouse are populated via an ETL process, loading data from flat files into the "Weather_DataWarehouse".
- **Dashboard**: Built with Dash in Python, this dashboard facilitates data analysis.
- **Dynamic Visualization**: The dashboard features dynamic graphs and charts to visualize climate data trends.

## Dataset Description

The dataset, provided by the National Centers for Environmental Information, includes climate data from three Maghreb countries. Key attributes are:

- Precipitation (PRCP)
- Snow Depth (SNWD)
- Snowfall (SNOW)
- Average Temperature (TAVG)
- Maximum Temperature (TMAX)
- Minimum Temperature (TMIN)
- Direction of Maximum Wind Gust (WDFG)
- Peak Gust Time (PGTM)
- Maximum Wind Speed in Gust (WSFG)
- Weather Types (WT**)

This repository aims to offer an efficient and dynamic approach to climate data analysis through a well-structured data warehouse and an interactive dashboard.

## Resources

- **Dash Documentation**: [Dash Documentation](https://dash.plotly.com/)
- **Python Documentation**: [Python Documentation](https://docs.python.org/3/)
