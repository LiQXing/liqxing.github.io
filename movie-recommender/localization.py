"""Display-only Chinese names keyed by stable MovieLens movieId.

Original dataset titles and all recommendation scores remain untouched.
This curated list covers common films and the classroom demo, not all 62k
titles. Unknown titles intentionally retain their original names.
"""
import re

# Common mainland Chinese release names. Ambiguous/unverified titles, including
# Return with Honor (1998), intentionally have no entry.
MOVIE_TITLES_ZH = {
    1: "玩具总动员", 2: "勇敢者的游戏", 6: "盗火线", 10: "007之黄金眼",
    16: "赌城风云", 17: "理智与情感", 21: "矮子当道", 25: "离开拉斯维加斯",
    32: "十二猴子", 34: "小猪宝贝", 39: "独领风骚", 47: "七宗罪",
    50: "非常嫌疑犯", 70: "杀出个黎明", 95: "断箭", 110: "勇敢的心",
    111: "出租车司机", 150: "阿波罗13号", 153: "永远的蝙蝠侠", 165: "虎胆龙威3",
    172: "捍卫机密", 185: "网络惊魂", 223: "疯狂店员", 231: "阿呆与阿瓜",
    253: "夜访吸血鬼", 260: "星球大战4：新希望", 288: "天生杀人狂",
    292: "恐怖地带", 293: "这个杀手不太冷", 296: "低俗小说",
    316: "星际之门", 318: "肖申克的救赎", 344: "神探飞机头", 356: "阿甘正传",
    357: "四个婚礼和一个葬礼", 364: "狮子王", 367: "变相怪杰", 377: "生死时速",
    380: "真实的谎言", 457: "亡命天涯", 480: "侏罗纪公园", 500: "窈窕奶爸",
    527: "辛德勒的名单", 541: "银翼杀手", 588: "阿拉丁", 589: "终结者2：审判日",
    590: "与狼共舞", 592: "蝙蝠侠", 593: "沉默的羔羊", 595: "美女与野兽",
    597: "风月俏佳人", 608: "冰血暴", 648: "碟中谍", 668: "大地之歌",
    750: "奇爱博士", 780: "独立日", 858: "教父", 912: "卡萨布兰卡",
    919: "绿野仙踪", 924: "2001太空漫游", 1089: "落水狗",
    1136: "巨蟒与圣杯", 1193: "飞越疯人院", 1196: "星球大战5：帝国反击战",
    1197: "公主新娘", 1198: "夺宝奇兵", 1200: "异形2", 1201: "黄金三镖客",
    1206: "发条橙", 1208: "现代启示录", 1210: "星球大战6：绝地归来",
    1213: "好家伙", 1214: "异形", 1221: "教父2", 1240: "终结者",
    1246: "死亡诗社", 1258: "闪灵", 1265: "土拨鼠之日", 1270: "回到未来",
    1291: "夺宝奇兵3：圣战奇兵", 1580: "黑衣人", 1704: "心灵捕手",
    1721: "泰坦尼克号", 1923: "我为玛丽狂", 2028: "拯救大兵瑞恩",
    2329: "美国X档案", 2571: "黑客帝国", 2858: "美国丽人", 2959: "搏击俱乐部",
    3578: "角斗士", 4226: "记忆碎片", 4306: "怪物史瑞克",
    4993: "指环王1：护戒使者", 4973: "天使爱美丽", 5952: "指环王2：双塔奇兵",
    6016: "上帝之城", 6377: "海底总动员", 6539: "加勒比海盗：黑珍珠号的诅咒",
    6918: "大河之歌", 7153: "指环王3：王者无敌", 7361: "暖暖内含光",
    26073: "人间的条件 第三部", 26082: "切腹", 48516: "无间道风云",
    58559: "蝙蝠侠：黑暗骑士", 60069: "机器人总动员", 68157: "无耻混蛋",
    68954: "飞屋环游记", 79132: "盗梦空间", 82143: "荒野独居",
    89745: "复仇者联盟", 91529: "蝙蝠侠：黑暗骑士崛起", 93040: "美国内战",
    99114: "被解救的姜戈", 105250: "自我的世纪", 109487: "星际穿越",
    112852: "银河护卫队", 122882: "疯狂的麦克斯：狂暴之路", 140737: "谜之屋",
    151763: "死亡笔记特别篇：幻影之神", 159817: "地球脉动",
    165969: "超正常化", 170705: "兄弟连", 171011: "地球脉动 第二季",
    171495: "宇宙：个人游记", 179135: "蓝色星球 第二季",
    182723: "宇宙时空之旅", 198185: "双峰",
    48780: "致命魔术", 135456: "攻壳机动队 S.A.C. 笑面男",
}

GENRES_ZH = {
    "Action": "动作", "Adventure": "冒险", "Animation": "动画",
    "Children": "儿童", "Children's": "儿童", "Comedy": "喜剧",
    "Crime": "犯罪", "Documentary": "纪录片", "Drama": "剧情",
    "Fantasy": "奇幻", "Film-Noir": "黑色电影", "Horror": "恐怖",
    "IMAX": "IMAX", "Musical": "歌舞", "Mystery": "悬疑",
    "Romance": "爱情", "Sci-Fi": "科幻", "Thriller": "惊悚",
    "War": "战争", "Western": "西部", "(no genres listed)": "类型未标注",
}

def chinese_title(movie_id, original):
    name = MOVIE_TITLES_ZH.get(int(movie_id))
    if not name:
        return ""
    year = re.search(r"\((\d{4})\)$", str(original))
    return f"{name}（{year.group(1)}）" if year else name

def display_title(movie_id, original):
    return chinese_title(movie_id, original) or str(original)

def chinese_genres(value):
    return " / ".join(GENRES_ZH.get(g, g) for g in str(value).split("|"))

def with_chinese_titles(frame):
    """Add a translation column without changing the original title column."""
    result = frame.copy()
    result["title_zh"] = [chinese_title(mid, title) for mid, title in zip(result.movieId, result.title)]
    return result
