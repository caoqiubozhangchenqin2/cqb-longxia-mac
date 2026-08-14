from __future__ import annotations

from datetime import date


# WS/T 612—2018《7岁～18岁儿童青少年身高发育等级评价》
# Each row is -2SD, -1SD, median, +1SD, +2SD in centimetres.
CHINA_HEIGHT = {
    "男": {
        7:(113.51,119.49,125.48,131.47,137.46), 8:(118.35,124.53,130.72,136.90,143.08),
        9:(122.74,129.27,135.81,142.35,148.88), 10:(126.79,133.77,140.76,147.75,154.74),
        11:(130.39,138.20,146.01,153.82,161.64), 12:(134.48,143.33,152.18,161.03,169.89),
        13:(143.01,151.60,160.19,168.78,177.38), 14:(150.22,157.93,165.63,173.34,181.05),
        15:(155.25,162.14,169.02,175.91,182.79), 16:(157.72,164.15,170.58,177.01,183.44),
        17:(158.76,165.07,171.39,177.70,184.01), 18:(158.81,165.12,171.42,177.73,184.03),
    },
    "女": {
        7:(112.29,118.21,124.13,130.05,135.97), 8:(116.83,123.09,129.34,135.59,141.84),
        9:(121.31,128.11,134.91,141.71,148.51), 10:(126.38,133.78,141.18,148.57,155.97),
        11:(132.09,139.72,147.36,154.99,162.63), 12:(138.11,145.26,152.41,159.56,166.71),
        13:(143.75,149.91,156.07,162.23,168.39), 14:(146.18,151.98,157.78,163.58,169.38),
        15:(147.02,152.74,158.47,164.19,169.91), 16:(147.59,153.26,158.93,164.60,170.27),
        17:(147.82,153.50,159.18,164.86,170.54), 18:(148.54,154.28,160.01,165.74,171.48),
    },
}


def age_years(birth_date: str, on_date: str):
    born = date.fromisoformat(birth_date)
    measured = date.fromisoformat(on_date)
    return (measured - born).days / 365.2425


def reference_at_age(gender: str, age: float):
    table = CHINA_HEIGHT.get(gender, CHINA_HEIGHT["男"])
    if age < 7 or age > 18:
        return None
    low = max(7, min(18, int(age)))
    high = min(18, low + 1)
    if low == high:
        return table[low]
    fraction = age - low
    return tuple(round(a + (b - a) * fraction, 2) for a, b in zip(table[low], table[high]))


def evaluate_height(gender: str, age: float, height: float):
    values = reference_at_age(gender, age)
    if not values:
        return "暂无对应参考", None
    n2, n1, median, p1, p2 = values
    if height < n2:
        label = "低于 -2SD"
    elif height < n1:
        label = "-2SD～-1SD"
    elif height <= p1:
        label = "正常范围"
    elif height <= p2:
        label = "+1SD～+2SD"
    else:
        label = "高于 +2SD"
    return label, median


def midparental_target_height(gender: str, father_height, mother_height):
    """Return mid-parental adult target height and the conventional ±2 SD range.

    The AAP formula uses a 13 cm sex adjustment and a target range of ±10.2 cm.
    This is a broad genetic reference, not an individual adult-height prediction.
    """
    if father_height is None or mother_height is None:
        return None
    father = float(father_height)
    mother = float(mother_height)
    if father <= 0 or mother <= 0:
        return None
    adjustment = 13.0 if gender == "男" else -13.0
    target = (father + mother + adjustment) / 2
    return round(target, 1), round(target - 10.2, 1), round(target + 10.2, 1)
