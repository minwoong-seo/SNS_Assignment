import pandas as pd


def get_df(path, col_names_arr):
    df = pd.read_csv(path)
    filtered_df = df.loc[:, col_names_arr]
    filtered_df = filter_df_by_year(filtered_df, "Date", 2020)
    return filtered_df


# df: DataFrame

def filter_df_by_year(df, date_col_name, sel_year=2015):
    df[date_col_name] = pd.to_datetime(df[date_col_name], format='%Y-%m-%d %H:%M:%S%z', utc=True)
    refined_df = separate_full_date(df)
    boolean_df = refined_df["Year"] >= sel_year
    df = refined_df[boolean_df]

    # print(df)
    high_column = df.pop("High")
    df.loc[:, "High"] = high_column

    return df


def separate_full_date(df):
    copied_df = df.copy()
    year_column = copied_df.loc[:, "Date"].dt.year
    month_column = copied_df.loc[:, "Date"].dt.month
    day_column = copied_df.loc[:, "Date"].dt.day
    df = df.drop("Date", axis=1)
    df.insert(0, "Year", year_column)
    df.insert(1, "Month", month_column)
    df.insert(2, "Day", day_column)

    return df
