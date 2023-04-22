import sqlite3
import matplotlib.pyplot as plt

def get_avg_brewery_type_by_state(cur):
    """
    Returns a dictionary with the average brewery type for each state.

    :param cur: a cursor object for the database
    :return: a dictionary with the average brewery type for each state
    """
    cur.execute("""
        SELECT States.state, Types.type, COUNT(*) as num_breweries
        FROM Breweries
        JOIN Types ON Breweries.brewery_type_id = Types.id
        JOIN States ON Breweries.state_id = States.id
        GROUP BY States.state, Types.type
    """)

    data = cur.fetchall()
    avg_brewery_type_by_state = {}

    for row in data:
        state, brewery_type, num_breweries = row
        if state not in avg_brewery_type_by_state:
            avg_brewery_type_by_state[state] = {brewery_type: num_breweries}
        else:
            avg_brewery_type_by_state[state][brewery_type] = num_breweries

    for state in avg_brewery_type_by_state:
        total_breweries = sum(avg_brewery_type_by_state[state].values())
        for brewery_type in avg_brewery_type_by_state[state]:
            avg_brewery_type_by_state[state][brewery_type] /= total_breweries

    return avg_brewery_type_by_state
#i <3 u

def plot_avg_brewery_type_by_state(avg_brewery_type_by_state):
    states = avg_brewery_type_by_state.keys()
    avg_set = set()
    for state in states:
        avg_set.update(avg_brewery_type_by_state[state].keys())
    type_names = list(avg_set)

    fig, ax = plt.subplots()
    bar_width = 0.8 / len(states)

    for i, state in enumerate(states):
        freqs = [avg_brewery_type_by_state[state].get(type, 0) for type in type_names]
        x = [j + i * bar_width for j in range(len(type_names))]
        ax.bar(x, freqs, bar_width, label=state)

    ax.set_xticks([j + bar_width for j in range(len(type_names))])
    ax.set_xticklabels(type_names, rotation=45)
    ax.legend()
    ax.set_xlabel('State')
    ax.set_ylabel('Average Type')
    ax.set_title('Average Brewery Type by State')

    fig.subplots_adjust(bottom=0.3)

    plt.show()

