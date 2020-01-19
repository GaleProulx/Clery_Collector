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

# Display all columns.
pd.set_option('display.max_columns', None)
# Stop wrapping.
pd.set_option('display.width', 1000)

# CONSTANT VARIABLES
# #####################################################################
FILE_TYPE = '.csv'
FILE_PATH = 'data/'

MAIN_FILE_NAME = 'MASTER_DATAFRAME_Outer_Join'
PROBABILITY_FILE_NAME = 'Probabilities_Dataframe'

PROBABILITY_MULTIPLIER_COLUMN = 'TOTAL'
ID_COLUMN = 'UNITID_P'


# FUNCTIONS
# #####################################################################
def import_data(file_name: str, file_type: str) -> pd.DataFrame:
    df = pd.read_csv(file_name + file_type)

    return df


# MAIN
# #####################################################################
def main() -> None:
    master_df = import_data(FILE_PATH + MAIN_FILE_NAME, FILE_TYPE)
    probability_df = import_data(FILE_PATH + PROBABILITY_FILE_NAME, FILE_TYPE)
    fake_df = pd.DataFrame(columns=master_df.columns)
    fake_df[ID_COLUMN] = master_df[ID_COLUMN]

    for column in master_df:
        if pd.notna(probability_df.loc[0, column]):
            fake_df[column] = master_df[PROBABILITY_MULTIPLIER_COLUMN] \
                                     * probability_df.loc[0, column]

    print(fake_df)


if __name__ == "__main__":
    main()
