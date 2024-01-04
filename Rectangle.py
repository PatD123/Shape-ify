class Rectangle:
    def __init__(self, p1, p2, color, line_width, name=None):
        self.top_left = p1 
        self.bot_right = p2
        self.color = color
        self.line_width = line_width
        self.name = name

        self.type = "Rectangle"

    def move(self, dis_x, dis_y):
        self.top_left[0] += dis_x
        self.top_left[1] += dis_y
        self.bot_right[0] += dis_x
        self.bot_right[1] += dis_y

    def in_rectangle(self, p):
        half = self.line_width / 2
        if p[0] >= self.top_left[0] - half and p[0] <= self.bot_right[0] + half \
           and p[1] >= self.top_left[1] - half and p[1] <= self.bot_right[1] + half:
            return True
        return False

    def on_segment(self, p):
        #  
        # ABBBBBBBBC
        # A        C
        # A        C
        # ADDDDDDDDC 
        #
        half = self.line_width / 2
        A_x = p[0] >= self.top_left[0] - half and p[0] <= self.top_left[0] + half
        A_y = p[1] >= self.top_left[1] - half and p[1] <= self.top_left[1] + half

        C_x = p[0] >= self.bot_right[0] - half and p[0] <= self.bot_right[0] + half
        C_y = p[1] >= self.bot_right[1] - half and p[1] <= self.bot_right[1] + half

        if A_x and A_y:
            return True
        if C_x and C_y:
            return True
        
        return False