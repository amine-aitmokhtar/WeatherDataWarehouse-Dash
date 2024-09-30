import pandas as pd
import glob


def merge_files(file_path_pattern):
    files = glob.glob(file_path_pattern)
    print(f"** Merging files from {file_path_pattern} **")
    merged_df = pd.concat(map(lambda file: pd.read_csv(file, low_memory=False), files), ignore_index=True)
    print(merged_df.head())
    print(merged_df.isnull().sum())
    return merged_df


def clean_data(df):
    keep_columns = ['STATION', 'NAME', 'LATITUDE', 'LONGITUDE', 'ELEVATION', 'DATE', 'PRCP', 'TAVG',
                    'TMAX', 'TMIN', 'SNWD', 'PGTM', 'SNOW', 'WDFG', 'WSFG']
    df = df[keep_columns]

    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y-%m-%d')
    df['YEAR'] = df['DATE'].dt.year
    df['MONTH'] = df['DATE'].dt.month
    df['DAY'] = df['DATE'].dt.day
    df['PAYS'] = df['STATION'].str[:2]

    for col in ['TMIN', 'TMAX', 'TAVG', 'PGTM', 'WDFG', 'WSFG']:
        df[col] = df[col].replace([-99, 93.2], pd.NA)

    df.fillna({'PRCP': 0, 'SNWD': 0, 'SNOW': 0}, inplace=True)

    # Select only numeric columns for median calculation
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    return df


def main():
    algeria_pattern = "./Dataset/Weather Data/Algeria/Weather_*.csv"
    morocco_pattern = "./Dataset/Weather Data/Morocco/Weather_*.csv"
    tunisia_pattern = "./Dataset/Weather Data/Tunisia/Weather_*.csv"

    df_algeria = merge_files(algeria_pattern)
    df_morocco = merge_files(morocco_pattern)
    df_tunisia = merge_files(tunisia_pattern)

    df = pd.concat([df_algeria, df_morocco, df_tunisia], ignore_index=True)
    print("*** Merging multiple country datasets into a single dataframe ***")
    print(df.head())

    cleaned_df = clean_data(df)
    cleaned_df.to_csv("./Dataset/Weather_data.csv", index=False)
    print("Data cleaned and saved to ./Dataset/Weather_data.csv")


if __name__ == "__main__":
    main()
