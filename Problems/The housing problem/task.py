# definition of the class
class RightTriangle:
    def __init__(self, hyp, leg_1, leg_2):
        self.c = hyp
        self.a = leg_1
        self.b = leg_2
        # calculate the area here
        self.area = leg_1 * leg_2 / 2
# triangle from the input
input_c, input_a, input_b = 13, 12, 5

# write your code here
if (input_c^2 == (input_a^2 + input_b^2)):
    rightTriangle = RightTriangle(input_c, input_a, input_b)
    print(rightTriangle.area)
else:
    print("Not right")

