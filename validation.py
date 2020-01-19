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
#
# INCLUDES ALL REPORT TOTALS BY YEAR

# IMPORT DEPENDENCIES & SET CONFIGURATION
# #####################################################################
import pandas as pd
import numpy as np
from string import digits
import csv

# Display all columns.
pd.set_option('display.max_columns', None)
# Stop wrapping.
pd.set_option('display.width', 1000)

# CONSTANT VARIABLES
# #####################################################################
REPORT_TYPES = ['noncampusarrest', 'noncampuscrime',
                'noncampusdiscipline', 'noncampushate',
                'oncampusarrest', 'oncampuscrime',
                'oncampusdiscipline', 'oncampushate',
                'publicpropertyarrest', 'publicpropertycrime',
                'publicpropertydiscipline', 'publicpropertyhate',
                'reportedarrest', 'reportedcrime', 'reporteddiscipline',
                'reportedhate', 'residencehallarrest',
                'residencehallcrime', 'residencehalldiscipline',
                'residencehallhate']
# REPORT_TYPES = ['noncampusarrest', 'noncampuscrime']
COLUMN_TYPES = ['']
FILE_TYPE = '.csv'
FILE_PATH = 'data/'
MASTER_DF_FILE_NAME = 'MASTER_DATAFRAME_NO_GROUP.csv'
REDUNDANT_COLUMNS = ['INSTNM', 'BRANCH', 'ADDRESS', 'CITY', 'STATE',
                     'ZIP', 'SECTOR_CD', 'SECTOR_DESC', 'MEN_TOTAL',
                     'WOMEN_TOTAL', 'TOTAL']
FIRST_REPORTED_YEAR = 7
LAST_REPORTED_YEAR = 17

COL_ID = 'UNITID_P'
COL_MEN = 'MEN_TOTAL'
COL_WOMEN = 'WOMEN_TOTAL'
COL_TOTAL = 'TOTAL'
COL_YEAR = 'YEAR'


# FUNCTIONS
# #####################################################################
def cleanly_import_data(file_name: str, year: int) -> pd.DataFrame:
    df = pd.read_csv(FILE_PATH + file_name, index_col=COL_ID, low_memory=False)
    df.columns = [name.upper() for name in df.columns]

    # remove first two years of data
    stat_list = list(df.columns)
    first_year_list = filter_string_from_list(stat_list, str(year))
    second_year_list = filter_string_from_list(stat_list, str(year + 1))
    df.drop(columns=first_year_list, inplace=True)
    df.drop(columns=second_year_list, inplace=True)
    filter_list = [column for column in df.columns if column.startswith("FILTER")]
    df.drop(columns=filter_list, inplace=True)
    df.drop(columns=REDUNDANT_COLUMNS, inplace=True)

    return df


def filter_string_from_list(a_list: list, filter: str) -> list:
    return [item for item in a_list if filter in item]


def set_year_code(first_year: int, second_year: int,
                  third_year: int) -> str:
    year_code = ''

    if first_year <= 7:
        year_code = '0' + str(first_year) + '0' + str(second_year) + '0' + str(third_year)
    elif first_year <= 8:
        year_code = '0' + str(first_year) + '0' + str(second_year) + str(third_year)
    elif first_year <= 9:
        year_code = '0' + str(first_year) + str(second_year) + str(third_year)
    else:
        year_code = str(first_year) + str(second_year) + str(third_year)

    return year_code


def subtract_list(first_list: list, second_list: list) -> list:
    return [item for item in first_list if item not in second_list]


# MAIN
# #####################################################################
def main() -> None:
    year_code = ''
    year = 0
    middle_year = 0
    upper_year = 0
    file_name = ''
    master_df = pd.read_csv(FILE_PATH + MASTER_DF_FILE_NAME, index_col=COL_ID, low_memory=False)
    year_df = None
    report_df = None
    matches = dict()
    error = False

    for year in range(FIRST_REPORTED_YEAR, LAST_REPORTED_YEAR - 1):
        # generate year code
        year_code = ''
        middle_year = year + 1
        upper_year = year + 2
        # each data has a year code (example: '070809')
        year_code = set_year_code(year, middle_year, upper_year)
        year_df = master_df.loc[master_df[COL_YEAR] == upper_year]

        for report_type in REPORT_TYPES:
            # generate file name
            file_name = report_type + year_code + FILE_TYPE
            report_df = cleanly_import_data(file_name, year)
            error = ""

            report_columns = report_df.columns

            for column in report_columns:
                for index, row in report_df.iterrows():
                    year_df_column = report_type + '_' + column.translate({ord(k): None for k in digits})
                    if str(report_df.loc[index, column]) == str(year_df.loc[index, year_df_column]):
                        error = str(report_df.loc[index, column]) + ", " + str(year_df.loc[index, year_df_column])

            matches[str(report_type) + " " + str(upper_year)] = error
            print(matches)

    with open('validation.csv', 'w', newline="") as csv_file:
        writer = csv.writer(csv_file)
        for key, value in matches.items():
            writer.writerow([key, value])
    print("Program Done.")


if __name__ == "__main__":
    main()
