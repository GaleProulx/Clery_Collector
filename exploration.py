# Author: Gale Proulx
# Class:  CCC-410ITS
# Certification of Authenticity:
# I certify that this is my work and the DAT-330 class work,
# except where I have given fully documented references to the work
# of others. I understand the definition and consequences of plagiarism
# and acknowledge that the assessor of this assignment may, for the purpose
# of assessing this assignment reproduce this assignment and provide a
# copy to another member of academic staff and / or communicate a copy of
# this assignment to a plagiarism checking service(which may then retain a
# copy of this assignment on its database for the purpose of future
# plagiarism checking).

# IMPORT DEPENDENCIES & SET CONFIGURATION
# ############################################################################
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

from sklearn.linear_model import LinearRegression

INFO_COLS = ['UNITID_P', 'INSTNM', 'BRANCH', 'ADDRESS', 'CITY', 'STATE',
             'ZIP', 'SECTOR_CD', 'SECTOR_DESC', 'MEN_TOTAL',
             'WOMEN_TOTAL', 'TOTAL', 'YEAR']

# Display all columns.
pd.set_option('display.max_columns', 20)
# Stop wrapping.
pd.set_option('display.width', 1000)


# IMPORT DEPENDENCIES & SET CONFIGURATION
# ############################################################################
def count_institutions_by_col(df: pd.DataFrame, column: str) -> (list, list):
    filter_list = list()
    institutions = list()

    for val in df[column].unique():
        filter_list.append(val)
        institutions.append(len(df.loc[df[column] == val]['INSTNM'].unique()))

    return filter_list, institutions


def count_crimes(df: pd.DataFrame, x_var: str, y_var: list, legend=None):
    if legend != None:
        category = list(df[legend].unique())
        stats = dict()
        
        for value in category:
            stats[value] = list()
    
        # find all colleges that reported crimes in respective categories
        x_axis = list()
        for x in df[x_var].unique():
            x_axis.append(x)
            for value in category:
                stats[value].append(df[y_var].loc[(df[x_var] == x) & (df[legend] == value)].sum().sum())
                    
    return list(df[x_var].unique()), stats


def import_clean_data(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename)

    # gather all crime columns with more than one crime reported
    stat_cols = [col for col in df.columns if col not in INFO_COLS]
    stat_cols = [col for col in stat_cols if df[col].sum() > 0]

    # remove all rows with no crimes reported
    important = df[df[stat_cols].sum(axis=1) != 0]

    # remove all 2 year institutions
    important = important.loc[important['SECTOR_CD'] < 4]
    important = important.loc[important['SECTOR_CD'] > 0]

    # only include main campus and remove all columns with no crimes reported
    important = important.loc[important['BRANCH'].str.contains('Main Campus',
                                                               case=False,
                                                               regex=False)]
    important = important[stat_cols + INFO_COLS]

    return important


def linear_regression(features: pd.DataFrame, target: pd.DataFrame):
    model = LinearRegression()
    model.fit(features, target)

    print("### LINEAR REGRESSION MODEL ###")
    print("R-Squared Value: " + str(model.score(features, target)))
    print("Intercept: " + str(model.intercept_))
    print("Coefficients: " + str(model.coef_))


def viz_scatterplot(x: list, y: list, title=None, x_label=None,
                    y_label=None, y_lim=None):
    ax = plt.subplot()
    ax.set_title(title)
    
    if isinstance(y, dict):
        for key in y:
            ax.scatter(x, y[key], label=key)
            ax.legend(loc=0)
    else:
        ax.scatter(x, y)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_ylim(y_lim)
    plt.show()


# MAIN
# ############################################################################
def main() -> None:
    df = import_clean_data('MASTER_DATAFRAME.csv')

    # Gather number of institutions in total that are reporting crimes.
    year, inst_report = count_institutions_by_col(df, 'YEAR')
    viz_scatterplot(year, inst_report, title='Postsecondary 4 Year Institutions ' +
                    'Reporting Crimes', x_label='Year', 
                    y_label='# of Institutions', y_lim=[0, 1500])
    
    rape_cols = [col for col in df.columns if 'RAPE' in col]
    x, y = count_crimes(df, 'YEAR', rape_cols, 'SECTOR_DESC')
    y['Total Institutions'] = inst_report
    viz_scatterplot(x, y, title='Postsecondary 4 Year Institutions Reporting Rape',
                    x_label='Year', y_label='# of Institutions')
    
    x, y = count_crimes(df, 'YEAR', ['LIQUOR'], 'SECTOR_DESC')
    y['Total Institutions'] = inst_report
    viz_scatterplot(x, y, title='Postsecondary 4 Year Institutions Reporting Liquor Crimes',
                    x_label='Year', y_label='# of Institutions')
    
    stat_cols = [col for col in df.columns if col not in INFO_COLS]
    x, y = count_crimes(df, 'YEAR', stat_cols, 'SECTOR_DESC')
    viz_scatterplot(x, y, title='Postsecondary 4 Year Institutions Total Crimes',
                x_label='Year', y_label='# of Institutions')

    
if __name__ == "__main__":
    main()
