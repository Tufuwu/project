import re
s = '#dffkoff'
d = 'dddd#dddd'
h = d.find('#')
for i in range(0,h):
    if d[i] != '':
        temp =d[:h]
        temp += '\n'
        print(temp)
        break
if s.find(s):
    print('ssss')








