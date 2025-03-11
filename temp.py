import re
h = "```yaml"
s = re.search(r'```yaml',h)
print(s)