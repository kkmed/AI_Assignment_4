import cv2
import numpy as np

neighbours = {
    'Adilabad': ['Kumuram Bheem', 'Nirmal'],
    'Kumuram Bheem': ['Adilabad', 'Mancherial', 'Nirmal'],
    'Nirmal': ['Adilabad', 'Jagtial', 'Kumuram Bheem', 'Mancherial', 'Nizamabad'],
    'Mancherial': ['Jagtial', 'Jayashankar Bhupalpally', 'Kumuram Bheem', 'Nirmal', 'Peddapalli'],
    'Nizamabad': ['Jagtial', 'Kamareddy', 'Nirmal', 'Rajanna Sircilla'],
    'Jagtial': ['Karimnagar', 'Mancherial', 'Nirmal', 'Nizamabad', 'Peddapalli', 'Rajanna Sircilla'],
    'Peddapalli': ['Jagtial', 'Jayashankar Bhupalpally', 'Karimnagar', 'Mancherial'],
    'Karimnagar': ['Jagtial', 'Jayashankar Bhupalpally', 'Peddapalli', 'Rajanna Sircilla', 'Siddipet', 'Warangal Rural', 'Warangal Urban'],
    'Rajanna Sircilla': ['Jagtial', 'Kamareddy', 'Karimnagar', 'Nizamabad', 'Siddipet'],
    'Kamareddy': ['Medak', 'Nizamabad', 'Rajanna Sircilla', 'Sangareddy', 'Siddipet'],
    'Medak': ['Kamareddy', 'Medchal Malkajgiri', 'Sangareddy', 'Siddipet'],
    'Sangareddy': ['Hyderabad', 'Kamareddy', 'Medak', 'Medchal Malkajgiri', 'Rangareddy', 'Vikarabad'],
    'Siddipet': ['Jangaon', 'Kamareddy', 'Karimnagar', 'Medak', 'Medchal Malkajgiri', 'Rajanna Sircilla', 'Warangal Urban', 'Yadadri Bhuvanagiri'],
    'Jayashankar Bhupalpally': ['Karimnagar', 'Mancherial', 'Mulugu', 'Peddapalli', 'Warangal Rural', 'Warangal Urban'],
    'Mulugu': ['Bhadradri Kothagudem', 'Jayashankar Bhupalpally', 'Mahabubabad', 'Warangal Rural'],
    'Warangal Urban': ['Jangaon', 'Jayashankar Bhupalpally', 'Karimnagar', 'Siddipet', 'Warangal Rural'],
    'Warangal Rural': ['Jangaon', 'Jayashankar Bhupalpally', 'Karimnagar', 'Mahabubabad', 'Mulugu', 'Warangal Urban'],
    'Jangaon': ['Mahabubabad', 'Siddipet', 'Suryapet', 'Warangal Rural', 'Warangal Urban', 'Yadadri Bhuvanagiri'],
    'Mahabubabad': ['Bhadradri Kothagudem', 'Jangaon', 'Khammam', 'Mulugu', 'Suryapet', 'Warangal Rural'],
    'Bhadradri Kothagudem': ['Khammam', 'Mahabubabad', 'Mulugu'],
    'Khammam': ['Bhadradri Kothagudem', 'Mahabubabad', 'Nalgonda', 'Suryapet'],
    'Suryapet': ['Jangaon', 'Khammam', 'Mahabubabad', 'Nalgonda', 'Yadadri Bhuvanagiri'],
    'Yadadri Bhuvanagiri': ['Jangaon', 'Medchal Malkajgiri', 'Nalgonda', 'Rangareddy', 'Siddipet', 'Suryapet'],
    'Medchal Malkajgiri': ['Hyderabad', 'Medak', 'Rangareddy', 'Sangareddy', 'Siddipet', 'Yadadri Bhuvanagiri'],
    'Hyderabad': ['Medchal Malkajgiri', 'Rangareddy', 'Sangareddy'],
    'Rangareddy': ['Hyderabad', 'Mahabubnagar', 'Medchal Malkajgiri', 'Nagarkurnool', 'Nalgonda', 'Sangareddy', 'Vikarabad', 'Yadadri Bhuvanagiri'],
    'Vikarabad': ['Mahabubnagar', 'Narayanpet', 'Rangareddy', 'Sangareddy'],
    'Mahabubnagar': ['Nagarkurnool', 'Narayanpet', 'Rangareddy', 'Vikarabad', 'Wanaparthy'],
    'Narayanpet': ['Jogulamba Gadwal', 'Mahabubnagar', 'Vikarabad', 'Wanaparthy'],
    'Jogulamba Gadwal': ['Nagarkurnool', 'Narayanpet', 'Wanaparthy'],
    'Wanaparthy': ['Jogulamba Gadwal', 'Mahabubnagar', 'Nagarkurnool', 'Narayanpet'],
    'Nagarkurnool': ['Jogulamba Gadwal', 'Mahabubnagar', 'Nalgonda', 'Rangareddy', 'Wanaparthy'],
    'Nalgonda': ['Khammam', 'Nagarkurnool', 'Rangareddy', 'Suryapet', 'Yadadri Bhuvanagiri']
}

domains = {state: ["Red","Green","Blue","Orange"] for state in neighbours}
colors = {}

def select_unassigned_variable():
    unassigned = [v for v in domains if v not in colors]
    return min(unassigned, key=lambda var: len(domains[var]))

def is_consistent(var, value):
    return all(colors.get(n) != value for n in neighbours[var])

def forward_checking():
    if len(colors) == len(domains):
        return True

    var = select_unassigned_variable()

    for value in domains[var]:
        if is_consistent(var, value):
            colors[var] = value

            removed = {}
            for n in neighbours[var]:
                if n not in colors and value in domains[n]:
                    domains[n].remove(value)
                    removed.setdefault(n, []).append(value)

            if all(domains[n] for n in domains if n not in colors):
                if forward_checking():
                    return True

            for n in removed:
                domains[n].extend(removed[n])

            del colors[var]

    return False

def validate():
    for state in neighbours:
        for n in neighbours[state]:
            if colors[state] == colors[n]:
                print("❌ Conflict:", state, n)
                return False
    print("✅ Valid coloring")
    return True

forward_checking()
print(colors)
validate()

img = cv2.imread("telangana.png")

color_map = {
    "Red": (0,0,255),
    "Green": (0,255,0),
    "Blue": (255,0,0),
    "Orange": (0,165,255)
}

seed_points = {
    "Adilabad": (74, 29),
    "Kumuram Bheem": (117, 36),
    "Nirmal": (65, 50),
    "Mancherial": (119, 57),
    "Nizamabad": (57, 73),
    "Jagtial": (88, 64),
    "Peddapalli": (116, 75),
    "Karimnagar": (109, 91),
    "Rajanna Sircilla": (81, 86),
    "Kamareddy": (45, 94),
    "Medak": (64, 109),
    "Sangareddy": (32, 116),
    "Siddipet": (85, 107),
    "Jayashankar Bhupalpally": (144, 81),
    "Mulugu": (166, 94),
    "Warangal Urban": (120, 104),
    "Warangal Rural": (135, 112),
    "Jangaon": (108, 120),
    "Mahabubabad": (146, 124),
    "Bhadradri Kothagudem": (173, 123),
    "Khammam": (159, 147),
    "Suryapet": (136, 158),
    "Yadadri Bhuvanagiri": (91, 136),
    "Medchal Malkajgiri": (73, 130),
    "Hyderabad": (68, 138),
    "Rangareddy": (62, 153),
    "Vikarabad": (30, 149),
    "Mahabubnagar": (42, 171),
    "Narayanpet": (24, 179),
    "Jogulamba Gadwal": (31, 208),
    "Wanaparthy": (46, 198),
    "Nagarkurnool": (71, 195),
    "Nalgonda": (108, 167)
}

for district, (x,y) in seed_points.items():
    color = color_map[colors[district]]

    cv2.floodFill(
        img,
        None,
        (x,y),
        color,
        loDiff=(5,5,5),
        upDiff=(5,5,5)
    )

cv2.imwrite("colored_telangana.png", img)