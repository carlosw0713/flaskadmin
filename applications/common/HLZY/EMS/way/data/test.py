import re

# pattern = r'MAX\((PT_\d+)\)-MIN\((PT_\d+)\)\*CT_\d+'
pattern = r'CT_\d+'
pattern = r'MAX\((PT_\d+)\)-MIN\((PT_\d+)\)'
text = '(MAX(PT_01335)-MIN(PT_01335))*CT_00127'

match = re.search(pattern, text)
if match:
    # print(len(match))
    # pt1 = match.group(1)
    # pt2 = match.group(2)
    ct = match.group(0)  # 匹配整个表达式
    # print(f"Extracted PT values: {pt1}, {pt2}")
    print(f"Extracted CT value: {ct}")
else:
    print("No match found.")


pattern = r'.*?MAX\(PT_\d+\)-MIN\(PT_\d+\).*?\*CT_12333'

# 示例字符串
text = 'MAX(PT_01335)-MIN(PT_01335)'

# 查找是否符合该格式
match = re.match(pattern, text)

if match:
    # 提取 PT_ 值

    pt_values = re.findall(r'PT_\d+', match.group(0))
    pt_values = re.findall(r'PT_\d+', match.group(0))
    print("Extracted PT values:", pt_values)
else:
    print("The input does not match the required format.")