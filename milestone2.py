import math
import os


def read_text_file(file_path):
    parameters ={}
    with open(file_path, 'r') as f:
        print(f)
        for line in f:
            key, value = line.strip().split(':')
            parameters[key.strip()] = (value.strip())
    return parameters

def write_points_to_file(file_path, data):
    with open(file_path, 'w') as f:
        for key, value in data.items():
            f.write(f"{key}: {value}\n")

def calcDistance(x,y):
    return math.sqrt((x[0] - y[0])**2 + (x[1]-y[1])**2)

def isPointincircle(point, parameters):
    diameter = int(parameters['WaferDiameter'])
    rad = diameter/2
    if calcDistance((0,0), point) < rad:
        return True
    return False
def checkChord(die_centre,die_size,parameters):
    diameter = int(parameters['WaferDiameter'])
    rad = diameter/2
    die_width = die_size[0]
    die_height = die_size[1]
    die_top_left = (die_centre[0]-(die_width/2), die_centre[1]+(die_height/2))
    die_top_right = (die_centre[0]+(die_width/2), die_centre[1]+(die_height/2))
    die_bottom_left = (die_centre[0]-(die_width/2), die_centre[1]-(die_height/2))
    die_bottom_right = (die_centre[0]+(die_width/2), die_centre[1]-(die_height/2))

    x_values = [point[0] for point in [die_top_left, die_top_right, die_bottom_left, die_bottom_right]]
    y_values = [point[1] for point in [die_top_left, die_top_right, die_bottom_left, die_bottom_right]]
    min_x, max_x = int(min(x_values)), int(max(x_values))
    min_y, max_y = int(min(y_values)), int(max(y_values))

    points_inside = [(x, y) for x in range(min_x, max_x + 1) for y in range(min_y, max_y + 1)]

    for i in points_inside:
        if calcDistance((0,0), i)<rad:
            return True
    return False

def isDieInCircle(die_centre,die_size):
    die_width = die_size[0]
    die_height = die_size[1]
    die_top_left = (die_centre[0]-(die_width/2), die_centre[1]+(die_height/2))
    die_top_right = (die_centre[0]+(die_width/2), die_centre[1]+(die_height/2))
    die_bottom_left = (die_centre[0]-(die_width/2), die_centre[1]-(die_height/2))
    die_bottom_right = (die_centre[0]+(die_width/2), die_centre[1]-(die_height/2))
    if isPointincircle(die_top_left, parameters) or isPointincircle(die_top_right, parameters) or isPointincircle(die_bottom_left, parameters) or isPointincircle(die_bottom_right, parameters) or chord(die_centre,die_size,parameters):
        return True
    return False

def calculate_lower_left_corner(die_centre,die_size):
    die_width = die_size[0]
    die_height = die_size[1]
    return (float(die_centre[0])-(die_width/2), float(die_centre[1])-(die_height/2))


def calcIndices(parameters):
    diameter = int(parameters.get('WaferDiameter', 0))
    die_size_str = parameters['DieSize']
    die_size = tuple(map(int, die_size_str.split('x')))
    shiftVector = [int(x) for x in parameters['DieShiftVector'].lstrip('(').rstrip(')').split(',')]
    reference_die = tuple(map(int, parameters['ReferenceDie'].lstrip('(').rstrip(')').split(',')))
    radius = diameter/2
    hyp = math.sqrt(die_size[0]**2 + die_size[1]**2)
    res = {}
    res[(0,0)] = calculate_lower_left_corner(reference_die,die_size)

    die_width = die_size[0]
    die_height = die_size[1]
    #quadrant 1
    row=col=0
    while True:
        col = 0
        while True:
            #reference point condition
            if row == 0 and col==0:
                col += 1
                continue

            curr_die = [reference_die[0] + row*die_width, reference_die[1] + col*die_height]
            if isDieInCircle(curr_die,die_size):
                res[(row,col)] = calculate_lower_left_corner(curr_die,die_size)
                col += 1
            else:
                break
        row += 1
        col = 0
        curr_die = [reference_die[0] + row*die_width, reference_die[1] + col*die_height]
        if not isDieInCircle(curr_die,die_size):
            break

    #quadrant 2
    row=col=0
    while True:
        col = 0
        while True:
            #reference point condition
            if row == 0 and col==0:
                col += 1
                continue

            curr_die = [reference_die[0] + row*die_width, reference_die[1] + col*die_height]
            if isDieInCircle(curr_die,die_size):
                res[(row,col)] = calculate_lower_left_corner(curr_die,die_size)
                col += 1
            else:
                break
        row -= 1
        col = 0
        curr_die = [reference_die[0] + row*die_width, reference_die[1] + col*die_height]
        if not isDieInCircle(curr_die,die_size):
            break
    
    #quadrant 3
    row=col=0
    while True:
        col = 0
        while True:
            #reference point condition
            if row == 0 and col==0:
                col -= 1
                continue

            curr_die = [reference_die[0] + row*die_width, reference_die[1] + col*die_height]
            if isDieInCircle(curr_die,die_size):
                res[(row,col)] = calculate_lower_left_corner(curr_die,die_size)
                col -= 1
            else:
                break
        row -= 1
        col = 0
        curr_die = [reference_die[0] + row*die_width, reference_die[1] + col*die_height]
        if not isDieInCircle(curr_die,die_size):
            break
    
    #quadrant 4
    row=col=0
    while True:
        col = 0
        while True:
            #reference point condition
            if row == 0 and col==0:
                col -= 1
                continue

            curr_die = [reference_die[0] + row*die_width, reference_die[1] + col*die_height]
            if isDieInCircle(curr_die,die_size):
                res[(row,col)] = calculate_lower_left_corner(curr_die,die_size)
                col -= 1
            else:
                break
        row += 1
        col = 0
        curr_die = [reference_die[0] + row*die_width, reference_die[1] + col*die_height]
        if not isDieInCircle(curr_die,die_size):
            break
    return res

path = "C:/Users/Krithika/Desktop/PSG/KLA-Hackathon-2024/input/Milestone2/Input"
os.chdir(path)
i=1
for file in os.listdir():
    if file.endswith(".txt"):
        file_path = os.path.join(path, file)
        parameters = read_text_file(file_path)
        diameter = int(parameters.get('WaferDiameter', 0))

        radius = diameter/2
        answer = calcIndices(parameters)
        print(answer)
        file_path = f'SampleOutputFormat{i}.txt'  # change the naming convention if needed
        write_points_to_file(file_path, answer)
        i+=1




