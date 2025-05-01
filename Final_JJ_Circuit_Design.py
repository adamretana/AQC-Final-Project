import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon

import numpy as np
from QuasiParticle import QuasiParticle as QP

rng = np.random.default_rng()

# CONSTANTS
t = 1000
dt = .1
dist_step = .5
substrate_Lx = 20
substrate_Ly = 4
SC_thin_Lx = 12
SC_thin_Ly = 2
SC_thick1_Lx = 8
SC_thick1_Ly = 8
insulator_thickness = 1
trap_Lx = 4
trap_Ly = 1

SC_E1 = 20
SC_E2 = 2

x_bins = []
y_bins = []
for i in range(2, 9):
    x_bins.append(i)
    y_bins.append(i)


QPs = []
#QPs.append(QP([8,4], [[2,2+SC_thin_Lx],[substrate_Ly,substrate_Ly+SC_thin_Ly]], 1, [[9,11],[4.5,5.5]]))

fig, ax = plt.subplots()
def main():
    barriered_qps = 0
    errored_qps = 0
    recombined_qps = 0

    for k in range(t):
        ax.clear()

        # SET CHART BOUNDS
        ax.set_xlim([0, 24])
        ax.set_ylim([0, 18])

        # DRAW CIRCUIT
        Substrate = patches.Rectangle((2,0), substrate_Lx, substrate_Ly, alpha=.5, color='purple')
        S_thin = patches.Rectangle((2, substrate_Ly), SC_thin_Lx, SC_thin_Ly, alpha=.5, color='blue')
        S_Thick1 = patches.Rectangle((2, substrate_Ly + SC_thin_Ly), SC_thick1_Lx, SC_thick1_Ly, alpha=.5, color='green')
        Trap = patches.Rectangle((9,4.5), trap_Lx, trap_Ly, color='orange')
        ax.add_patch(Substrate)
        ax.add_patch(S_thin)
        ax.add_patch(S_Thick1)
        ax.add_patch(Trap)

        insulator_edges = np.array([[SC_thin_Lx+2, substrate_Ly], [SC_thin_Lx+2, substrate_Ly+SC_thin_Ly], [SC_thin_Lx-insulator_thickness+2, substrate_Ly+SC_thin_Ly], [SC_thin_Lx-insulator_thickness+2, substrate_Ly+SC_thin_Ly+insulator_thickness], [SC_thin_Lx+insulator_thickness+2, substrate_Ly+SC_thin_Ly+insulator_thickness], [SC_thin_Lx+insulator_thickness+2, substrate_Ly]])
        Insulator = Polygon(insulator_edges, color='black', alpha=.5)

        thick2_start_x = SC_thin_Lx-insulator_thickness+2
        thick2_start_y = substrate_Ly+SC_thin_Ly+insulator_thickness
        s_thick2 = np.array([[thick2_start_x, thick2_start_y], [thick2_start_x, thick2_start_y+SC_thick1_Ly-insulator_thickness], [thick2_start_x+2, thick2_start_y+SC_thick1_Ly-insulator_thickness], [thick2_start_x+2, thick2_start_y+SC_thick1_Ly-2-insulator_thickness], [thick2_start_x+6, thick2_start_y+SC_thick1_Ly-2-insulator_thickness], [thick2_start_x+6, thick2_start_y+SC_thick1_Ly-insulator_thickness], [thick2_start_x+8+insulator_thickness, thick2_start_y+SC_thick1_Ly-insulator_thickness], [thick2_start_x+8+insulator_thickness, thick2_start_y-SC_thin_Ly-insulator_thickness], [thick2_start_x+2, thick2_start_y-SC_thin_Ly-insulator_thickness], [thick2_start_x+2, thick2_start_y], [thick2_start_x, thick2_start_y]])
        S_Thick2 = Polygon(s_thick2, color='green', alpha=.5)

        ax.add_patch(Insulator)
        ax.add_patch(S_Thick2)

        # SIMULATE QPs
        if k % 2 == 0 : 
            starting_y = np.random.randint(substrate_Ly,SC_thin_Ly+substrate_Ly+SC_thick1_Ly)
            if starting_y > SC_thin_Ly+substrate_Ly: barriered_qps += 1
            else: 
                starting_pos = [np.random.randint(2,2+SC_thin_Lx), starting_y]
                SC_bounds = [[2,2+SC_thin_Lx],[substrate_Ly,substrate_Ly+SC_thin_Ly]]
                trap_bounds = [[9,9+trap_Lx],[4.5,4.5+trap_Ly]]
                if trap_bounds[0][0] <= starting_pos[0] <= trap_bounds[0][1] and trap_bounds[1][0] <= starting_pos[1] <= trap_bounds[1][1]:
                    curr_trapped = True
                else: curr_trapped = False
                QPs.append(QP(starting_pos, SC_bounds, 1, trap_bounds, trapped=curr_trapped, step_size=dist_step))


        QPs_To_Delete = []
        num_trapped = 0
        for i, qp in zip(range(len(QPs)), QPs):
            ax.scatter(qp.pos[0], qp.pos[1], label = '1', color = 'r')
            if qp.trapped: 
                qp.Update_Pos(SC_E2, SC_E1)
                num_trapped += 1
            else: qp.Update_Pos(SC_E1, SC_E2)
            if qp.Check_Recombined(): 
                recombined_qps += 1
                QPs_To_Delete.append(i)
            elif (14-dist_step <= qp.pos[0] <= 14+dist_step) or (13-dist_step <= qp.pos[0] <= 13+dist_step and 6-dist_step <= qp.pos[1] <= 6+dist_step):
                errored_qps += 1
                QPs_To_Delete.append(i)
        
        #print(num_trapped)
        QPs_To_Delete.sort(reverse=True)
        for i in QPs_To_Delete: 
            try: QPs.pop(i)
            except: print("OF FUCK")

        plt.pause(dt)
    plt.show()

    print("errored: {}, barriered: {}, Recombined: {}".format(errored_qps, barriered_qps, recombined_qps))

main()