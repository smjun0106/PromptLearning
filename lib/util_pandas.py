import os
import pandas as pd


def save_to_excel(df, excel_path="excel.xlsx", replace=False):
    if replace:
        if os.path.exists(excel_path):  # if file exists
            os.remove(excel_path)

        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
    else:
        if os.path.exists(excel_path):  # if file exists
            data = pd.read_excel(excel_path)  # load file
            start_row = data.shape[0] + 1  # add extra index for new line

            with pd.ExcelWriter(excel_path, mode='a', if_sheet_exists="overlay") as writer:
                df.to_excel(writer, index=False, startrow=start_row, header=False)

        else:
            with pd.ExcelWriter(excel_path, mode='w', engine='openpyxl') as writer:
                df.to_excel(writer, index=False)


def get_last_row(df, reverse_index=-1):
    """
    This function returns the last row of a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame from which to get the last row.

    Returns:
    pd.Series: The last row of the DataFrame.
    """
    if df.empty:
        raise ValueError("The DataFrame is empty")
    return df.iloc[reverse_index], len(df) + reverse_index


def add_item_with_new_column(df, new_item, row_index=1, column_name='B'):
    # Check if the column exists
    if column_name in df.columns:
        # Check if the cell contains a list
        df.at[row_index, column_name] = new_item
    else:
        # If the column does not exist, create it and add the new item
        df[column_name] = None
        df.at[row_index, column_name] = new_item

