import pandas as pd
import matplotlib.pyplot as plt
from numpy import nanmean
from numpy import nanmedian

df = pd.read_excel('C:/Users/ac18a/Downloads/S&P 500 data.xlsx')
df = df[["Date", "Price", "LT IntRate", "Earnings"]]

# add PE ratio

PE_list = []
for i in range(len(df.index)):
    PE = df["Price"][i] / df["Earnings"][i]
    PE_list.append(PE)
df['PE'] = PE_list


# function to add "n" years average earnings and "n" years average PE

def Earnings_and_PE_in_period(dataframe, months_period):
    Average_earnings_list = []
    Trailing_PE_list = []
    for i in range(months_period - 1):
        Average_earnings_list.append(None)
        Trailing_PE_list.append(None)
    for i in range(len(df.index) - months_period + 1):
        Average_earnings = sum(dataframe["Earnings"][i:i + months_period]) / months_period
        Trailing_PE = dataframe["Price"][i + months_period - 1] / Average_earnings
        Average_earnings_list.append(Average_earnings)
        Trailing_PE_list.append(Trailing_PE)
    title_earnings = "Avg._" + str(months_period) + "_months_earnings"
    title_PE = "Trail._" + str(months_period) + "_months_PE"
    dataframe[title_earnings] = Average_earnings_list
    dataframe[title_PE] = Trailing_PE_list


# Examples
Earnings_and_PE_in_period(df, 12)
Earnings_and_PE_in_period(df, 24)
Earnings_and_PE_in_period(df, 60)
Earnings_and_PE_in_period(df, 120)


def annual_percentage_return_after_certain_period(dataframe, period_in_years):
    annual_return_in_n_years_list = []
    for i in range(len(df.index) - (period_in_years * 12) - 1):
        return_in_n_years = ((df["Price"][i + (period_in_years * 12)] - df["Price"][i]) / df["Price"][i])
        # If you remove the next function you just have the total return, which you should multiply by 100
        annual_return_in_n_years = ((1 + return_in_n_years) ** (1 / period_in_years) - 1) * 100
        annual_return_in_n_years_list.append(annual_return_in_n_years)
    for i in range(period_in_years * 12 + 1):
        annual_return_in_n_years_list.append(None)
    title_return = "Ann_return_after_" + str(period_in_years) + "_years"
    dataframe[title_return] = annual_return_in_n_years_list


# Examples
annual_percentage_return_after_certain_period(df, 1)
annual_percentage_return_after_certain_period(df, 2)
annual_percentage_return_after_certain_period(df, 5)
annual_percentage_return_after_certain_period(df, 7)
annual_percentage_return_after_certain_period(df, 10)
annual_percentage_return_after_certain_period(df, 15)
annual_percentage_return_after_certain_period(df, 17)
annual_percentage_return_after_certain_period(df, 20)
annual_percentage_return_after_certain_period(df, 25)
annual_percentage_return_after_certain_period(df, 30)
annual_percentage_return_after_certain_period(df, 50)

inversePE_list = []

for i in range(len(df.index)):
    inversePE = 100 / df.at[i, "Trail._120_months_PE"]
    inversePE_list.append(inversePE)

df["Inverse_trail._120_months_PE"] = inversePE_list

# To see the whole dataframe
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
# print(df)

# Perhaps I should also add "Date"
df_test_correlation = df[["Date", "Ann_return_after_1_years", "Ann_return_after_2_years", "Ann_return_after_5_years",
                          "Ann_return_after_7_years",
                          "Ann_return_after_10_years", "Ann_return_after_15_years", "Ann_return_after_17_years",
                          "Ann_return_after_20_years", "Ann_return_after_25_years", "Ann_return_after_30_years",
                          "Ann_return_after_50_years",
                          "PE", "Trail._12_months_PE", "Trail._24_months_PE", "Trail._60_months_PE",
                          "Trail._120_months_PE", "Inverse_trail._120_months_PE"]]

# Full correlation table. To make it more readable, some rows/columns should probably be removed.
corr_table = df_test_correlation.corr()
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(corr_table)


# If you want to see the graph of one single correlation
def corr_graph(dataframe, returns, PE, Date, correlation_table=None, point_size=1):
    plot1 = dataframe.plot.scatter(x=returns,
                                   y=PE,
                                   c=Date,
                                   s=point_size,
                                   colormap='gist_rainbow')
    if correlation_table is None:
        correlation_table = dataframe.corr()
    try:
        plt.title(label="Correlation = " + str(format(correlation_table.at[returns, PE] * 100, ".2f") + "%"),
                  color="black")
    except:
        raise TypeError("\n correlation_table should be a dataframe. It should contain correlation values"
                        "with the same row name and column name as the return and PE you entered")
    # corr_table.iloc[2,3]  if you use integers
    plt.figtext(0.01, 0.945, " Avg = " + str(format(nanmean(dataframe[returns]), ".2f"))
                + "%  Med = " + str(format(nanmedian(dataframe[returns]), ".2f"))
                + "%\n Avg PE = " + str(format(nanmean(dataframe[PE]), ".2f"))
                + "  Med PE = " + str(format(nanmedian(dataframe[PE]), ".2f")),
                fontsize=8)
    plt.show()


corr_graph(df_test_correlation, "Ann_return_after_1_years", "PE", 'Date', corr_table, point_size=0.5)
corr_graph(df_test_correlation, "Ann_return_after_17_years", "PE", 'Date', corr_table, point_size=0.5)
corr_graph(df_test_correlation, "Ann_return_after_17_years", "Trail._60_months_PE", 'Date', corr_table, point_size=0.5)
corr_graph(df_test_correlation, "Ann_return_after_17_years", "Inverse_trail._120_months_PE", 'Date', corr_table,
           point_size=0.5)
corr_graph(df_test_correlation, "Ann_return_after_17_years", "Trail._120_months_PE", 'Date', corr_table, point_size=0.5)
corr_graph(df_test_correlation, "Ann_return_after_30_years", "Trail._60_months_PE", 'Date', corr_table, point_size=0.5)
corr_graph(df_test_correlation, "Ann_return_after_50_years", "Trail._60_months_PE", 'Date', corr_table, point_size=0.5)

# corr_table.append(df_test_correlation[["Date"]]
# corr_graph(df_test_correlation, "Ann_return_after_1_years", "PE", 'Date', corr_table, point_size=0.5)


# I discovered that the 5 years PE is a much better predictor of future returns than the annual or monthly PE!!
# 1 year returns
# corr_graph(df_test_correlation, "Ann_return_after_1_years", "PE", 'Date', corr_table, point_size=0.5)
# corr_graph(df_test_correlation, "Ann_return_after_1_years", "Trail._12_months_PE", 'Date', corr_table, point_size=0.5)
# corr_graph(df_test_correlation, "Ann_return_after_1_years", "Trail._60_months_PE", 'Date', corr_table, point_size=0.5)
# 2 year returns
# corr_graph(df_test_correlation, "Ann_return_after_2_years", "PE", 'Date', corr_table, point_size=0.5)
# corr_graph(df_test_correlation, "Ann_return_after_2_years", "Trail._12_months_PE", 'Date', corr_table, point_size=0.5)
# corr_graph(df_test_correlation, "Ann_return_after_2_years", "Trail._60_months_PE", 'Date', corr_table, point_size=0.5)
# 5 year returns
# corr_graph(df_test_correlation, "Ann_return_after_5_years", "PE", 'Date', corr_table, point_size=0.5)
# corr_graph(df_test_correlation, "Ann_return_after_5_years", "Trail._12_months_PE", 'Date', corr_table, point_size=0.5)
# corr_graph(df_test_correlation, "Ann_return_after_5_years", "Trail._60_months_PE", 'Date', corr_table, point_size=0.5)
# 10 year returns
# corr_graph(df_test_correlation, "Ann_return_after_10_years", "PE", 'Date', corr_table, point_size=0.5)
# corr_graph(df_test_correlation, "Ann_return_after_10_years", "Trail._12_months_PE", 'Date', corr_table, point_size=0.5)
# corr_graph(df_test_correlation, "Ann_return_after_10_years", "Trail._60_months_PE", 'Date', corr_table, point_size=0.5)
