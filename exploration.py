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
# #####################################################################
import pandas as pd

# Display all columns.
pd.set_option('display.max_columns', 20)
# Stop wrapping.
pd.set_option('display.width', 1000)


# MAIN
# #####################################################################
def main() -> None:
    df = pd.read_csv('MASTER_DATAFRAME.csv')

    print(df.describe())


if __name__ == "__main__":
    main()
