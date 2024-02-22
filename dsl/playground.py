from lark import Lark, Transformer, Tree
import pandas as pd

# Define the temporary table for testing
table1 = pd.DataFrame(
    {
        "col1": [1, 2, 3, 4, 5],
        "col2": [6, 7, 8, 9, 10],
        "col3": [11, 12, 13, 14, 15],
    }
)

# Define a dictionary to map table names to DataFrame objects
tables = {"table1": table1}

# Define the grammar for the DSL
# LABELS menas index or column labels
dsl_grammar = """
    start: command+
    command: drop | split | move
    drop: "drop(" "table=" NAME "," "labels=" labels "," "axis=" AXIS ")"
    move: "move(" "table=" NAME "," "from=" NUMBER "," "to=" NUMBER ")"
    split: "split(" [args] ")"
    args: [arg ("," arg)*]
    arg: NAME "=" (NAME | NUMBER)

    labels: "[" [label ("," label)*] "]"
    label: NAME | NUMBER

    NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
    AXIS: "0" | "1"
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""


class DSLTransformer(Transformer):
    def drop(self, args):
        return {"drop": {"table": args[0], "labels": args[1], "axis": args[2]}}

    def split(self, args):
        # Implement the logic for split here
        return {"split": args}

    def arg(self, args):
        return {args[0]: args[1]}

    def labels(self, args):
        # Convert the list of label Trees into a list of label values
        return [label.children[0].value for label in args]


# Initialize Lark with the grammar
dsl_parser = Lark(dsl_grammar, parser="lalr", transformer=DSLTransformer())


# Function to parse and execute commands
def execute_dsl(dsl_code):
    parsed = dsl_parser.parse(dsl_code)
    # print(parsed.pretty())  # This line prints the parsed tree in a readable format.

    for command in parsed.children:
        print("Executing command:", command)
        if isinstance(command, Tree):
            command = command.children[0]
            if "drop" in command:
                table_name = command["drop"]["table"]
                labels = command["drop"]["labels"]
                axis = int(command["drop"]["axis"])
                # if the labels does not exist in the table's columns, then skip
                if (not set(labels).issubset(tables[table_name].columns)) and axis == 1:
                    print("Invalid column's labels:", labels)
                    continue
                if axis == 0:
                    labels = [int(label) for label in labels]
                    if not set(labels).issubset(tables[table_name].index):
                        print("Invalid index labels:", labels)
                        continue
                table = tables[table_name]
                table.drop(labels=labels, axis=axis, inplace=True)
                print("Table after drop:\n", table)

        else:
            print("Invalid command:", command)


# Test the interpreter
dsl_code_1 = """
    drop(table=table1, labels=[col1, col2], axis=1)
"""

dsl_code_2 = """
    drop(table=table1, labels=[1, 2], axis=0)
"""
execute_dsl(dsl_code_1)
