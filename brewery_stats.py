import sqlite3

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