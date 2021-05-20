import math

def degree(x):
    pi = math.pi
    degree = ((x * 180) / pi) % 360
    return int(degree)

# diff_x = current_x - previous_x
# diff_y = current_y - previous_y

diff_x = 318 - 349
diff_y = 150 - 174

result = degree(math.atan2(diff_y, diff_x))
print(result)
