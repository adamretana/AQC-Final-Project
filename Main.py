import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random

import matplotlib.animation as animation
from QuasiParticle import QausiParticle1D as QP

def Check_Trapped_Square(Lx, Ly, pos): 
    if Lx[0] <= pos[0] <= Lx[1] and Ly[0] <= pos[1] <= Ly[1]: return True
    else: return False 

def main():
    t0 = 0
    tf = 1000
    active_qps = []
    relaxed_qps = []
    relaxation_pts_x = []
    relaxation_pts_y = []
    Lx = [2, 10] # Dimensions of superconductiong surface
    Ly = [2, 8]
    num_escaped = 0
    num_captured = 0

    #active_qps.append(QP(random.randint(2,10), 2, random.uniform(-.2,.2), random.uniform(.05,.2), 0.1))
    for t in range(t0, tf):

        if t % 10 == 0: active_qps.append(QP(random.uniform(2,10), 2, random.uniform(-.2,.2), random.uniform(.05,.2), random.random()))

        qp_to_delete = []
        for i, qp in zip(range(0, len(active_qps)), active_qps):
            qp.Update_Pos(Lx[0], Lx[1], Ly[0], Ly[1])
            if not Lx[0]+.01 <= qp.x <= Lx[1]-.01:
                qp.dx = -qp.dx
                if qp.Check_If_Relaxed(): 
                    relaxed_qps.append(qp)
                    relaxation_pts_x.append(qp.x)
                    relaxation_pts_y.append(qp.y)
                    qp_to_delete.append(i)
                    num_escaped += 1
            elif not Ly[0]+.01 <= qp.y <= Ly[1]-.01:
                qp.dy = -qp.dy
                if qp.Check_If_Relaxed(): 
                    relaxed_qps.append(qp)
                    relaxation_pts_x.append(qp.x)
                    relaxation_pts_y.append(qp.y)
                    qp_to_delete.append(i)
                    num_escaped += 1
            elif Check_Trapped_Square([4,6], [4,6], [qp.x, qp.y]):
                relaxed_qps.append(qp)
                relaxation_pts_x.append(qp.x)
                relaxation_pts_y.append(qp.y)
                qp_to_delete.append(i)
                num_captured += 1

        qp_to_delete.sort(reverse=True)
        for i in qp_to_delete: 
            try: active_qps.pop(i)
            except: print("OF FUCK")
        
        '''qp_to_delete = []
        for i in range(0, len(active_qps)):
            if active_qps[i].relaxed: 
                relaxed_qps.append(active_qps[i])
                active_qps.pop(i)'''

    #print(len(active_qps))
    #print(len(relaxed_qps))
    print('Captured: {}, Escaped: {}'.format(num_captured, num_escaped))

    fig, ax = plt.subplots()


    for qp in relaxed_qps:
        ax.plot(qp.xpath, qp.ypath, color='g')

    ax.scatter(relaxation_pts_x, relaxation_pts_y, marker='x', color='purple')

    ax.set_xlim([0, 10])
    ax.set_ylim([0, 10])
    S = patches.Rectangle((2,2), 8, 6, alpha=.5, color='r')
    S_trap = patches.Rectangle((4,4), 2, 2, alpha=.5, color='b')
    ax.add_patch(S)
    ax.add_patch(S_trap)

    plt.show()

main()