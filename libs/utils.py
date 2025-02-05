import os
import sys
import pandas as pd
from datetime import datetime
from .constants import OUTPUT_FOLDER


def generate_excel_report(df_source, df_target, primary_key_col_nm):
    try:

        # Make df columns case-insensitive by converting col names in both files to same case
        # & makesure no whitespaces around
        df_source = df_source.rename(columns=lambda x: x.strip().upper())
        df_target = df_target.rename(columns=lambda x: x.strip().upper())
        df_row_count = pd.DataFrame([(df_source.shape[0], df_target.shape[0])],
                                    columns=["source_row_count", "target_row_count"])
        
        # convert the primary key column case to upper
        primary_key_col_nm = primary_key_col_nm.upper()

        if df_source.empty or df_target.empty:
            error = "source or Target data cannot be empty.."
            print(error)
            raise Exception(error)

        # Validating source & target files.
        validate_primary_key_column(df_source, 'source', primary_key_col_nm)
        validate_primary_key_column(df_target, 'target', primary_key_col_nm)
        validate_columns_in_source_and_target(df_source, df_target)

        empty_df = pd.DataFrame(columns=df_target.columns.to_list())
        cols_ordered = get_columns_in_required_order(empty_df, primary_key_col_nm)

        # Find out the newly added & deleted rows from target/recent file
        add_rows_id_list, del_rows_id_list = get_id_list_for_added_deleted_rows(
            df_source, df_target, primary_key_col_nm)

        # Get the df for newly added & deleted rows
        add_rows_df = get_df_for_added_rows(df_target, add_rows_id_list, empty_df,
                                            cols_ordered, primary_key_col_nm)
        del_rows_df = get_df_for_deleted_rows(df_source, del_rows_id_list, empty_df,
                                              cols_ordered, primary_key_col_nm)

        # concatenate the add_rows_df & del_rows_df in to a single df
        add_del_rows_df = pd.concat([add_rows_df, del_rows_df], axis=0, ignore_index=True)
        add_del_rows_df = add_del_rows_df.fillna("")

        df_src_update = df_source[~df_source[primary_key_col_nm].isin(del_rows_id_list)]
        df_trgt_update = df_target[~df_target[primary_key_col_nm].isin(add_rows_id_list)]

        df_src_trgt_update = pd.merge(df_src_update, df_trgt_update, how="inner",
                                      on=primary_key_col_nm, suffixes=("", "_NEW"))
        df_src_trgt_update = df_src_trgt_update[cols_ordered]

        var_cols = empty_df.drop(primary_key_col_nm, axis=1).columns.to_list()

        # Adding Status Column
        df_src_trgt_update["STATUS"] = df_src_trgt_update.apply(get_status, axis=1, args=(var_cols,))
        print("Fetching the Updated Rows data from the target file..")
        df_src_trgt_update = df_src_trgt_update[df_src_trgt_update['STATUS'] == 'UPDATED']
        df_src_trgt_update = get_df_with_only_updated_values(df_src_trgt_update, var_cols)

        # concatenating the add_del_rows_df & df_src_trgt_update
        df_final = pd.concat([add_del_rows_df, df_src_trgt_update], axis=0, ignore_index=True)
        status_column_val = df_final.pop('STATUS')
        df_final.insert(1, 'STATUS', status_column_val)
        df_final = df_final.fillna("")
        dt_str = datetime.now().strftime("%Y%m%d%H%M%S")

        # Generating XLSX Report
        print('Generating the XLSX Status Report dynamically with ADDED, '
                    'UPDATED and DELETED info..')
        output_file_path = os.path.join(OUTPUT_FOLDER, f"delta_report_{dt_str}.xlsx")
        with pd.ExcelWriter(output_file_path, engine="xlsxwriter") as writer:
            df_final.to_excel(writer, index=False, sheet_name="comparison_result")
            df_row_count.to_excel(writer, index=False, sheet_name="row_count")

        print(f'XLSX Report Path: "{output_file_path}"')
        print("Finished Execution for Data comparison....")

    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        exception_details = (f"Exception Type: {exc_type} Exception value: {value} "
                             f"at line no: {tb.tb_lineno}")
        print(exception_details)
        raise Exception(e)


def validate_primary_key_column(df, type, prime_key):
    """
    This function is used to validate if primary key is present in dataframe & unique
    :param df: Dataframe
    :param type: source/target
    :param prime_key: name of a column which acts like Primary key/composite in source/target file sheet
    :return: True/None: True--> only if validation passed  & if validation failed exception will be thrown
    """
    try:
        print(f"Validating the if Primary key is available in df..")
        if not prime_key.upper() in [col.upper() for col in df.columns.to_list()]:
            error = (f"Primary key '{prime_key}' provided in config.json file is "
                     f"not found in source/target files..")
            raise Exception(error)

        print(f"Validating the Primary key for any duplicates in {type} data")
        df.dropna(subset=[prime_key], inplace=True)
        # df = df[df[prime_key] != 0]
        # df = df[df[prime_key] != ""]
        # df = df[df[prime_key] != "0"]
        dup_df = df[df[prime_key].duplicated()]
        if dup_df.shape[0]:
            dup_prime_keys = list(set(dup_df[f'{prime_key}'].values))
            error = f"Duplicate values found in '{type}' data PrimaryKey '{prime_key}' : '{dup_prime_keys}' "
            print(error)
            return dup_prime_keys
            # raise Exception(error)
        else:
            print('valid..')
            return []
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        exception_details = (f"Exception Type: {exc_type} Exception value: {value} "
                             f"at line no: {tb.tb_lineno}")
        print(exception_details)
        raise Exception(e)


def validate_columns_in_source_and_target(df_source, df_target):
    """
    This function is used to check if same columns are present in both source and target data frames.

    :param df_source: source  dataframe
    :param df_target: target  dataframe
    :return: True/None: True--> only if validation passed  & if validation failed exception will be thrown
    """
    try:
        print(f"Validating if same columns are present in both source and target data.. ")
        src_cols = df_source.columns.to_list()
        trgt_cols = df_target.columns.to_list()
        diff_in_cols = set(src_cols)-set(trgt_cols) or set(trgt_cols)-set(src_cols)
        if diff_in_cols:
            missmatch_cols = (set(src_cols) - set(trgt_cols)) .union(set(trgt_cols) - set(src_cols))
            error = f"columns missmatch found between source & target data. mismatch_columns: {missmatch_cols}"
            print(error)
            raise Exception(error)
        else:
            print("valid...")
            return True
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        exception_details = (f"Exception Type: {exc_type} Exception value: {value} "
                             f"at line no: {tb.tb_lineno}")
        print(exception_details)
        raise Exception(e)


def get_columns_in_required_order(empty_df, prime_key):
    """
    This function is used to place the columns in the required order &
    update the column names(_NEW as Postfix) in target df

    :param empty_df: empty dataframe with all the columns from source/target file
    :param prime_key: primary key column name
    :return: cols: All the source and target df columns in the required order
    """
    try:
        cols = [prime_key]
        for col in empty_df.columns.to_list():
            if col != prime_key:
                cols.append(col)
                cols.append(f"{col}_NEW")
        return cols
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        exception_details = (f"Exception Type: {exc_type} Exception value: {value} "
                             f"at line no: {tb.tb_lineno}")
        print(exception_details)
        raise Exception(e)


def get_id_list_for_added_deleted_rows(df_source, df_target, prime_key_col_nm):
    """
    This function is used to figure out the list of ids which are newly added in
    target file & which are newly deleted in target file when compared with source file.

    :param df_source: source file dataframe
    :param df_target: target file dataframe
    :param prime_key_col_nm: primary key column name
    :return: newly_added_rows, deleted_rows
    """
    try:
        source_id_list = set(df_source[prime_key_col_nm].values)
        target_id_list = set(df_target[prime_key_col_nm].unique())
        newly_added_rows = list(target_id_list - source_id_list)
        deleted_rows = list(source_id_list - target_id_list)
        print(f"Id's of newly added rows in target file: {newly_added_rows}")
        print(f"Id's of deleted rows in target file: {deleted_rows}")
        return newly_added_rows, deleted_rows
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        exception_details = (f"Exception Type: {exc_type} Exception value: {value} "
                             f"at line no: {tb.tb_lineno}")
        print(exception_details)
        raise Exception(e)


def get_df_for_added_rows(df_target, new_rows_id_list, empty_df, cols_ordered,
                          primary_key_col_nm):
    """
    This function will filter the df_target dataframe based on new_rows_id_list
    & creates a new df for  newly added rows.

    :param df_target: target dataframe
    :param new_rows_id_list: list of id's of newly added rows in target file
    :param empty_df: empty dataframe with source/target columns
    :param cols_ordered: list of required columns in the expected order
    :param primary_key_col_nm: Primary key column name
    :return: new_rows_df: df for newly added rows
    """
    try:
        print('Fetching the data for newly added rows if any..')
        # Get the df for newly added rows & will merge it with empty df to get the desired output format
        new_rows_df = df_target[df_target[primary_key_col_nm].isin(new_rows_id_list)]
        new_rows_df = pd.merge(empty_df, new_rows_df, suffixes=('', '_NEW'),
                               on=primary_key_col_nm, how='outer')
        new_rows_df = new_rows_df[cols_ordered]
        new_rows_df['STATUS'] = "ADDED"
        return new_rows_df
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        exception_details = (f"Exception Type: {exc_type} Exception value: {value} "
                             f"at line no: {tb.tb_lineno}")
        print(exception_details)
        raise Exception(e)


def get_df_for_deleted_rows(df_source, del_rows_id_list, empty_df, cols_ordered,
                                  primary_key_col_nm):
    """
    This function will filter the df_target dataframe based on del_rows_id_list
    & creates a new df for  newly deleted rows.

    :param df_source: source data frame
    :param del_rows_id_list: target dataframe
    :param empty_df: empty dataframe
    :param cols_ordered: list of required columns in the expected order
    :param primary_key_col_nm: Primary key column name
    :return: del_rows_df: df for newly deleted rows
    """

    try:
        print('Fetching the data for deleted rows if any..')
        # Get the df for deleted rows & will merge it with empty df to get the desired output format
        del_rows_df = df_source[df_source[primary_key_col_nm].isin(del_rows_id_list)]
        del_rows_df = pd.merge(del_rows_df, empty_df, suffixes=('', '_NEW'),
                               on=primary_key_col_nm, how='outer')
        del_rows_df = del_rows_df[cols_ordered]
        del_rows_df['STATUS'] = "DELETED"
        return del_rows_df
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        exception_details = (f"Exception Type: {exc_type} Exception value: {value} "
                             f"at line no: {tb.tb_lineno}")
        print(exception_details)
        raise Exception(e)


def get_status(row, cols):
    """
    This function basically takes the df row (source & target info) as input & it will compare
    the values between the source & target columns & return status accordingly..

    :param row: data frame row
    :param cols: dataframe columns
    :return: "NO CHANGE"/ "UPDATED" : NO CHANGE--> no update happened in the row &
                                      UPDATED --> Update happened for atleast one value in the row
    """
    try:
        status = "NO CHANGE"
        for col in cols:
            src_col = col
            trgt_col = f"{src_col}_NEW"
            if str(row[src_col]).strip().lower() != str(row[trgt_col]).strip().lower():
                status = "UPDATED"
                return status
        return status
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        exception_details = (f"Exception Type: {exc_type} Exception value: {value} "
                             f"at line no: {tb.tb_lineno}")
        print(exception_details)
        raise Exception(e)


def get_df_with_only_updated_values(df_src_trgt_update, cols):
    """
    This function takes the df_src_trgt_update as input and it will replace
    the values with empty string ""  in the dataframe if there is no update
    happened between src & target column values..

    :param df_src_trgt_update: Dataframe with source & target info.
    :param cols: list of columns which is eligible for value comparison
    :return: df_src_trgt_update: modified dataframe with only updated values
    """
    try:
        for index, row in df_src_trgt_update.iterrows():
            for col in cols:
                src_col = col
                trgt_col = f"{src_col}_NEW"
                if str(row[src_col]).strip().lower() == str(row[trgt_col]).strip().lower():
                    df_src_trgt_update.at[index, src_col] = ""
                    df_src_trgt_update.at[index, trgt_col] = ""
        return df_src_trgt_update
    except Exception as e:
        exc_type, value, tb = sys.exc_info()
        exception_details = (f"Exception Type: {exc_type} Exception value: {value} "
                             f"at line no: {tb.tb_lineno}")
        print(exception_details)
        raise Exception(e)


