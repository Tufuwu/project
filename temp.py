import re
h = "runs-on: ubuntu-18.04'\n"
s = re.sub(r'ubuntu-\d+\.\d+','ubuntu-latest',h)
print(s)