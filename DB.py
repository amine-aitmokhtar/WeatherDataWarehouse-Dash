import pymysql
import pandas as pd
import numpy as np


def create_database(connection, db_name):
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    print(f"Database {db_name} created")
    cursor.close()


def create_tables(cursor):
    table_creation_queries = {
        "Station_Dim": """
            CREATE TABLE IF NOT EXISTS Station_Dim (
                StationID INT AUTO_INCREMENT,
                StationCode VARCHAR(255),
                Name VARCHAR(255),
                Latitude FLOAT,
                Longitude FLOAT,
                Elevation FLOAT,
                Pays CHAR(2),
                PRIMARY KEY (StationID)
            )
        """,
        "Date_Dim": """
            CREATE TABLE IF NOT EXISTS Date_Dim (
                Date_ID INT AUTO_INCREMENT,
                Date DATE,
                Year INT,
                Month INT,
                Day INT,
                PRIMARY KEY (Date_ID)
            )
        """,
        "Weather_Fact": """
            CREATE TABLE IF NOT EXISTS Weather_Fact (
                StationID INT,
                Date_ID INT,
                PRCP FLOAT,
                TAVG FLOAT,
                TMAX FLOAT,
                TMIN FLOAT,
                SNWD FLOAT,
                PGTM FLOAT,
                SNOW FLOAT,
                WDFG FLOAT,
                WSFG FLOAT,
                PRIMARY KEY (StationID, Date_ID),
                FOREIGN KEY (StationID) REFERENCES Station_Dim(StationID),
                FOREIGN KEY (Date_ID) REFERENCES Date_Dim(Date_ID)
            )
        """
    }

    for table, query in table_creation_queries.items():
        cursor.execute(query)
        print(f"Table {table} created")


def populate_tables(cursor, data):
    # Insert data into Station_Dim and Date_Dim
    stations = data[["STATION", "NAME", "LATITUDE", "LONGITUDE", "ELEVATION", "PAYS"]].drop_duplicates()
    dates = data[["DATE", "YEAR", "MONTH", "DAY"]].drop_duplicates()

    station_id_map = {}
    for _, row in stations.iterrows():
        cursor.execute("""
            INSERT INTO Station_Dim (StationCode, Name, Latitude, Longitude, Elevation, Pays) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, tuple(row))
        station_id_map[row["STATION"]] = cursor.lastrowid

    date_id_map = {}
    for _, row in dates.iterrows():
        cursor.execute("""
            INSERT INTO Date_Dim (Date, Year, Month, Day) 
            VALUES (%s, %s, %s, %s)
        """, tuple(row))
        date_id_map[row["DATE"]] = cursor.lastrowid

    data = data.replace({np.nan: None})  # Replace NaN with None

    for _, row in data.iterrows():
        cursor.execute("""
            INSERT INTO Weather_Fact (StationID, Date_ID, PRCP, TAVG, TMAX, TMIN, SNWD, PGTM, SNOW, WDFG, WSFG) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
        station_id_map[row["STATION"]], date_id_map[row["DATE"]], row["PRCP"], row["TAVG"], row["TMAX"], row["TMIN"],
        row["SNWD"], row["PGTM"], row["SNOW"], row["WDFG"], row["WSFG"]))

    print("Tables populated")


def populate_date_dim(cursor):
    date_dim = pd.read_csv('./Dataset/Dim_Date_1850-2050.csv')
    date_dim = date_dim.replace({np.nan: None})  # Replace NaN with None
    for _, row in date_dim.iterrows():
        cursor.execute("""
            INSERT INTO Date_Dim (Date, Year, Month, Day) 
            VALUES (%s, %s, %s, %s)
        """, (row["Date"], row["Year"], row["Month"], row["Day"]))
    print("Date_Dim populated from Dim_Date_1850-2050.csv")


def main():
    initial_connection = pymysql.connect(host='localhost', user='root', password='test123', charset='utf8mb4',
                                         cursorclass=pymysql.cursors.DictCursor)
    create_database(initial_connection, 'weather_dataWarehouse')
    initial_connection.close()

    db = pymysql.connect(host='localhost', user='root', password='test123', database='weather_dataWarehouse',
                         charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()

    create_tables(cursor)
    print("Data Warehouse schema created")

    data = pd.read_csv('./Dataset/Weather_data.csv')
    populate_tables(cursor, data)

    # Populate DateDim separately
    populate_date_dim(cursor)

    cursor.close()
    db.commit()
    db.close()


if __name__ == "__main__":
    main()




