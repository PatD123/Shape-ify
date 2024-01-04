import numpy as np
class Line:
    def __init__(self, p1, p2, color, line_width, name=None):
        self.p1 = p1 
        self.p2 = p2
        self.color = color
        self.line_width = line_width
        self.name = name

        self.type = "Line"

    def move(self, dis_x, dis_y):
        self.p1[0] += dis_x
        self.p1[1] += dis_y
        self.p2[0] += dis_x
        self.p2[1] += dis_y

    def on_segment(self, p):
        half = self.line_width / 2

        # 1) Find ortho proj of p onto NM (P1 - P2). Find the actual point on the line.
        NM = np.array([self.p2[0] - self.p1[0],
              self.p2[1] - self.p1[1]])
        NM_norm = np.linalg.norm(NM)
        NM_unit = NM / NM_norm

        NP = [p[0] - self.p1[0], p[1] - self.p1[1]]
        P_ortho_vec = np.dot(NP, NM_unit) * NM_unit
        P_ortho_pt = P_ortho_vec + self.p1


        # 2) Check whether that point is within the domain of P1 - P2
        if P_ortho_pt[0] < min(self.p1[0], self.p2[0]) or P_ortho_pt[0] > max(self.p1[0], self.p2[0]) or \
           P_ortho_pt[1] < min(self.p1[1], self.p2[1]) or P_ortho_pt[1] > max(self.p1[1], self.p2[1]):
            return False
    
        # 3) Check dist of that found point to p to see if it is within the half of the
        #    line_width.
        P_ll = NP - P_ortho_vec
        P_ll_mag = np.linalg.norm(P_ll)
        if P_ll_mag > half:
            return False
        
        return True