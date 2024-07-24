from utils import Pathing
info = input("Enter values: ")

inputs = [int(item) for item in info.strip() if item != ' ']

columns = inputs.pop(0)
rows = inputs.pop(0)

portal_count = inputs.pop(0)
pairs = []

for i in range(portal_count):
    portal = input("")
    inputs.clear()
    inputs = [int(item) for item in portal.strip() if item != ' ']
    portal_pairs = []

    for j in range(2):
        if len(inputs) >= 2:
            pair = (rows - inputs.pop(1), inputs.pop(0))
            portal_pairs.append(pair)
        else:
            print("Error: Insufficient coordinates for portal pair.")
            break

    pairs.append(portal_pairs)

pathing = Pathing(rows, columns, pairs)

path_count = pathing.find_paths()
print("Paths: ", path_count)