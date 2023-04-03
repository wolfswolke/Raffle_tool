from collections import Counter

from logic.database_handler import read_db


def calculate_probabilities(list_item):
    total_tickets = len(list_item)
    counter = Counter(list_item)
    probabilities = {}
    for number, count in counter.items():
        probability = count / total_tickets
        probabilities[number] = probability
    return probabilities


raffle_list = list()
for items in read_db():
    for _ in range(items[3]):
        raffle_list.append(items[2])

probabilities_outer = calculate_probabilities(raffle_list)
sorted(probabilities_outer, key=probabilities_outer.get, reverse=True)
print(probabilities_outer)
