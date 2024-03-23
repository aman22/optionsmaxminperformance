import json
from prettytable import PrettyTable
from collections import Counter

def read_and_print_json(file_path):
    print(f"START---")
    try:
        # Open the JSON file for reading
        with open(file_path, 'r') as file:
            # Load the JSON data
            print(f"FILE OPEN ---")
            data = json.load(file)

            # #Print AS A TABLE
            # table = PrettyTable(data.keys())
            # # Add rows to the table
            # table.add_row(data.values())
            # # Iterate through the items in the JSON data and print their values
            # # for key, value in data.items():
            # #     print(f"{key}: {value}")
            # print(table)

            if isinstance(data, list):
                # Create a PrettyTable object with column names from the first object
                if data:
                    table = PrettyTable(data[0].keys())
                else:
                    print("Error: Empty JSON array.")
                    return

                # Add rows to the table
                for entry in data:
                    table.add_row(entry.values())

                # Print the table
                # print(table)
                print(f"Number of rows: {len(table.rows)}")
                print(f"Field names: {table.field_names}")
                count_distinct_values(table, 'sector')
            else:
                print("Error: JSON data is not an array.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

# Example usage:
#json_file_path = "/Users/amandetail/PycharmProjects/optionsmaxminperformance/data"
json_file_path = "/Users/Aman/PycharmProjects/optionsmaxminperformance/data_files/data-1row"

def count_distinct_values(table, column_name):
    # Get the index of the specified column
    column_index = table.field_names.index(column_name) if column_name in table.field_names else -1

    if column_index != -1:
        # Extract values from the specified column
        column_values = [row[column_index] for row in table.rows]

        # Count distinct values using Counter
        distinct_values_count = Counter(column_values)

        # Print the results
        print(f"Distinct values in '{column_name}':")
        for value, count in distinct_values_count.items():
            print(f"{value}: {count}")
    else:
        print(f"Error: Column '{column_name}' not found in the table.")
# Replace with the actual path to your JSON file
read_and_print_json(json_file_path)