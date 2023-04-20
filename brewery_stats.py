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
    states = [int(state_dict['state_id']) for state_dict in avg_brewery_type_by_state]

    avg_brewery_types = [float(state_dict['avg_brewery_type']) for state_dict in avg_brewery_type_by_state]
    plt.bar(states, avg_brewery_types)
    plt.xlabel('State ID')
    plt.ylabel('Average Number of Breweries per Type')
    plt.title('Average Number of Breweries per Type by State')
    plt.show()
