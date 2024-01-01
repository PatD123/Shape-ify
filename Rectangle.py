class Rectangle:
    def __init__(self, p1, p2, line_width):
        self.top_left = p1 
        self.bot_right = p2
        self.line_width = line_width
 
    def show(self):
        pass

    def on_segment(self, p):
        #  
        # ABBBBBBBBC
        # A        C
        # A        C
        # ADDDDDDDDC 
        #

        A_x = p[0] >= self.top_left[0] - self.line_width and p[0] <= self.top_left[0] + self.line_width
        A_y = p[1] >= self.top_left[1] and p[1] <= self.bot_right[1]

        B_x = p[0] >= self.top_left[0] and p[0] <= self.bot_right[0]
        B_y = p[1] >= self.top_left[1] - self.line_width and p[1] <= self.top_left[1] + self.line_width

        C_x = p[0] >= self.bot_right[0] - self.line_width and p[0] <= self.bot_right[0] + self.line_width
        C_y = p[1] >= self.top_left[1] and p[1] <= self.bot_right[1]

        D_x = p[0] >= self.top_left[0] and p[0] <= self.bot_right[0]
        D_y = p[1] >= self.bot_right[1] - self.line_width and p[1] <= self.bot_right[1] + self.line_width