import sqlite3

def get_avg_brewery_type_by_state(cur):
    """
    Returns a dictionary with the average brewery type for each state.

    :param cur: a cursor object for the database
    :return: a dictionary with the average brewery type for each state
    """
    cur.execute("""
        SELECT state, AVG(CASE brewery_type 
                            WHEN 'micro' THEN 1
                            WHEN 'nano' THEN 2
                            WHEN 'regional' THEN 3
                            WHEN 'brewpub' THEN 4
                            WHEN 'large' THEN 5
                            WHEN 'planning' THEN 6
                            WHEN 'contract' THEN 7
                            ELSE 8
                        END) AS avg_type
        FROM breweries
        GROUP BY state
        """)
    result = {}
    for row in cur.fetchall():
        result[row[0]] = int(row[1])
    return result