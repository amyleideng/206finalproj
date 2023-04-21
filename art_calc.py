import sqlite3
import matplotlib.pyplot as plt

def calculate_dept_percent(cur):
    cur.execute(
        """
        SELECT Artworks.title, Origin.origin, Dept.dept
        FROM Artworks
        JOIN Origin ON Artworks.origin_id = Origin.id
        JOIN Dept ON Artworks.dept_id = Dept.id
        """
    )
    data = cur.fetchall()
    counts = {}
    for title, country, department in data:
        if country not in counts:
            counts[country] = {}
        if department not in counts[country]:
            counts[country][department] = 0
        counts[country][department] += 1

    dct = {}
    for country, dept_counts in counts.items():
        total = sum(dept_counts.values())
        dct[country] = {dept: round((count/total)*100, 2) for dept, count in dept_counts.items()}

    # print(dct)
    return dct

def percents_bar_graph(dct):
    countries = dct.keys()
    dept_set = set()
    for country in countries:
        dept_set.update(dct[country].keys())
    dept_names = list(dept_set)

    fig, ax = plt.subplots()
    bar_width = 0.8 / len(countries)

    for i, country in enumerate(countries):
        freqs = [dct[country].get(dept, 0) for dept in dept_names]
        x = [j + i * bar_width for j in range(len(dept_names))]
        ax.bar(x, freqs, bar_width, label=country)

    ax.set_xticks([j + bar_width for j in range(len(dept_names))])
    ax.set_xticklabels(dept_names, rotation=45)
    ax.legend()
    ax.set_xlabel('Department')
    ax.set_ylabel('Percentage')
    ax.set_title('Department Frequencies by Country')

    fig.subplots_adjust(bottom=0.3)

    plt.show()