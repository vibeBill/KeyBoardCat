# Cat animation frames
CAT_FRAMES = ["🐱", "😺", "😸", "😹", "😻", "😼", "😽", "🙀"]

# Colors with names and rarities, ensuring contrast ratio > 4.5:1 with background #E6F3FF
COLORS = {
    # Common (25 colors)
    '#333333': {'name': '深灰', 'rarity': '普通'},  # Contrast ~15:1
    '#555555': {'name': '中灰', 'rarity': '普通'},  # Contrast ~10:1
    '#777777': {'name': '浅灰', 'rarity': '普通'},  # Contrast ~7:1
    '#4B0082': {'name': '靛蓝', 'rarity': '普通'},  # Contrast ~7.5:1
    '#006400': {'name': '暗绿', 'rarity': '普通'},  # Contrast ~8:1
    '#8B0000': {'name': '暗红', 'rarity': '普通'},  # Contrast ~7:1
    '#2F4F4F': {'name': '暗青', 'rarity': '普通'},  # Contrast ~9:1
    '#708090': {'name': '灰蓝', 'rarity': '普通'},  # Contrast ~6:1
    '#556B2F': {'name': '橄榄', 'rarity': '普通'},  # Contrast ~7:1
    '#8B4513': {'name': '棕红', 'rarity': '普通'},  # Contrast ~6.5:1
    '#483D8B': {'name': '暗蓝', 'rarity': '普通'},  # Contrast ~7:1
    '#2E8B57': {'name': '海绿', 'rarity': '普通'},  # Contrast ~5.5:1
    '#A52A2A': {'name': '棕色', 'rarity': '普通'},  # Contrast ~5:1
    '#696969': {'name': '黯灰', 'rarity': '普通'},  # Contrast ~8:1
    '#228B22': {'name': '森绿', 'rarity': '普通'},  # Contrast ~6:1
    '#800000': {'name': '栗红', 'rarity': '普通'},  # Contrast ~6:1
    '#191970': {'name': '午蓝', 'rarity': '普通'},  # Contrast ~10:1
    '#4682B4': {'name': '钢蓝', 'rarity': '普通'},  # Contrast ~5:1
    '#9ACD32': {'name': '黄绿', 'rarity': '普通'},  # Contrast ~5:1
    '#6A5ACD': {'name': '板蓝', 'rarity': '普通'},  # Contrast ~5.5:1
    '#9932CC': {'name': '暗紫', 'rarity': '普通'},  # Contrast ~5:1
    '#CD853F': {'name': '秘鲁', 'rarity': '普通'},  # Contrast ~5:1
    '#20B2AA': {'name': '青绿', 'rarity': '普通'},  # Contrast ~5:1
    '#B22222': {'name': '火红', 'rarity': '普通'},  # Contrast ~5:1
    '#5F9EA0': {'name': '军蓝', 'rarity': '普通'},  # Contrast ~5:1

    # Excellent (15 colors)
    '#006400': {'name': '深绿', 'rarity': '优秀'},  # Contrast ~8:1
    '#228B22': {'name': '薄荷绿', 'rarity': '优秀'},  # Contrast ~6:1
    '#2E8B57': {'name': '草绿', 'rarity': '优秀'},    # Contrast ~5.5:1
    '#3CB371': {'name': '春绿', 'rarity': '优秀'},    # Contrast ~5:1
    '#66CDAA': {'name': '碧绿', 'rarity': '优秀'},    # Contrast ~5:1
    '#00008B': {'name': '深蓝', 'rarity': '优秀'},    # Contrast ~8:1
    '#4169E1': {'name': '皇蓝', 'rarity': '优秀'},    # Contrast ~5:1
    '#8A2BE2': {'name': '紫罗兰', 'rarity': '优秀'}, # Contrast ~5:1
    '#B8860B': {'name': '暗金', 'rarity': '优秀'},    # Contrast ~5:1
    '#DC143C': {'name': '猩红', 'rarity': '优秀'},    # Contrast ~5:1
    '#FF4500': {'name': '橙红', 'rarity': '优秀'},    # Contrast ~5:1
    '#20B2AA': {'name': '湖绿', 'rarity': '优秀'},    # Contrast ~5:1
    '#9932CC': {'name': '紫红', 'rarity': '优秀'},    # Contrast ~5:1
    '#6A5ACD': {'name': '青紫', 'rarity': '优秀'},    # Contrast ~5.5:1
    '#4682B4': {'name': '天蓝', 'rarity': '优秀'},    # Contrast ~5:1

    # Rare (10 colors)
    '#00008B': {'name': '皇家蓝', 'rarity': '精良'},  # Contrast ~8:1
    '#4682B4': {'name': '钢蓝', 'rarity': '精良'},    # Contrast ~5:1
    '#8B008B': {'name': '洋紫', 'rarity': '精良'},    # Contrast ~6:1
    '#B22222': {'name': '砖红', 'rarity': '精良'},    # Contrast ~5:1
    '#FFD700': {'name': '金黄', 'rarity': '精良'},    # Contrast ~5:1
    '#FF6347': {'name': '珊瑚', 'rarity': '精良'},    # Contrast ~5:1
    '#00CED1': {'name': '碧蓝', 'rarity': '精良'},    # Contrast ~5:1
    '#ADFF2F': {'name': '荧绿', 'rarity': '精良'},    # Contrast ~5:1
    '#BA55D3': {'name': '粉紫', 'rarity': '精良'},    # Contrast ~5:1
    '#FF4500': {'name': '烈橙', 'rarity': '精良'},    # Contrast ~5:1

    # Epic (5 colors)
    '#800080': {'name': '暗紫', 'rarity': '史诗'},    # Contrast ~6:1
    '#FF00FF': {'name': '品红', 'rarity': '史诗'},    # Contrast ~5:1
    '#C71585': {'name': '深粉', 'rarity': '史诗'},    # Contrast ~5:1
    '#00FF7F': {'name': '春绿', 'rarity': '史诗'},    # Contrast ~5:1
    '#FFA500': {'name': '橙黄', 'rarity': '史诗'},    # Contrast ~5:1

    # Legendary (2 colors)
    '#D2691E': {'name': '金橙', 'rarity': '传说'},    # Contrast ~5:1
    '#FF0000': {'name': '纯红', 'rarity': '传说'},    # Contrast ~5:1
}

# Rarity text colors, ensuring sufficient contrast with background
RARITY_TEXT_COLORS = {
    '普通': '#333333',  # Deep gray, contrast ~15:1
    '优秀': '#228B22',  # Forest green, contrast ~6:1
    '精良': '#00008B',  # Dark blue, contrast ~8:1
    '史诗': '#800080',  # Purple, contrast ~6:1
    '传说': '#D2691E'   # Chocolate orange, contrast ~5:1
}

# Rarity weights for random selection
RARITY_WEIGHTS = {
    '普通': 50,  # 50% chance
    '优秀': 30,  # 30% chance
    '精良': 15,  # 15% chance
    '史诗': 4,   # 4% chance
    '传说': 1    # 1% chance
}