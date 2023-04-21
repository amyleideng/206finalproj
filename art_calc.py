import sqlite3
import matplotlib.pyplot as plt

# def origin_and_dept(cur):
#     cur.execute(
#         """
#         SELECT Artworks.title, Origin.origin, Dept.dept
#         FROM Artworks
#         JOIN Origin ON Artworks.origin_id = Origin.id
#         JOIN Dept ON Artworks.dept_id = Dept.id
#         """
#     )
#     tuples_list = cur.fetchall()

#     france_dept_dict = {}
#     dept_percents = {}

#     for _, country, dept in tuples_list:
#         if country == 'France':
#             france_dept_dict[dept] = france_dept_dict.get(dept, 0) + 1
#     total_france_pieces = sum(france_dept_dict.values())

#     for dept, count in france_dept_dict.items():
#         percent = count/total_france_pieces*100
#         dept_percents[dept] = percent
    
#     print(dept_percents) 
#     return dept_percents

# def bar_graph(cur, conn):
#     dept_percents = origin_and_dept(cur)

#     departments = list(dept_percents.keys())
#     percentages = list(dept_percents.values())

#     plt.bar(departments, percentages)
#     plt.xlabel('Departments')
#     plt.ylabel('Percentages')
#     plt.title('Percentage of Pieces from France by Department')

#     plt.show()

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
        dct[country] = {dept: (count/total)*100 for dept, count in dept_counts.items()}

    print(dct)
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