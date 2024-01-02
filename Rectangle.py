class Rectangle:
    def __init__(self, p1, p2, color, line_width):
        self.top_left = p1 
        self.bot_right = p2
        self.color = color
        self.line_width = line_width

    def move(self, dis_x, dis_y):
        self.top_left[0] += dis_x
        self.top_left[1] += dis_y
        self.bot_right[0] += dis_x
        self.bot_right[1] += dis_y

    def on_segment(self, p):
        #  
        # ABBBBBBBBC
        # A        C
        # A        C
        # ADDDDDDDDC 
        #

        A_x = p[0] >= self.top_left[0] - self.line_width and p[0] <= self.top_left[0] + self.line_width
        A_y = p[1] >= self.top_left[1] - self.line_width and p[1] <= self.top_left[1] + self.line_width

        C_x = p[0] >= self.bot_right[0] - self.line_width and p[0] <= self.bot_right[0] + self.line_width
        C_y = p[1] >= self.bot_right[1] - self.line_width and p[1] <= self.bot_right[1] + self.line_width

        if A_x and A_y:
            return True
        if C_x and C_y:
            return True
        
        return False