import pandas as pd
import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import random
from typing import Dict


class Ticker:
    def __init__(self, ticker_name: str):
        self._ticker_name = ticker_name
        self._ticker = yf.Ticker(ticker_name)

    def info_last_hour(self, end_time: datetime.datetime) -> pd.DataFrame:
        """Reads info about ticker for some hour time with 5 min 
        interval

        Args:
            end_time (datetime.datetime): hour info

        Returns:
            pd.DataFrame
        """
        start_time = end_time - datetime.timedelta(hours=1)
        hour_history = self._ticker.history(start=start_time,
                                            end=end_time, interval='5m')
        hour_history.index = hour_history.index.tz_convert('Europe/Moscow')
        return hour_history

    def calc_average(self, ticker_info: pd.DataFrame,
                     index: list = [0]) -> pd.DataFrame:
        """calculates average price for given Ticker info

        Args:
            ticker_info (pd.DataFrame): ticker price info
            index (list, optional): index for result row. Defaults to [0].

        Returns:
            pd.DataFrame: average Low and High price
        """
        high_mean = ticker_info['High'].mean()
        low_mean = ticker_info['Low'].mean()
        return pd.DataFrame({
            "Low_mean": low_mean,
            "High_mean": high_mean}, index=index,
            )

    @staticmethod
    def create_date_plot(data: Dict[str, pd.DataFrame]):
        """create plot for SMA of mean price

        Args:
            data (Dict[str, pd.DataFrame]): result df from calc_sma method
        """
        colors = ['tab:blue',
                  'tab:orange',
                  'tab:green',
                  'tab:red',
                  'tab:purple',
                  'tab:brown',
                  'tab:pink',
                  'tab:gray',
                  'tab:olive',
                  'tab:cyan']
        plt.rc('font', size=12)
        _, ax = plt.subplots(figsize=(10, 6))
        for label, df in data.items():
            for column in ["Low_mean_sma", "High_mean_sma"]:
                color = random.choice(colors)
                colors.remove(color)
                ax.plot(df['time'], df[column], color=color,
                        label=label+' '+column.split('_')[0])

        plt.xticks(rotation=90)
        ax.set_xlabel('Time')
        ax.set_ylabel('USD cost')
        ax.set_title('TS Plot')
        ax.grid(True)
        ax.legend(loc='upper left')
        return ax

    def calc_sma(self, start_time: datetime.datetime,
                 end_time: datetime.datetime,
                 window_size: int = 5) -> pd.DataFrame:
        """calc SMA of hour average for ticker

        Args:
            start_time (datetime.datetime)
            end_time (datetime.datetime)
            window_size (int, optional): SMA kernel size. Defaults to 5.

        Returns:
            pd.DataFrame: df with columns:
            ['time', "Low_mean_sma", "High_mean_sma"]
        """

        all_df = pd.DataFrame()
        while start_time < end_time:
            start_time += datetime.timedelta(hours=1)
            hour_df = self.info_last_hour(start_time)
            mean = self.calc_average(hour_df, [start_time])
            all_df = all_df.append(mean)
        ret = all_df.rolling(window=window_size) \
            .mean() \
            .iloc[window_size-1:] \
            .reset_index() \
            .rename(columns={"index": 'time',
                             "Low_mean": "Low_mean_sma",
                             "High_mean": "High_mean_sma"})
        return ret
