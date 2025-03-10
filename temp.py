import re
h = "actions/upload-artifact@v3"
s = re.sub(r'actions/upload-artifact@v\d','actions/upload-artifact@v4',h)
print(s)