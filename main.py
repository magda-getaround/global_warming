import numpy as np
import pandas as pd
import scipy
import statistics
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# 2320799 - LA
# 2320795 - SAN FRANCISCO INTERNATIONAL AIRPORT
# 2320905 - HEATHROW airport LONDON
# 2320909 - NYC
FILE = "2320795.csv"
CITY = "NONE"
if "2320795" in FILE:
    CITY = "San Francisco"
elif "2320905" in FILE:
    CITY = "London"
elif "2320799" in FILE:
    CITY = "Los Angeles"
elif "2320909" in FILE:
    CITY = "New York City"

sns.set()
warnings.simplefilter(action="ignore", category=FutureWarning)


def show_year_avg_graph(df):
    ya = df.groupby(df["YEAR"])["TAVG"].mean().to_frame(name="avg_temp").reset_index()

    rolling_avg = ya.avg_temp.rolling(window=2).mean()
    exponential_moving_avg = ya.avg_temp.ewm(span=59).mean()

    rolling_avg.plot(
        style="r--", label="Year average temp"
    )
    exponential_moving_avg.plot(
        style="b", label="Exponential moving average"
    )

    plt.legend()
    plt.title("Average temperature in {city} from 1960 to 2019".format(city=CITY))
    plt.xlabel("Year")
    plt.ylabel("Temp in Celsius")
    plt.xticks(np.arange(59), range(1960, 2019), rotation=90)
    plt.show()


def show_rainfall_graph(df):
    ya = df.groupby(df["YEAR"])["PRCP"].sum().to_frame(name="rain_sum").reset_index()
    ya.set_index("YEAR")

    ya.rain_sum.ewm(span=59).mean().plot.line(style="b", label="Rainfall")

    plt.legend()
    plt.title("Rainy days in {city} from 1960 to 2019".format(city=CITY))
    plt.xlabel("Year")
    plt.ylabel("Milimiters of rain")
    plt.xticks(np.arange(59), range(1960, 2019), rotation=90)
    plt.show()


df = pd.read_csv(
    FILE, parse_dates=["DATE"], sep=",", decimal=".", infer_datetime_format=True
)
print(df)

df["TAVG"] = df.apply(
    lambda row: float(statistics.mean([row["TMIN"], row["TMAX"]])), axis=1
)
print(df)

df["RAINED"] = df.apply(
    lambda row: 1 if row["PRCP"] > 0 else 0, axis=1
)

df["YEAR"] = pd.DatetimeIndex(df["DATE"]).year

# -------------------------------------------------------------------------------------------------------------------- #

# show_year_avg_graph(df)
show_rainfall_graph(df)
