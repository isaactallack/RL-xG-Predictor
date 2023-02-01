from math import exp, factorial
from collections import defaultdict
import matplotlib.pyplot as plt

def poisson_probability(k: int, lam: float) -> float:
    """
    Calculate the probability of getting k successes in a Poisson
    process with rate lam.
    """
    return (lam ** k) * exp(-lam) / factorial(k)

def create_poisson_distribution(lam: float) -> defaultdict:
    """
    Create a Poisson distribution centered around lam.
    """
    poisson_distribution = defaultdict(float)
    for k in range(0, 26): # maximum possible goals in Rocket League is 25
        poisson_distribution[k] = poisson_probability(k, lam)
    return poisson_distribution

def calculate_win_probability(expected_goals_a: float, expected_goals_b: float) -> float:
    """
    Calculate the percentage chance that team A wins the match based on the
    percentage that the Poisson score is higher than team B's.
    """
    distribution_a = create_poisson_distribution(expected_goals_a)
    distribution_b = create_poisson_distribution(expected_goals_b)

    win_probability = 0.0
    draw_probability = 0.0
    for goals_a, probability_a in distribution_a.items():
        for goals_b, probability_b in distribution_b.items():
            if goals_a > goals_b:
                win_probability += probability_a * probability_b
            elif goals_a == goals_b:
                draw_probability += probability_a * probability_b

# Write a function to plot a graph of two poisson distributions 

    win_probability += draw_probability / 2
    return win_probability