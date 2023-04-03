import random

from logic.database_handler import alter_db


def start_raffle(sql_data, number_of_drafts, raffle_list, winning_price):
    ticket_count = (len(raffle_list))
    print("Ticket Count: {}".format(ticket_count))
    winner_list = []
    user_data = []

    for items in sql_data:
        user_data.append(items)

    raffle_range = _get_raffle_data(raffle_list)
    raffles = 0

    while raffles < number_of_drafts:
        winner_position = _draft(raffle_range)
        raffle_dict = dict(enumerate(raffle_list))
        winner_id = raffle_dict[winner_position]

        if winner_id in winner_list:
            print("{} has already won. Redrawing.".format(winner_id))
        else:
            alter_db(winner_id, winning_price)
            raffle_range = _get_raffle_data(raffle_list)
            winner_list.append(winner_id)
            raffles += 1

    print(f"The winners are: ")
    for items in winner_list:
        print(f"{items}")


def _draft(raffle_range):
    return random.randint(0, raffle_range)


def _get_raffle_data(user_data):
    raffle_range = len(user_data) - 1
    return raffle_range
