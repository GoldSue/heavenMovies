import re

# 清洗函数
def clean(text):
    return text.replace('\xa0', ' ').replace('\u3000', ' ').strip()

raw_data = [
    '\r\n', '\r\n', '◎译\u3000\u3000名\u3000K-POP：猎魔女团/韩流：恶魔猎人/韩流女团：恶魔猎人/Kpop 猎魔女团',
    '◎片\u3000\u3000名\u3000K-Pop: Demon Hunters', '◎年\u3000\u3000代\u30002025',
    '◎产\u3000\u3000地\u3000美国', '◎类\u3000\u3000别\u3000喜剧/动作/动画/音乐/歌舞/奇幻/冒险',
    '◎语\u3000\u3000言\u3000英语/韩语', '◎字\u3000\u3000幕\u3000中文',
    '◎上\u3000日期\u30002025-06-20(美国)', '◎IMDb评分\xa0 7.9/10 from 4206 users',
    '◎片\u3000\u3000长\u300095分钟', '◎导\u3000\u3000演\u3000克里斯·艾伯翰斯 Chris Appelhans',
    '　　玛吉·康 Maggie Kang',
    '◎编\u3000\u3000剧\u3000克里斯·艾伯翰斯 Chris Appelhans', '　　Danya Jimenez',
    '　　玛吉·康 Maggie Kang', '　　Hannah McMechan',
    '◎主\u3000\u3000演\u3000赵雅顿 Arden Cho', '　　梅·洪 May Hong', '　　柳智英 Ji-young Yoo',
    '　　安孝燮 Hyo-seop Ahn', '　　金允珍 Yunjin Kim', '　　郑肯 Ken Jeong',
    '　　李炳宪 Byung-hun Lee', '　　金大贤 Daniel Dae Kim', '　　Rumi Oak Rumi Oak',
    '　　乔尔·金·布斯特 Joel Kim Booster', '　　丽兹·考什 Liza Koshy', '　　Alan Lee Alan Lee',
    '　　赵胜汪 SungWon Cho', '　　玛吉·康 Maggie Kang',
    '　　约翰·埃里克·本特利 John Eric Bentley', '　　Nathan Schauf Nathan Schauf',
    '　　Charlene Ramos Charlene Ramos', '　　Cori Baik Cori Baik',
    '　　Jennifer Sun Bell Jennifer Sun Bell', '　　Kira Tamagawa Kira Tamagawa',
    '◎简\u3000\u3000介',
    '　　她们不只是演唱会一票难求的人气女团，更是斩妖除魔的超强高手！韩流巨星鲁米、米拉和佐依私底下化身为魔物猎人，竭尽全力保护歌迷，对抗无所不在的异界威胁。如今，她们必须联手面对至今最大的敌人：一群以男团之姿迷倒万千粉丝的魔鬼。',
    'K-POP：猎魔女团.2025.BD.1080P.中字', ' ', '\r\n\r\n\r\n', '\r\n\r\n      '
]

result = {}
current_key = None
multiline_buffer = []

for line in raw_data:
    line = clean(line)
    if not line:
        continue

    if line.startswith('◎'):
        if current_key and multiline_buffer:
            result[current_key] = '\n'.join(multiline_buffer).strip()
            multiline_buffer = []

        match = re.match(r'◎([^\s]+[\s\u3000]+[^\s\u3000]+)(.*)', line)
        if match:
            current_key = match.group(1).strip()  # 去除"◎"
            value = match.group(2).strip()
            if value:
                result[current_key] = value
                current_key = None
        else:
            current_key = line.lstrip('◎').strip()
    else:
        if current_key:
            multiline_buffer.append(line)

if current_key and multiline_buffer:
    result[current_key] = '\n'.join(multiline_buffer).strip()

# 输出字典
from pprint import pprint
pprint(result, sort_dicts=False)
