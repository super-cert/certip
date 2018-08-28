import re
string = "country:        FR"

b = re.findall(r'ountry: +\w+',string)
print()
print(b)