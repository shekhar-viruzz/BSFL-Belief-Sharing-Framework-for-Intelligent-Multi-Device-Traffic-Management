import re


input_file = "routes.rou.xml"
output_file = "routes_heavy.rou.xml"


with open(input_file, "r") as f:
    data = f.read()



def compress(match):

    depart = float(match.group(1))

    # 1 hour traffic -> 10 minutes
    new_depart = depart / 6

    return f'depart="{new_depart:.2f}"'



data = re.sub(
    r'depart="([0-9.]+)"',
    compress,
    data
)



with open(output_file, "w") as f:
    f.write(data)



print("Created:", output_file)
