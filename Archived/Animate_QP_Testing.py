import matplotlib.pyplot as plt
import matplotlib.patches as patches

import numpy as np
from QuasiParticle import QuasiParticle as QP

rng = np.random.default_rng()

# CONSTANTS
t = 1000
dt = .1
dx = 1
dy = 1
SC_Lx = 8
SC_Ly = 8
SC_E1 = 20
SC_E2 = 2

x_bins = []
y_bins = []
for i in range(2, 9):
    x_bins.append(i)
    y_bins.append(i)


QPs = []
#QPs.append(QP([2,2], [[2,10],[2,10]], 1, [[4,8],[4,8]]))


fig, ax = plt.subplots()
def main():
    for k in range(t):
        ax.clear()

        if k % 2 == 0 : 
            starting_pos = [np.random.randint(2,10), np.random.randint(2,10)]
            SC_bounds = [[2,10],[2,10]]
            trap_bounds = [[4,8],[4,8]]
            if trap_bounds[0][0] <= starting_pos[0] <= trap_bounds[0][1] and trap_bounds[1][0] <= starting_pos[1] <= trap_bounds[1][1]:
                curr_trapped = True
            else: curr_trapped = False
            QPs.append(QP(starting_pos, SC_bounds, 1, trap_bounds, trapped=curr_trapped, step_size=.1))

        S1 = patches.Rectangle((2,2), SC_Lx, SC_Ly, alpha=.5, color='brown')
        Insulator = patches.Rectangle((10,2), 2, SC_Ly, alpha=.5, color='black')
        S2 = patches.Rectangle((12,2), SC_Lx, SC_Ly, alpha=.5, color='g')
        S_trap = patches.Rectangle((4,4), 4, 4, alpha=.5, color='b')
        Substrate = patches.Rectangle((2,0), 18, 2, alpha=.5, color='b')
        ax.add_patch(S1)
        ax.add_patch(S2)
        ax.add_patch(Insulator)
        ax.add_patch(S_trap)
        ax.add_patch(Substrate)

        QPs_To_Delete = []
        num_trapped = 0
        for i, qp in zip(range(len(QPs)), QPs):
            ax.scatter(qp.pos[0], qp.pos[1], label = '1', color = 'r')
            if qp.trapped: 
                qp.Update_Pos(SC_E2, SC_E1)
                num_trapped += 1
            else: qp.Update_Pos(SC_E1, SC_E2)
            if qp.Check_Recombined(): QPs_To_Delete.append(i)
        
        QPs_To_Delete.sort(reverse=True)
        for i in QPs_To_Delete: 
            try: QPs.pop(i)
            except: print("OF FUCK")


        plt.pause(dt)

    plt.show()

main()
