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
    x_list = list()
    institutions = list()

    for val in df[column].unique():
        x_list.append(val)
        institutions.append(df.loc[df[column] == val].shape[0])

    return x_list, institutions


def count_inst_by_col_per_student(df: pd.DataFrame, column=None, 
                                  columns=None, by_sector=False) -> (list, list):
    x_list = list()
    institutions = list()

    for year in df['YEAR'].unique():
        if column:
            x_list.append(year)
            institutions.append(
                (df[column].loc[df['YEAR'] == year].sum() / 
                df['TOTAL'].loc[df['YEAR'] == year].sum()) * 1000
            )
        elif columns:
            x_list.append(year)
            institutions.append(
                (df[columns].loc[df['YEAR'] == year].sum().sum() / 
                df['TOTAL'].loc[df['YEAR'] == year].sum()) * 1000
            )

    return x_list, institutions


def count_institutions_by_two_col(df: pd.DataFrame, x_axis: str, 
                                  legend_col: str, legend_vals: list,
                                  per_student=False, crime=None,
                                  crimes=None) -> dict:
    scatter_vals = dict()
    scatter_vals[x_axis] = list()
    
    for val in legend_vals:
        scatter_vals[val] = list()
        
    for xval in df[x_axis].unique():
        scatter_vals[x_axis].append(xval)
        for lval in legend_vals:
            if per_student == False:
                scatter_vals[lval].append(
                    df.loc[(df[x_axis] == xval) &\
                           (df[legend_col] == lval)].shape[0]
                )
            elif per_student and crime:
                scatter_vals[lval].append(
                    (df[crime].loc[(df[x_axis] == xval) &\
                           (df[legend_col] == lval)].sum() /
                    df['TOTAL'].loc[(df[x_axis] == xval) &\
                           (df[legend_col] == lval)].sum()) * 1000
                )
            elif per_student and crimes:
                scatter_vals[lval].append(
                    (df[crimes].loc[(df[x_axis] == xval) &\
                           (df[legend_col] == lval)].sum().sum() /
                    df['TOTAL'].loc[(df[x_axis] == xval) &\
                           (df[legend_col] == lval)].sum()) * 1000
                )
    
    return scatter_vals


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


def viz_scatterplot(x: list, y: list, title=None, xaxis_label=None,
                    yaxis_label=None, y_lim=None, y_color=None, y_label=None,
                    y2=None, y2_color=None, y2_label=None, y3=None, 
                    y3_color=None, y3_label=None, alpha=0.5):
    ax = plt.subplot()
    ax.set_title(title)
    ax.scatter(x, y, color=y_color, label=y_label, alpha=alpha)
    if y2 != None:
        ax.scatter(x, y2, color=y2_color, label=y2_label, alpha=alpha)
        ax.legend()
    if y3 != None:
        ax.scatter(x, y3, color=y3_color, label=y3_label, alpha=alpha)
        ax.legend()
    ax.set_ylabel(yaxis_label)
    ax.set_xlabel(xaxis_label)
    ax.set_ylim(y_lim)
    plt.show()


# MAIN
# ############################################################################
def main() -> None:
    df = import_clean_data('MASTER_DATAFRAME.csv')
    sectors = ['Public, 4-year or above', 'Private nonprofit, 4-year or above',
               'Private for-profit, 4-year or above']

    # Find number of institutions reporting crimes.
    x, y = count_institutions_by_col(df, 'YEAR')
    viz_scatterplot(x, y, title='Postsecondary 4 Year '
                                'Institutions Reporting Crimes',
                    xaxis_label='Year',
                    yaxis_label='# of Institutions', y_lim=[0, 1500])
    
    # Visualize number of institutions reporting crimes by sector.
    scatter_vals = count_institutions_by_two_col(df, 'YEAR', 'SECTOR_DESC',
                                                 sectors)
    values = list(scatter_vals.values())
    viz_scatterplot(values[0], values[1], title='Postsecondary 4 Year Institutions Reporting Crimes by Sector',
                    xaxis_label='Year', yaxis_label='# of Institutions',
                    y_color='#4bcc4b', y_label='Public', y_lim=[0, 1200],
                    y2=values[2], y2_label='Nonprofit', y2_color='#4b4bcc',
                    y3=values[3], y3_label='For-Profit', y3_color='#ff4b4b')
    
    # Visualize number of Liquor Crimes per 1000 Students.
    x, y = count_inst_by_col_per_student(df, column='LIQUOR')
    viz_scatterplot(x, y, title='Postsecondary 4 Year '
                                'Institutions Reporting Liquor Crimes',
                    xaxis_label='Year', y_lim=[0, 45],
                    yaxis_label='Reported Crimes Per 1000 Students')

    # Visualize number of Burglary Crimes per 1000 Students.
    x, y = count_inst_by_col_per_student(df, column='BURGLA')
    viz_scatterplot(x, y, title='Postsecondary 4 Year '
                                'Institutions Reporting Burglary Crimes',
                    xaxis_label='Year',
                    yaxis_label='Reported Crimes Per 1000 Students',y_lim=[0, 4])
    
    # Visualize number of Rape Crimes per 1000 Students.
    rape_cols = [col for col in df.columns if 'RAPE' in col]
    x, y = count_inst_by_col_per_student(df, columns=rape_cols)
    viz_scatterplot(x, y, title='Postsecondary 4 Year '
                                'Institutions Reporting Rape Crimes',
                    xaxis_label='Year',
                    yaxis_label='Reported Crimes Per 1000 Students', y_lim=[0, 1.5])
    
    # Visualize number of Rape Crimes per 1000 Students by sector.
    scatter_vals = count_institutions_by_two_col(df, 'YEAR', 'SECTOR_DESC', 
                                                 sectors, per_student=True, 
                                                 crimes=rape_cols)
    values = list(scatter_vals.values())
    viz_scatterplot(values[0], values[1], title='Postsecondary 4 Year Institutions Reporting Rape Crimes',
                    xaxis_label='Year', yaxis_label='Reported Crimes Per 1000 Students', 
                    y_color='#4bcc4b', y_label='Public', y_lim=[0, 2.5],
                    y2=values[2], y2_label='Nonprofit', y2_color='#4b4bcc',
                    y3=values[3], y3_label='For-Profit', y3_color='#ff4b4b')
    
    # Visualize number of Assault Crimes per 1000 Students by sector.
    assault_cols = [col for col in df.columns if 'AGG_A' in col]
    scatter_vals = count_institutions_by_two_col(df, 'YEAR', 'SECTOR_DESC', 
                                                 sectors, per_student=True, 
                                                 crimes=assault_cols)
    values = list(scatter_vals.values())
    viz_scatterplot(values[0], values[1], title='Postsecondary 4 Year Institutions Reporting Aggrevated Assault Crimes',
                    xaxis_label='Year', yaxis_label='Reported Crimes Per 1000 Students', 
                    y_color='#4bcc4b', y_label='Public', y_lim=[0, 2.5],
                    y2=values[2], y2_label='Nonprofit', y2_color='#4b4bcc',
                    y3=values[3], y3_label='For-Profit', y3_color='#ff4b4b')
    
    # Visualize number of Fondle Crimes per 1000 Students by sector.
    scatter_vals = count_institutions_by_two_col(df, 'YEAR', 'SECTOR_DESC', 
                                                 sectors, per_student=True, 
                                                 crime='FONDL')
    values = list(scatter_vals.values())
    viz_scatterplot(values[0], values[1], title='Postsecondary 4 Year Institutions Reporting Fondle Crimes',
                    xaxis_label='Year', yaxis_label='Reported Crimes Per 1000 Students', 
                    y_color='#4bcc4b', y_label='Public', y_lim=[0, 2.5],
                    y2=values[2], y2_label='Nonprofit', y2_color='#4b4bcc',
                    y3=values[3], y3_label='For-Profit', y3_color='#ff4b4b')


if __name__ == "__main__":
    main()
