import math

def degree(x):
    pi = math.pi
    degree = ((x * 180) / pi) % 360
    return int(degree)

x1 = 3
y1 = 3

x2= 5
y2 =4

diff_y = y2-y1
diff_x = x2-x1

#(0, 17) (49, 81) 52

result1 = math.atan2(81-17, 49)
result2 = math.atan2(5, -5)
result3 = math.atan2(-5, -5)
result4 = math.atan2(-5, 5)

print(degree(result1))
