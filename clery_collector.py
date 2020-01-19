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
from string import digits

# Display all columns.
pd.set_option('display.max_columns', None)
# Stop wrapping.
pd.set_option('display.width', 1000)

# CONSTANT VARIABLES
# #####################################################################
# REPORT_TYPES = ['noncampusarrest', 'noncampuscrime',
#                 'noncampusdiscipline', 'noncampushate',
#                 'oncampusarrest', 'oncampuscrime',
#                 'oncampusdiscipline', 'oncampushate',
#                 'publicpropertyarrest', 'publicpropertycrime',
#                 'publicpropertydiscipline', 'publicpropertyhate',
#                 'reportedarrest', 'reportedcrime', 'reporteddiscipline',
#                 'reportedhate', 'residencehallarrest',
#                 'residencehallcrime', 'residencehalldiscipline',
#                 'residencehallhate']
REPORT_TYPES = ['noncampusarrest', 'noncampuscrime']
COLUMN_TYPES = ['']
FILE_TYPE = '.csv'
FILE_PATH = 'data/'
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
COL_YEAR_INDEX = 13

EXPORT_FILE_NAME = 'MASTER_DATAFRAME.csv'


# FUNCTIONS
# #####################################################################
def cleanly_import_data(file_name: str, filter1: str, filter2: str,
                        filter3: str, year: int, middle_year: int,
                        first_df: bool, report_type: str) \
                        -> pd.DataFrame:
    df = pd.read_csv(file_name, low_memory=False)

    # capitalize all columns
    df.columns = [name.upper() for name in df.columns]

    # drop redundant or unnecessary data
    df.drop(columns=[filter1, filter2, filter3], inplace=True)
    if not first_df:
        df.drop(columns=REDUNDANT_COLUMNS, inplace=True)

    # remove first two years of data
    stat_list = list(df.columns)
    first_year_list = grab_strings_from_list(stat_list, str(year))
    second_year_list = grab_strings_from_list(stat_list, str(middle_year))
    df.drop(columns=first_year_list, inplace=True)
    df.drop(columns=second_year_list, inplace=True)

    # make columns unique to report type
    stat_list = list(df.columns)
    for index, column in enumerate(stat_list):
        # line below by user valignatev from stack overflow
        # https://stackoverflow.com/questions/12851791/removing-numbers-from-string
        stat_list[index] = column.translate({ord(k): None for k in digits})
    renamed_list = concat_list_elements(stat_list, report_type)
    for col_name, col_rename in zip(df.columns, renamed_list):
        if col_name != COL_ID and col_name not in REDUNDANT_COLUMNS:
            df.rename(columns={col_name: col_rename}, inplace=True)

    return df


def concat_dataframes(main_df: pd.DataFrame,
                      concat_df: pd.DataFrame,
                      first_df: bool) -> (pd.DataFrame, bool):
    if first_df:
        first_df = False
        main_df = concat_df
    else:
        main_df = pd.concat([main_df, concat_df],
                            join='outer', sort=False)

    return main_df, first_df


def concat_list_elements(a_list: list, to_concat: str) -> list:
    return [str(to_concat + '_' + item) for item in a_list]


def export_dataframe(df: object, file_name: object) -> object:
    print('Exporting dataframe to ' + file_name + '...')
    df.to_csv(file_name)
    print('Successfully exported!')


def grab_strings_from_list(a_list: list, grab: str) -> list:
    return [item for item in a_list if grab in item]


def merge_dataframes(main_df: pd.DataFrame,
                     merge_df: pd.DataFrame,
                     first_df: bool) -> (pd.DataFrame, bool):
    if first_df:
        first_df = False
        main_df = merge_df
    else:
        main_df = pd.merge(main_df, merge_df, on=COL_ID)

    return main_df, first_df


def print_progress(current_step: int, first_step: int, last_step: int):
    steps = last_step - first_step
    progress = int(((current_step - first_step) / steps) * 100)
    progress_left = 100 - progress
    progress_bar = '[' + ('=' * progress) + (' ' * progress_left) + ']'
    print(progress_bar + ' ' + str(progress) + '%')


def set_filter_name(first_year: int, second_year: int,
                    third_year: int) -> (str, str, str):
    filter1 = 'FILTER{:02d}'.format(first_year)
    filter2 = 'FILTER{:02d}'.format(second_year)
    filter3 = 'FILTER{:02d}'.format(third_year)

    return filter1, filter2, filter3


def set_year_code(first_year: int, second_year: int,
                  third_year: int) -> str:
    return '{:02d}'.format(first_year) + '{:02d}'.format(second_year) \
            + '{:02d}'.format(third_year)


def shorten_columns(df: pd.DataFrame) -> pd.DataFrame:
    stat_list = list(df.columns)

    for index, column in enumerate(stat_list):
        if column != COL_ID and column not in REDUNDANT_COLUMNS:
            stat_list[index] = column[column.find('_')+1:]

    df.columns = stat_list

    return df


def subtract_list(first_list: list, second_list: list) -> list:
    return [item for item in first_list if item not in second_list]


# MAIN
# #####################################################################
def main() -> None:
    master_df = None
    year_df = None
    first_df = True
    first_master_df = True

    for year in range(FIRST_REPORTED_YEAR, LAST_REPORTED_YEAR - 1):
        # generate year code
        middle_year = year + 1
        upper_year = year + 2
        # each data has a year code (example: '070809')
        year_code = set_year_code(year, middle_year, upper_year)

        # generate filter names
        filter1, filter2, filter3 = set_filter_name(year, middle_year,
                                                    upper_year)

        for report_type in REPORT_TYPES:
            # generate file name
            file_name = FILE_PATH + report_type + year_code + FILE_TYPE

            report_df = cleanly_import_data(file_name, filter1, filter2,
                                            filter3, year, middle_year,
                                            first_df, report_type)
            year_df, first_df = merge_dataframes(year_df,
                                                 report_df, first_df)

        # add year of data reports
        year_df.insert(loc=COL_YEAR_INDEX,
                       column=COL_YEAR, value=upper_year)

        # append year dataframe to master dataframe
        master_df, first_master_df = concat_dataframes(master_df,
                                                       year_df,
                                                       first_master_df)
        first_df = True

        print_progress(upper_year, FIRST_REPORTED_YEAR, LAST_REPORTED_YEAR)

    # delete report type from columns
    master_df = shorten_columns(master_df)

    # column sum code by user meteore from stack overflow
    # https://stackoverflow.com/questions/13078751/
    # combine-duplicated-columns-within-a-dataframe/13083900
    master_df = master_df.groupby(master_df.columns, axis=1, sort=False).sum()

    # print dataframe to excel
    export_dataframe(master_df, EXPORT_FILE_NAME)


if __name__ == "__main__":
    main()
