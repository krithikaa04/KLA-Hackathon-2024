import math
import os


def equallySpacedPoints(parameters):
        circles = []
        diameter = parameters['WaferDiameter']
        no_points = parameters['NumberOfPoints']
        angle = parameters['Angle']
        center = (0,0)
        radius = diameter / 2
        angle_radians = math.radians(angle)
        #x , y in one direction
        x = center[0] + radius * math.cos(angle_radians)
        y = center[1] + radius * math.sin(angle_radians)
        symmetric_angle_radians = math.radians(180 + angle)
        #x,y in the opposite direction
        symmetric_x = center[0] + radius * math.cos(symmetric_angle_radians)
        symmetric_y = center[1] + radius * math.sin(symmetric_angle_radians)
        points = []
        for i in range(no_points):
            temp = i / (no_points - 1) 
            x_ = (1 - temp) * (x) + temp * symmetric_x
            y_ = (1 - temp) * (y) + temp * symmetric_y
            points.append((x_, y_))
        return points


def read_text_file(file_path):
    parameters ={}
    with open(file_path, 'r') as f:
        print(f)
        for line in f:
            key, value = line.strip().split(':')
            parameters[key.strip()] = int(value.strip())
    return parameters

def write_points_to_file(file_path, points):
    with open(file_path, 'w') as f:
        for point in points:
            f.write(f"({point[0]},{point[1]})\n")

path = "C:/Users/Krithika/Desktop/PSG/KLA-Hackathon-2024/input/Milestone1/Input"
os.chdir(path)
i=1
for file in os.listdir():
    if file.endswith(".txt"):
        file_path = os.path.join(path, file)
        parameters = read_text_file(file_path)
        print(parameters)
        points = equallySpacedPoints(parameters)
        #print(points)
        file_path = f'SampleOutputFormat{i}.txt'  # change the naming convention if needed
        write_points_to_file(file_path, points)
        i+=1
                