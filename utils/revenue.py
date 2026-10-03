from config.settings import DEFAULT_AOV, DEFAULT_CR, DEFAULT_TRAFFIC


def calculate_loss(ux, speed, trust):
    avg_score = (ux + speed + trust) / 3

    if avg_score < 4:
        improvement = 0.40
    elif avg_score < 6:
        improvement = 0.25
    elif avg_score < 8:
        improvement = 0.15
    else:
        improvement = 0.05

    current_revenue = DEFAULT_TRAFFIC * DEFAULT_CR * DEFAULT_AOV
    loss = current_revenue * improvement

    return int(loss), int(current_revenue), improvement