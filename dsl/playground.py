from lark import Lark, Transformer, Tree
import utils


# Define the grammar for the DSL
# LABELS menas index or column labels
dsl_grammar = """
    start: command+
    command: drop | move | copy | merge | split | transpose | aggregate | test
    drop: "drop(" "table=" NAME "," "label=" label "," "axis=" AXIS ")"
    move: "move(" "table=" NAME "," "label=" label "," "target_table=" NAME "," "target_position=" NUMBER "," "axis=" AXIS ")"
    copy: "copy(" "table=" NAME "," "label=" label "," "target_table=" NAME "," "target_label=" NUMBER "," "axis=" AXIS ")"
    merge: "merge(" "table=" NAME "," "label_1=" label "," "label_2=" label "," "glue=" STRING "," "new_label=" label "," "axis=" AXIS ")"
    split: "split(" "table=" NAME "," "label=" label "," "delimiter=" STRING "," "new_labels=" labels "," "axis=" AXIS ")"
    transpose: "transpose(" "table=" NAME ")"
    aggregate: "aggregate(" "table=" NAME "," "label=" label "," "operation=" OPERATION "," "axis=" AXIS ")"
    test: "test(" "table=" NAME "," "label1=" label "," "label2=" label "," "strategy=" STRATEGY "," "axis=" AXIS ")"

    labels: "[" [label ("," label)*] "]"
    label: NAME | NUMBER

    NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
    AXIS: "0" | "1" | "index" | "columns"
    STRING : /"[^"]*"/
    OPERATION: "sum" | "mean" | "median" | "min" | "max"
    STRATEGY: "t-test" | "z-test" | "chi-squared"

    %import common.NUMBER
    %import common.WS
    %ignore WS
"""


class DSLTransformer(Transformer):
    def drop(self, args):
        return {"drop": {"table": args[0], "label": args[1], "axis": args[2]}}

    def move(self, args):
        return {
            "move": {
                "table": args[0],
                "label": args[1],
                "target_table": args[2],
                "target_position": args[3],
                "axis": args[4],
            }
        }

    def copy(self, args):
        return {
            "copy": {
                "table": args[0],
                "label": args[1],
                "target_table": args[2],
                "target_label": args[3],
                "axis": args[4],
            }
        }

    def merge(self, args):
        return {
            "merge": {
                "table": args[0],
                "label1": args[1],
                "label2": args[2],
                "glue": args[3],
                "new_label": args[4],
                "axis": args[5],
            }
        }

    def split(self, args):
        return {
            "split": {
                "table": args[0],
                "label": args[1],
                "delimiter": args[2],
                "new_labels": args[3],
                "axis": args[4],
            }
        }

    def transpose(self, args):
        return {"transpose": {"table": args[0]}}

    def aggregate(self, args):
        return {
            "aggregate": {
                "table": args[0],
                "label": args[1],
                "strategy": args[2],
                "operation": args[3],
                "axis": args[4],
            }
        }

    def test(self, args):
        return {
            "test": {
                "table": args[0],
                "label1": args[1],
                "label2": args[2],
                "strategy": args[3],
                "axis": args[4],
            }
        }


# Initialize Lark with the grammar
dsl_parser = Lark(dsl_grammar, parser="lalr", transformer=DSLTransformer())

def convert_axis(token):
    if token.value.isdigit():
        return int(token.value)
    elif token.value in ['index', 'columns']:
        return token.value
    else:
        raise ValueError(f"Unexpected token value: {token.value}")


# Function to parse and execute commands
def execute_dsl(tables, dsl_code):
    parsed = dsl_parser.parse(dsl_code)
    # print(parsed.pretty())  # This line prints the parsed tree in a readable format.

    for command in parsed.children:
        # print("Executing command:", command)
        if isinstance(command, Tree):
            command = command.children[0]
            command_type = list(command.keys())[0]

            table_name = command[command_type]["table"]
            table = tables[table_name]

            if command_type == "drop":
                label = command["drop"]["label"].children[0].value
                axis = convert_axis(command["drop"]["axis"])
                table = utils.drop(table, label, axis)
            elif command_type == "move":
                label = command["move"]["label"].children[0].value
                target_table = command["move"]["target_table"]
                target_position = command["move"]["target_position"].value
                axis = convert_axis(command["move"]["axis"])
                table, tables[target_table] = utils.move(
                    table, label, tables[target_table], target_position, axis
                )
            elif command_type == "copy":
                label = command["copy"]["label"]
                target_table = command["copy"]["target_table"]
                target_label = command["copy"]["target_label"]
                axis = convert_axis(command["copy"]["axis"])
                table = utils.copy(
                    table, label, tables[target_table], target_label, axis
                )
            elif command_type == "merge":
                label1 = command["merge"]["label1"]
                label2 = command["merge"]["label2"]
                glue = command["merge"]["glue"]
                new_label = command["merge"]["new_label"]
                axis = convert_axis(command["merge"]["axis"])
                table = utils.merge(table, label1, label2, glue, new_label, axis)
            elif command_type == "split":
                label = command["split"]["label"]
                delimiter = command["split"]["delimiter"]
                new_labels = command["split"]["new_labels"]
                axis = convert_axis(command["split"]["axis"])
                table = utils.split(table, label, delimiter, new_labels, axis)
            elif command_type == "transpose":
                table = utils.transpose(table)
            elif command_type == "aggregate":
                label = command["aggregate"]["label"]
                strategy = command["aggregate"]["strategy"]
                operation = command["aggregate"]["operation"]
                axis = convert_axis(command["aggregate"]["axis"])
                table = utils.aggregate(table, label, strategy, operation, axis)
            elif command_type == "test":
                label1 = command["test"]["label1"]
                label2 = command["test"]["label2"]
                strategy = command["test"]["strategy"]
                axis = convert_axis(command["test"]["axis"])
                table = utils.test(table, label1, label2, strategy, axis)
        else:
            print("Invalid command:", command)
        
        return tables
