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
import clery_collector
import pandas as pd
import unittest

# CONSTANT VARIABLES
# #####################################################################
REDUNDANT_COLUMNS = ['INSTNM', 'BRANCH', 'ADDRESS', 'CITY', 'STATE',
                     'ZIP', 'SECTOR_CD', 'SECTOR_DESC', 'MEN_TOTAL',
                     'WOMEN_TOTAL', 'TOTAL', 'UNITID_P']
COL_ID = 'UNITID_P'

# CLASS
# #####################################################################
class TestCleryCollector(unittest.TestCase):

    def test_cleanly_import_data(self):
        # testing if this is the first dataframe in program
        import_first_df = clery_collector.cleanly_import_data(
            'test_files/test_cleanly_import_data/'
            'noncampusarrest070809.csv',
            'FILTER07', 'FILTER08', 'FILTER09', 7, 8, True,
            'noncampusarrest'
        )

        expected_first_df = pd.read_csv(
            'test_files/test_cleanly_import_data/'
            'test_cleanly_import_data_firstdf_result.csv'
        )

        # testing if this is not the first dataframe in program
        import_not_first_df = clery_collector.cleanly_import_data(
            'test_files/test_cleanly_import_data/'
            'noncampusarrest070809.csv',
            'FILTER07', 'FILTER08', 'FILTER09', 7, 8, False,
            'noncampusarrest'
        )

        expected_not_first_df = pd.read_csv(
            'test_files/test_cleanly_import_data/'
            'test_cleanly_import_data_not_firstdf_result.csv'
        )

        pd.testing.assert_frame_equal(import_first_df,
                                      expected_first_df)
        pd.testing.assert_frame_equal(import_not_first_df,
                                      expected_not_first_df)

    def test_concat_dataframes(self):
        main_first_df = pd.DataFrame()

        main_not_first_df = pd.read_csv(
            'test_files/test_concat_dataframes/'
            'noncampusarrest070809.csv'
        )

        concat_df = pd.read_csv(
            'test_files/test_concat_dataframes/'
            'noncampusarrest080910.csv'
        )

        expected_df = pd.read_csv(
            'test_files/test_concat_dataframes/'
            'expected_concat_dataframes.csv'
        )

        result_first_df, result_not_first_bool = \
            clery_collector.concat_dataframes(main_first_df,
                                              concat_df,
                                              True)

        result_not_first_df, result_first_bool = \
            clery_collector.concat_dataframes(main_not_first_df,
                                              concat_df,
                                              False)

        pd.testing.assert_frame_equal(result_first_df,
                                      concat_df)
        pd.testing.assert_frame_equal(result_not_first_df,
                                      expected_df,
                                      False)

    def test_concat_list_elements(self):
        a_list = ['Hello', 'my', 'name', 'is', 'Elder', 'Gale']
        to_concat = 'UwU'
        expected_list = ['UwU_Hello', 'UwU_my', 'UwU_name', 'UwU_is',
                         'UwU_Elder', 'UwU_Gale']
        generated_list = clery_collector.concat_list_elements(a_list,
                                                              to_concat)

        self.assertEqual(generated_list, expected_list)

    def test_grab_strings_from_list(self):
        a_list = ['Janeway', 'Cisco', 'Picard', 'Kirk',
                  'Janice', 'Julia', 'January']
        grab = 'Jan'
        expected_list = ['Janeway', 'Janice', 'January']
        generated_list = clery_collector.grab_strings_from_list(a_list,
                                                                grab)
        self.assertEqual(generated_list, expected_list)

    def test_merge_dataframes(self):
        main_first_df = pd.DataFrame()

        main_not_first_df = pd.read_csv(
            'test_files/test_merge_dataframes/noncampusarrest070809.csv'
        )

        merge_crime_df = pd.read_csv(
            'test_files/test_merge_dataframes/noncampuscrime070809.csv'
        )

        result_first_df, result_first_bool = \
            clery_collector.merge_dataframes(main_first_df,
                                             merge_crime_df, True)

        result_not_first_df, result_not_first_bool = \
            clery_collector.merge_dataframes(main_not_first_df,
                                             merge_crime_df, False
        )
        result_not_first_df.to_csv("HELP.csv")
        expected_df = pd.read_csv(
            'test_files/test_merge_dataframes/test_merge_input.csv'
        )

        # if the df is the first one, it should not change
        pd.testing.assert_frame_equal(merge_crime_df,
                                      result_first_df)
        self.assertEqual(False, result_first_bool)
        # testing actual concatenation
        pd.testing.assert_frame_equal(expected_df,
                                      result_not_first_df)
        self.assertEqual(False, result_not_first_bool)

    def test_set_filter_name(self):
        self.assertEqual(clery_collector.set_filter_name(7, 8, 9),
                         ('FILTER07', 'FILTER08', 'FILTER09'))

    def test_set_year_code(self):
        self.assertEqual(clery_collector.set_year_code(9, 10, 11), '091011')

    def test_shorten_columns(self):
        exclude = ['INSTNM', 'BRANCH', 'ADDRESS', 'CITY', 'STATE',
                   'ZIP', 'SECTOR_CD', 'SECTOR_DESC', 'MEN_TOTAL',
                   'WOMEN_TOTAL', 'TOTAL', 'UNITID_P']
        generated_df = clery_collector.\
            shorten_columns(pd.read_csv('test_files/test_shorten_columns/'
                                        'noncampusarrest070809.csv'),
                            exclude)
        expected_df = pd.read_csv('test_files/test_shorten_columns/'
                                  'expected_shorten_columns.csv')
        pd.testing.assert_frame_equal(generated_df, expected_df)

    def test_subtract_list(self):
        first_list = ['Janeway', 'Kim', 'Paris', 'Tuvok', 'Nelix', 'Kes',
                      'Torres', 'Chakotay']
        second_list = ['Kes', 'Nelix', 'Paris']
        generated_list = clery_collector.subtract_list(first_list, second_list)
        expected_list = ['Janeway', 'Kim', 'Tuvok', 'Torres', 'Chakotay']
        self.assertEqual(generated_list, expected_list)


if __name__ == '__main__':
    unittest.main()