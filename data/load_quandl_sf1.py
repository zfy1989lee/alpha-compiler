
# Code to load raw data from Quandl/SF1
# https://www.quandl.com/data/SF1-Core-US-Fundamentals-Data/
# requires the python Quandl package, and the 
# Quandl API key to be set as an ENV variable QUANDL_API_KEY.

import quandl
from os import environ
import sys

DS_NAME = "SF1"   # quandl DataSet code
RAW_FLDR = "raw"  # folder to store the raw text file
VAL_COL_NAME = "Value"

# TODO: move this function to utils/
def set_api_key():
    """read QUANDL_API_KEY env variable, and set it."""
    try:
        api_key = environ["QUANDL_API_KEY"]
    except KeyError:
        print("could not read the env variable: QUANDL_API_KEY")
        sys.exit()
    quandl.ApiConfig.api_key = api_key


def populate_raw_data(tickers, fields, at_time_of):
    set_api_key()

    global suffix
    if at_time_of:
        suffix = "ARQ"  # suffix for numbers at-time-of (as recorded)
    else:
        suffix = "MRQ"  # suffix for restated numbers

    # for every ticker in ticker_list get
    fields_a = map(lambda s: "%s_%s" % (s, suffix), fields)
    all_fields = None
    for ticker in tickers:
        for field in fields_a:

            query_str = "%s/%s_%s" % (DS_NAME, ticker, field)
            print("fetching data for: {}".format(query_str))
            df = quandl.get(query_str)

            #  Change column name to field
            df = df.rename(columns={VAL_COL_NAME: field})

            if all_fields is None:
                all_fields = df
            else:
                all_fields = all_fields.join(df)  # join data of all fields

        # write to file: raw/
        all_fields.to_csv("{}/{}.csv".format(RAW_FLDR, ticker))


if __name__ == '__main__':

    tickers = ["WMT"]
    fields = ["GP", "CAPEX", "EBIT", "ASSETS"]
    at_time_of = False  # if this is true append "", else append "_MRQ"

    populate_raw_data(tickers, fields, at_time_of)

    print("this worked boss")
