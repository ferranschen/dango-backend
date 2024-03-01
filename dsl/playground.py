from lark import Lark, Transformer, Tree
import utils


# Define the grammar for the DSL
# LABELS menas index or column labels
dsl_grammar = """
    start: command+
    command: drop | move | copy | merge | split | fold | unfold | transpose
    drop: "drop(" "table=" NAME "," "labels=" labels "," "axis=" AXIS ")"
    move: "move(" "table=" NAME "," "column=" label "," "to=" NUMBER ")"
    copy: "copy(" "table=" NAME "," "column=" label "," "new_column=" label ")"
    merge: "merge(" "table=" NAME "," "column1=" label "," "column2=" label "," "glue=" STRING "," "new_column=" label ")"
    split: "split(" "table=" NAME "," "column=" label "," "delimiter=" STRING "," "new_columns=" labels ")"
    fold: "fold(" "table=" NAME "," "column=" label ")"
    unfold: "unfold(" "table=" NAME ")"
    transpose: "transpose(" "table=" NAME ")"

    labels: "[" [label ("," label)*] "]"
    label: NAME | NUMBER

    NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
    AXIS: "0" | "1" | "index" | "columns"
    STRING : /"[^"]*"/
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""


class DSLTransformer(Transformer):
    def drop(self, args):
        return {"drop": {"table": args[0], "labels": args[1], "axis": args[2]}}

    def move(self, args):
        return {"move": {"table": args[0], "column": args[1], "to": args[2]}}
    
    def copy(self, args):
        return {"copy": {"table": args[0], "column": args[1], "new_column": args[2]}}
    
    def merge(self, args):
        return {"merge": {"table": args[0], "column1": args[1], "column2": args[2], "glue": args[3], "new_column": args[4]}}
    
    def split(self, args):
        return {"split": {"table": args[0], "column": args[1], "delimiter": args[2], "new_columns": args[3]}}
    
    def fold(self, args):
        return {"fold": {"table": args[0], "column": args[1]}}
    
    def unfold(self, args):
        return {"unfold": {"table": args[0]}}
    
    def transpose(self, args):
        return {"transpose": {"table": args[0]}}

    def labels(self, args):
        # Convert the list of label Trees into a list of label values
        return [label.children[0].value for label in args]


# Initialize Lark with the grammar
dsl_parser = Lark(dsl_grammar, parser="lalr", transformer=DSLTransformer())


# Function to parse and execute commands
def execute_dsl(tables, dsl_code):
    parsed = dsl_parser.parse(dsl_code)
    print(parsed.pretty())  # This line prints the parsed tree in a readable format.

    for command in parsed.children:
        print("Executing command:", command)
        if isinstance(command, Tree):
            command = command.children[0]
            command_type = list(command.keys())[0]

            table_name = command[command_type]["table"]
            table = tables[table_name]

            if command_type == "drop":
                labels = command["drop"]["labels"]
                axis = int(command["drop"]["axis"])
                table = utils.drop(table, labels, axis)
            elif command_type == "move":
                column = command["move"]["column"].children[0]
                to = int(command["move"]["to"])
                table = utils.move(table, column, to)
            elif command_type == "copy":
                column = command["copy"]["column"].children[0]
                new_column = command["copy"]["new_column"].children[0]
                table = utils.copy(table, column, new_column)
            elif command_type == "merge":
                column1 = command["merge"]["column1"].children[0]
                column2 = command["merge"]["column2"].children[0]
                glue = command["merge"]["glue"].strip('"')
                new_column = command["merge"]["new_column"].children[0]
                table = utils.merge(table, column1, column2, glue, new_column)
            elif command_type == "split":
                column = command["split"]["column"].children[0]
                delimiter = command["split"]["delimiter"].strip('"')
                new_columns = command["split"]["new_columns"]
                table = utils.split(table, column, delimiter, new_columns)
            elif command_type == "fold":
                column = command["fold"]["column"].children[0]
                table = utils.fold(table, column)
            elif command_type == "unfold":
                table = utils.unfold(table)
            elif command_type == "extract":
                column_name = command["extract"]["column_name"].children[0]
                pattern = command["extract"]["pattern"]
                table = utils.extract(table, column_name, pattern)
            elif command_type == "transpose":
                table = utils.transpose(table)

        else:
            print("Invalid command:", command)
