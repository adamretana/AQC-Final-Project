import random
import time
random.seed(5)

class QausiParticle1D:

    relaxed = False

    def __init__(self, x, y, dx, dy, Relaxation_Rate):
        self.x = x
        self.y = y
        self.xpath = [x]
        self.ypath = [y]
        self.dx = dx
        self.dy = dy
        self.Relaxation_Rate = Relaxation_Rate

    def Update_Pos(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.xpath.append(self.x)
        self.ypath.append(self.y)

    def Check_If_Relaxed(self):
        return False #random.random() > (1 - self.Relaxation_Rate)
    
#Testing QuasiParticle1D
'''
def main():
    t0 = 0
    tf = 100
    active_qps = []

    for t in range(t0, tf):
        surface = list("_"*10)

        if random.random() > .5: active_qps.append(QausiParticle1D(x=random.randint(0,9), dx=random.choice([-1,1]), Relaxation_Rate=random.random(), y=0, dy=0))

        for qp in active_qps:
            if qp.relaxed: continue
            surface[qp.x] = '+'
            qp.Update_Pos()
            if qp.Check_If_Relaxed(): qp.relaxed = True
            elif not 0 <= qp.x <= 9: qp.relaxed = True
        surface_str = "".join(surface)
        print("{0:4}: {1}".format(t, surface_str))
        time.sleep(.1)

main()
'''