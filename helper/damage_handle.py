#Helper function to determine the distance from bullet launch to bullet hit
def hit_distance(bullet):
    dx = bullet.x - bullet.start_x
    dy = bullet.y - bullet.start_y

    distance = ((dx**2) + (dy**2)) ** 0.5

    if distance < 100:
        return "CLOSE"
    else:
        return "LONG"

#Helper function that returns the side of the tank that has been hit
def hit_direction(bullet, taker):
    
    opposite = {"up" : "down",
                "down" : "up",
                "left" : "right",
                "right" : "left"}
    
    if bullet.direction == opposite[taker.direction]:
        return "FRONT"
    elif bullet.direction == taker.direction:
        return "BACK"
    else:
        return "SIDE"

#Calculating damage based on distance and tank side
def calculate_damage(bullet, taker):
    if hit_distance(bullet) == "CLOSE":
        if hit_direction(bullet, taker) == "SIDE":
            return 30
        elif hit_direction(bullet, taker) == "FRONT":
            return 20
        else:
            return 50
    else:
        if hit_direction(bullet, taker) == "SIDE":
            return 15
        elif hit_direction(bullet, taker) == "FRONT":
            return 10
        else:
            return 25


def deal_damage(bullet, taker):
    damage = calculate_damage(bullet, taker)
    taker.take_damage(damage)