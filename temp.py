import re
h = "111  - '3.4'"
s = re.sub(r'- \'3.[0-9]\'','- \'3.9\'',h)
print(s)