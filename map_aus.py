import cv2

neighbours = {
    "WA":  ["NT", "SA"],
    "NT":  ["WA", "SA", "QLD"],
    "SA":  ["WA", "NT", "QLD", "NSW", "VIC"],
    "QLD": ["NT", "SA", "NSW"],
    "NSW": ["QLD", "SA", "VIC"],
    "VIC": ["SA", "NSW"],
    "TAS": [] 
}

domains = {state: ["Red", "Green", "Blue"] for state in neighbours}
colors = {}

def select_unassigned_variable(colors, domains):
    for var in domains:
        if var not in colors:
            return var

def is_consistent(var, value, colors, neighbours):
    for neighbour in neighbours[var]:
        if neighbour in colors and colors[neighbour] == value:
            return False
    return True

def forward_checking(colors, domains, neighbours):
    if len(colors) == len(domains):
        return colors

    var = select_unassigned_variable(colors, domains)

    for value in domains[var]:
        if is_consistent(var, value, colors, neighbours):
            colors[var] = value

            saved_domains = {v: domains[v][:] for v in domains}

            failure = False
            for neighbour in neighbours[var]:
                if neighbour not in colors:
                    domains[neighbour] = [
                        v for v in domains[neighbour] if v != value
                    ]
                    if not domains[neighbour]:
                        failure = True
                        break

            if not failure:
                result = forward_checking(colors, domains, neighbours)
                if result:
                    return result

            for v in domains:
                domains[v] = saved_domains[v][:]

            del colors[var]

    return None

result = forward_checking(colors, domains, neighbours)
print(result)

state_points = {
    "WA":  (452, 818),
    "NT":  (1021, 517),
    "SA":  (1114, 1009),
    "QLD": (1571, 723),
    "NSW": (1561, 1200),
    "VIC": (1498, 1479),
    "TAS": (1557, 1746)
}

color_map = {
    "Red":   (255, 0, 0),
    "Green": (0, 255, 0),
    "Blue":  (0, 0, 255)
}

image = cv2.imread("australia.png")

if image is None:
    raise Exception("Image not found")

for state, point in state_points.items():
    color_name = result[state]
    fill_color = color_map[color_name]

    cv2.floodFill(
         image,
         mask=None,
         seedPoint=point,
         newVal=fill_color,
         loDiff=(10, 10, 10),
         upDiff=(10, 10, 10)
     )

image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
cv2.imwrite("colored_map.png", image)