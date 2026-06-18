import pygame

def hit_distance(dealer, taker):
    dx = taker.x - dealer.x
    dy = taker.y - dealer.y

    distance = ((dx**2) + (dy**2)) ** 0.5

    if distance < 100:
        return "CLOSE"
    else:
        return "LONG"


def hit_direction(dealer, taker):
    if dealer.direction == "up":
        if taker.direction == "left" or taker.direction == "right":
            return "SIDE"
        elif taker.direction == "up":
            return "BACK"
        else:
            return "FRONT"
    elif dealer.direction == "down":
        if taker.direction == "left" or taker.direction == "right":
            return "SIDE"
        elif taker.direction == "down":
            return "BACK"
        else:
            return "FRONT"
    elif dealer.direction == "left":
        if taker.direction == "up" or taker.direction == "down":
            return "SIDE"
        elif taker.direction == "left":
            return "BACK"
        else:
            return "FRONT"
    else:
        if taker.direction == "up" or taker.direction == "down":
            return "SIDE"
        elif taker.direction == "right":
            return "BACK"
        else:
            return "FRONT"

def calculate_damage(dealer, taker):
    if hit_distance(dealer, taker) == "CLOSE":
        if hit_direction(dealer, taker) == "SIDE":
            return 30
        elif hit_direction(dealer, taker) == "FRONT":
            return 20
        else:
            return 50
    else:
        if hit_direction(dealer, taker) == "SIDE":
            return 15
        elif hit_direction(dealer, taker) == "FRONT":
            return 10
        else:
            return 25


def deal_damage(dealer, taker):
    damage = calculate_damage(dealer, taker)
    taker.take_damage(damage)