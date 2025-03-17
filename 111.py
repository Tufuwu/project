import yaml

with open("D:/vscode/3/project/data1/aiven/pghoard/action.yml", "r") as f:
    data = yaml.safe_load(f)

print(data)