# Import the GUI Module.
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Import Matrix generator module
import numpy

FRAME_WIDTH = 500


class Map:
    def __init__(self, size, probability):
        """Initialize a new map object.
        Args:
            size (int): size of map 10 - 1000
            probability (double): 0.0 - 1.0 (0: all empty cells, 1: all walls)
        Returns:
            map object (n*n matrix) with n*n*p empty cells and n*n*(1-p) filled cells
        """
        self.size = size
        self.probability = probability

        # Check if arguments are valid
        if probability > 1 or probability < 0:
            raise ValueError("probability is in range 0 and 1")

        # Generate a uniform distribution matrix (values range from 0.0 to 1.0)
        self.map = numpy.random.uniform(size=[size, size])
        # Generate matrix with n*n*p empty cells
        self.map = (self.map < probability).astype(int)

        # Set start and finish
        self.map[0, 0] = self.map[size - 1, size - 1] = 0

    # Draw map on canvas
    def draw_map(self, canvas):
        # Determine the width of each cell
        width = FRAME_WIDTH/self.size
        for x in range(0, self.size):
            for y in range(0, self.size):
                # Draw first and last cell
                if (x == 0 and y == 0) or (x == (self.size - 1) and y == (self.size - 1)):
                    canvas.draw_polygon([(x*width, y*width), ((x+1)*width, y*width),
                                         ((x+1)*width, (y+1)*width), ((x*width), (y+1)*width)], 1, "Black", "Green")
                # Draw other cells
                else:
                    if self.map[x, y] == 0:
                        canvas.draw_polygon([(x*width, y*width), ((x+1)*width, y*width),
                                             ((x+1)*width, (y+1)*width), ((x*width), (y+1)*width)], 1, "Black", "White")
                    else:
                        canvas.draw_polygon([(x*width, y*width), ((x+1)*width, y*width),
                                             ((x+1)*width, (y+1)*width), ((x*width), (y+1)*width)], 1, "Black", "Red")


def generate_map():
    global current_map
    current_map = Map(int(input_size.get_text()), float(input_probability.get_text()))
    return


def draw_handler(canvas):
    current_map.draw_map(canvas)
    return


def input_handler():
    return

current_map = Map(10, 0.2)

frame = simplegui.create_frame('Assignment 1', FRAME_WIDTH, FRAME_WIDTH)
frame.add_button("Generate Map", generate_map)
frame.set_draw_handler(draw_handler)

#
input_size = frame.add_input('Size', input_handler, 50)
input_size.set_text("10")
input_probability = frame.add_input("Probability", input_handler, 100)
input_probability.set_text("0.2")

frame.start()
