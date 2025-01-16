import matplotlib.pyplot as plt
import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

CONFIRMED_CASES_FILE = os.path.join(script_dir, 'time_series_covid19_confirmed_global.csv')
DEATHS_FILE = os.path.join(script_dir, 'time_series_covid19_deaths_global.csv')
RECOVERIES_FILE = os.path.join(script_dir, 'time_series_covid19_recovered_global.csv')

DATE_FORMAT = '%m/%d/%y'

def get_data_for_country(country):
    print('Getting the data for the subplots.')

    # Read in the data to a pandas DataFrame.
    cases_data = pd.read_csv(CONFIRMED_CASES_FILE)
    deaths_data = pd.read_csv(DEATHS_FILE)
    recoveries_data = pd.read_csv(RECOVERIES_FILE)

    try:
        cases_grouped_by_country = cases_data.groupby('Country/Region')
        cases_data_frame_by_country = cases_grouped_by_country.sum()
        cases_by_location = cases_data_frame_by_country.loc[country, cases_data_frame_by_country.columns[3:]]

        deaths_grouped_by_country = deaths_data.groupby('Country/Region')
        deaths_data_frame_by_country = deaths_grouped_by_country.sum()
        deaths_by_location = deaths_data_frame_by_country.loc[country, deaths_data_frame_by_country.columns[3:]]

        recoveries_grouped_by_country = recoveries_data.groupby('Country/Region')
        recoveries_data_frame_by_country = recoveries_grouped_by_country.sum()
        recoveries_by_location = recoveries_data_frame_by_country.loc[country, recoveries_data_frame_by_country.columns[3:]]
    except Exception:
        print(f"There is no available data for the country {country}")
        raise

    return cases_by_location, deaths_by_location, recoveries_by_location

def make_confirmed_cases_subplots(ax1, ax2, cases_by_location):
    print('Generating subplots for confirmed cases.')

    # Plot 1: Daily confirmed cases.
    cases_by_location.index = pd.to_datetime(cases_by_location.index, format=DATE_FORMAT, errors='coerce')
    new_daily_confirmed_cases = cases_by_location.diff().fillna(0).clip(lower=0)  # Set negative values to zero

    ax1.bar(cases_by_location.index, new_daily_confirmed_cases.values, label='Daily Confirmed Cases', color='purple')
    ax1.set_ylabel('Daily Confirmed Cases')
    ax1.legend()
    ax1.ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Plot 2: Total confirmed cases.
    ax2.plot(cases_by_location.index, cases_by_location.values, label='Total Confirmed Cases', color='blue')
    ax2.set_ylabel('Confirmed cases')
    ax2.legend()
    ax2.ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Set major locator for the x-axis to be every 6 months.
    ax1.xaxis.set_major_locator(plt.MultipleLocator(180))
    ax2.xaxis.set_major_locator(plt.MultipleLocator(180))

def make_deaths_subplots(ax1, ax2, deaths_by_location):
    print('Generating subplots for deaths cases.')

    # Plot 3: Daily deaths.
    deaths_by_location.index = pd.to_datetime(deaths_by_location.index, format=DATE_FORMAT, errors='coerce')
    new_daily_deaths = deaths_by_location.diff().fillna(0).clip(lower=0)  # Set negative values to zero

    ax1.bar(deaths_by_location.index, new_daily_deaths.values, label='Daily Deaths', color='purple')
    ax1.set_ylabel('Daily Deaths')
    ax1.legend()
    ax1.ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Plot 4: Total deaths.
    ax2.plot(deaths_by_location.index, deaths_by_location.values, label='Total Deaths', color='orange')
    ax2.set_ylabel('Total Deaths')
    ax2.legend()
    ax2.ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Set major locator for the x-axis to be every 6 months.
    ax1.xaxis.set_major_locator(plt.MultipleLocator(180))
    ax2.xaxis.set_major_locator(plt.MultipleLocator(180))

def make_recoveries_subplots(ax1, ax2, recoveries_by_location):
    print('Generating subplots for recoveries cases.')

    # Plot 5: Daily recoveries.
    recoveries_by_location.index = pd.to_datetime(recoveries_by_location.index, format=DATE_FORMAT, errors='coerce')
    new_daily_recoveries = recoveries_by_location.diff().fillna(0).clip(lower=0)  # Set negative values to zero

    ax1.bar(recoveries_by_location.index, new_daily_recoveries.values, label='Daily Recoveries', color='green')
    ax1.set_ylabel('Daily Recoveries')
    ax1.legend()
    ax1.ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Plot 6: Total recoveries.
    ax2.plot(recoveries_by_location.index, recoveries_by_location.values, label='Total Recoveries', color='cyan')
    ax2.set_ylabel('Total Recoveries')
    ax2.legend()
    ax2.ticklabel_format(style='plain', axis='y')  # Disable scientific notation.

    # Set major locator for the x-axis to be every 6 months.
    ax1.xaxis.set_major_locator(plt.MultipleLocator(180))
    ax2.xaxis.set_major_locator(plt.MultipleLocator(180))

def generate_plot(country):
    print(f'Generating plot for {country}')

    fig, axs = plt.subplots(3, 2, figsize=(15, 12), sharex=True)

    cases_by_location, deaths_by_location, recoveries_by_location = get_data_for_country(country)

    # Plotting all the data
    make_confirmed_cases_subplots(axs[0, 0], axs[0, 1], cases_by_location)
    make_deaths_subplots(axs[1, 0], axs[1, 1], deaths_by_location)
    make_recoveries_subplots(axs[2, 0], axs[2, 1], recoveries_by_location)

    # Rotate x-axis labels for better visibility.
    for ax in axs.flat:
        ax.tick_params(axis='x', rotation=45)

    # Add a title reporting the latest number of cases available.
    title = f"Analysis of the Impact of COVID-19 in {country}"
    plt.suptitle(title)

    plt.show()

if __name__ == "__main__":
    default_country = input('Enter the country, or press Enter to use "Germany": ')
    if not default_country:
        default_country = 'Germany'

    try:
        generate_plot(default_country.strip())
    except Exception as e:
        print('Error encountered:', e)