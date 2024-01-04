import re

f = open('total.xml','r')
res = f.readlines()
result = []
for d in res:
    data = re.findall('>(https:\/\/.+)<',d)
    for i in data:
       result.append(i)

print(len(result))