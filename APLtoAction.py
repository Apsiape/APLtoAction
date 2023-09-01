import os

# Function to read APL from a text file and return a list of lines
def read_apl_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        return None

# Function to write the converted GGL lines to a text file
def write_ggl_to_file(ggl_lines, file_name):
    with open(file_name, 'w') as file:
        for line in ggl_lines:
            file.write(f"{line}\n")

# Function to convert logical operators from WOW APL to GGL
def translate_logical_operators(condition):
    return condition.replace("&", " and ").replace("|", " or ")

# Function to convert buff and debuff conditions from WOW APL to GGL
def translate_conditions(conditions):
    translated_conditions = []
    for condition in conditions:
        condition = condition.strip()
        condition = translate_logical_operators(condition)
        if "buff." in condition:
            buff_name = condition.split(".")[1]
            translated_conditions.append(f"Unit(unitID):HasBuffs(A.{buff_name}.ID) > 0")
        elif "debuff." in condition:
            debuff_name = condition.split(".")[1]
            translated_conditions.append(f"Unit(unitID):HasDebuffs(A.{debuff_name}.ID) > 0")
        else:
            translated_conditions.append(condition)
    return " and ".join(translated_conditions)

# Function to convert a single line of WOW APL to Action/GGL syntax
def convert_apl_to_ggl(apl_line):
    if "#" in apl_line or not apl_line.strip():
        return None
    action, *conditions = apl_line.split(",")
    conditions = translate_conditions(conditions)
    ggl_action = f"A.{action.capitalize()}:IsReady(unitID)"

    if ggl_action:
        if conditions:
            return f"if {ggl_action} and {conditions} then return {ggl_action}:Show(icon) end"
        else:
            return f"if {ggl_action} then return {ggl_action}:Show(icon) end"
    return None

# Function to perform the entire APL to GGL conversion process
def apl_to_ggl_conversion(input_apl_file, output_ggl_file):
    apl_lines_from_file = read_apl_from_file(input_apl_file)
    if apl_lines_from_file:
        ggl_lines = [convert_apl_to_ggl(line) for line in apl_lines_from_file]
        ggl_lines = [line for line in ggl_lines if line]
        write_ggl_to_file(ggl_lines, output_ggl_file)

input_apl_file_name = input("Enter the name of the input APL text file (e.g., 'sample_apl.txt'): ")
output_ggl_file_name = input("Enter the name for the output GGL text file (e.g., 'converted_ggl.txt'): ")

if os.path.exists(input_apl_file_name):
    apl_to_ggl_conversion(input_apl_file_name, output_ggl_file_name)
    print(f"Conversion complete. The converted GGL is saved as '{output_ggl_file_name}'.")
else:
    print(f"The file '{input_apl_file_name}' does not exist in the current directory.")
