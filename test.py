import re

line = '猎金游戏.2025.HD.1080P.国语中英双字'
match = re.match(r'^(.*?)\.\d{4}\.HD', line)
print(match.group(1))


