import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random

import matplotlib.animation as animation
from QuasiParticle import QausiParticle1D as QP

def main():
    t0 = 0
    tf = 100
    active_qps = []
    relaxed_qps = []
    relaxation_pts_x = []
    relaxation_pts_y = []

    for t in range(t0, tf):

        if t % 10 == 0: active_qps.append(QP(random.randint(2,10), 2, random.uniform(-.2,.2), random.uniform(.05,.2), random.random()))

        qp_to_delete = []
        for i, qp in zip(range(0, len(active_qps)), active_qps):
            qp.Update_Pos()
            if qp.Check_If_Relaxed(): 
                qp.relaxed = True
                relaxed_qps.append(qp)
                relaxation_pts_x.append(qp.x)
                relaxation_pts_y.append(qp.y)
                qp_to_delete.append(i)
            elif not 2 <= qp.x <= 10 or not 2 <= qp.y <= 8:
                qp.relaxed = True
                relaxed_qps.append(qp)
                relaxation_pts_x.append(qp.x)
                relaxation_pts_y.append(qp.y)
                qp_to_delete.append(i)

        for i in qp_to_delete: active_qps.pop(i)
        
        '''qp_to_delete = []
        for i in range(0, len(active_qps)):
            if active_qps[i].relaxed: 
                relaxed_qps.append(active_qps[i])
                active_qps.pop(i)'''

    print(len(active_qps))
    print(len(relaxed_qps))

    fig, ax = plt.subplots()


    for qp in relaxed_qps:
        ax.plot(qp.xpath, qp.ypath, color='g')

    ax.scatter(relaxation_pts_x, relaxation_pts_y, marker='x', color='purple')

    ax.set_xlim([0, 10])
    ax.set_ylim([0, 10])
    S = patches.Rectangle((2,2), 2, 6, alpha=.5, color='r')
    S_trap = patches.Rectangle((4,2), 6, 6, alpha=.5, color='b')
    ax.add_patch(S)
    ax.add_patch(S_trap)

    plt.show()

main()