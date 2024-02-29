import pandas as pd
from collections import OrderedDict


def drop(table, labels, axis):
    if axis == 1 or axis == "columns":
        if not set(labels).issubset(table.columns):
            raise ValueError(f"Invalid column labels:{labels}")
    if axis == 0 or axis == "index":
        labels = [int(label) for label in labels]
        if not set(labels).issubset(table.index):
            raise ValueError(f"Invalid index labels:{labels}")

    print("Table before column move:\n", table)

    table.drop(labels=labels, axis=axis, inplace=True)

    print("Table after drop:\n", table)
    return table


def move(table, column, to):
    if column not in table.columns:
        raise ValueError(f"Column {column} does not exist in the DataFrame")

    num_columns = len(table.columns)
    if to < 0 or to >= num_columns:
        raise ValueError(f"New position {to} is out of bounds")

    print("Table before column move:\n", table)

    column_to_move = table[column]

    table.drop(labels=[column], axis="columns", inplace=True)
    table.insert(loc=to, column=column, value=column_to_move)

    print("Table after column move:\n", table)
    return table


def copy(table, column, new_column):
    if column not in table.columns:
        raise ValueError(f"Column {column} does not exist in the DataFrame")
    if new_column in table.columns:
        raise ValueError(
            f"New column label {new_column} already exists in the DataFrame"
        )
    print("Table before column copy:\n", table)
    table[new_column] = table[column].copy()
    print("Table after column copy:\n", table)
    return table


def merge(table, column1, column2, glue, new_column):
    if column1 not in table.columns:
        raise ValueError(f"Column {column1} does not exist in the DataFrame")
    if column2 not in table.columns:
        raise ValueError(f"Column {column2} does not exist in the DataFrame")
    if new_column in table.columns:
        raise ValueError(
            f"New column label {new_column} already exists in the DataFrame"
        )
    print("Table before column merge:\n", table)
    table[new_column] = table[column1].astype(str) + glue + table[column2].astype(str)
    print("Table after column merge:\n", table)
    return table


def split(table, column, delimiter, new_columns):
    if column not in table.columns:
        raise ValueError(f"Column {column} does not exist in the DataFrame")
    if len(new_columns) != 2:
        raise ValueError("new_labels must contain exactly two new column names")

    print("Table before column split:\n", table)
    table[new_columns[0]], table[new_columns[1]] = zip(
        *table[column].str.split(delimiter, n=1).tolist()
    )
    print("Table after column split:\n", table)

    return table


def fold(table, column):
    # Find the index of the column name
    if column not in table.columns:
        raise ValueError(f"Column {column} does not exist in the DataFrame")
    print("Table before column split:\n", table)
    column_index = table.columns.get_loc(column)

    # Prepare an empty list to hold the new rows
    new_rows = []

    # Iterate over each row in the DataFrame
    for _, row in table.iterrows():
        # For each column after the specified index, create a new row
        # with the value from the pivot column and the current column
        for col in table.columns[column_index + 1:]:
            new_row = [row[column], row[col]]  # Use column_name directly
            new_rows.append(new_row)

    new_table = pd.DataFrame(new_rows, columns=[column, "folded_value"])
    print("Table after column split:\n", new_table)
    return new_table


def unfold(table):
    print("Table before column split:\n", table)
    # Create an OrderedDict to maintain the order of groups as they're encountered
    temp = OrderedDict()
    
    # Iterate through the DataFrame rows
    for index, row in table.iterrows():
        # Use all but the last column as the key, accessing values explicitly
        t = tuple(row.iloc[:-1])
        # Append the last value using .iloc to access by position
        if t in temp:
            temp[t].append(row.iloc[-1])
        else:
            temp[t] = [row.iloc[-1]]
    
    # Determine the maximum number of columns required
    max_col = max(len(v) for v in temp.values())
    
    # Prepare the unfolded DataFrame
    unfolded_data = []
    
    # Populate the unfolded_data list with rows expanded according to temp
    for key, values in temp.items():
        row = list(key)
        row.extend(values + [''] * (max_col - len(values)))  # Extend with values and fill the rest with blanks
        unfolded_data.append(row)
    
    # Convert unfolded_data into a DataFrame
    column_names = list(table.columns[:-1]) + [f'col_{i}' for i in range(max_col)]
    unfolded_table = pd.DataFrame(unfolded_data, columns=column_names)
    print("Table after column split:\n", unfolded_table)
    return unfolded_table


def fill(table, column):
    if column not in table.columns:
        raise ValueError(f"Column {column} does not exist in the DataFrame")

    # Fill empty cells with the value from above
    table[column].fillna(method="ffill", inplace=True)

    return table


def delete(table, predicate, axis):
    if axis == 0:  # Delete rows
        # Apply the predicate across each row
        # The predicate function should be designed to operate on row series or individual values depending on the use case
        rows_to_delete = table.apply(lambda row: predicate(row), axis=1)
        filtered_table = table[~rows_to_delete]
    elif axis == 1:  # Delete columns
        # Apply the predicate across each column
        columns_to_delete = [col for col in table.columns if predicate(table[col])]
        filtered_table = table.drop(columns=columns_to_delete)
    else:
        raise ValueError("Axis must be 0 (rows) or 1 (columns)")

    return filtered_table


def transpose(table):
    return table.transpose()
