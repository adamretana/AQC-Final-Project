import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
from matplotlib.patches import Polygon

import numpy as np

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

def Q_Chip():
    fig, ax = plt.subplots()

    ax.clear()

    # SET CHART BOUNDS
    ax.set_xlim([0, 24])
    ax.set_ylim([0, 16])

    # DRAW CIRCUIT
    Substrate = patches.Rectangle((2,0), substrate_Lx, substrate_Ly, alpha=.5, color='purple')
    S_thin = patches.Rectangle((2, substrate_Ly), SC_thin_Lx, SC_thin_Ly, alpha=.5, color='blue')
    S_Thick1 = patches.Rectangle((2, substrate_Ly + SC_thin_Ly), SC_thick1_Lx, SC_thick1_Ly, alpha=.5, color='green')
    Trap = patches.Rectangle((9,4.5), trap_Lx, trap_Ly, color='orange', alpha=.5)
    ax.add_patch(Substrate)
    ax.add_patch(S_thin)
    ax.add_patch(S_Thick1)
    ax.add_patch(Trap)

    #insulator_edges = np.array([[SC_thin_Lx+2, substrate_Ly], [SC_thin_Lx+2, substrate_Ly+SC_thin_Ly], [SC_thin_Lx-insulator_thickness+2, substrate_Ly+SC_thin_Ly], [SC_thin_Lx-insulator_thickness+2, substrate_Ly+SC_thin_Ly+insulator_thickness], [SC_thin_Lx+insulator_thickness+2, substrate_Ly+SC_thin_Ly+insulator_thickness], [SC_thin_Lx+insulator_thickness+2, substrate_Ly]])
    #Insulator = Polygon(insulator_edges, color='black', alpha=.5)

    thick2_start_x = SC_thin_Lx
    thick2_start_y = substrate_Ly+SC_thin_Ly
    s_thick2 = np.array([[thick2_start_x, thick2_start_y], [thick2_start_x, thick2_start_y+SC_thick1_Ly], [thick2_start_x+2, thick2_start_y+SC_thick1_Ly], [thick2_start_x+2, thick2_start_y+SC_thick1_Ly-2], [thick2_start_x+6, thick2_start_y+SC_thick1_Ly-2], [thick2_start_x+6, thick2_start_y+SC_thick1_Ly], [thick2_start_x+10, thick2_start_y+SC_thick1_Ly], [thick2_start_x+10, thick2_start_y-SC_thin_Ly], [thick2_start_x+2, thick2_start_y-SC_thin_Ly], [thick2_start_x+2, thick2_start_y], [thick2_start_x, thick2_start_y]])
    S_Thick2 = Polygon(s_thick2, color='green', alpha=.5)

    #ax.add_patch(Insulator)
    ax.add_patch(S_Thick2)

    JJ1 = lines.Line2D([SC_thin_Lx+2,SC_thin_Lx+2],[substrate_Ly,substrate_Ly+SC_thin_Ly],2, color="black")
    JJ2 = lines.Line2D([SC_thin_Lx+2,SC_thin_Lx],[substrate_Ly+SC_thin_Ly,substrate_Ly+SC_thin_Ly],2, color="black")
    ax.add_line(JJ1)
    ax.add_line(JJ2)

    # Draw Text
    ax.text(4,10,"Thick Layer", color='green')
    ax.text(15,10,"Thick Layer", color='green')
    ax.text(3,4.7,"Thin Layer", color='blue')
    ax.text(10,4.7,"Trap", color='yellow')
    ax.text(4,1,"Substrate", color='Purple')
    ax.text(14.25,5.5,"$JJ$", color='black')

    #Draw Axis Labels
    ax.set_xlabel("x Length (mm)")
    ax.set_ylabel("y Length (mm)")

    plt.show()

Q_Chip()

def QP_Barrier_Trap():
    fig, ax = plt.subplots()

    ax.set_xlim([0, 10])
    ax.set_ylim([0, 10])

    # Draw Energy Levels
    E0 = lines.Line2D([1,3],[2,2],3, color="green")
    El = lines.Line2D([3,5],[6,6],3, color="green")
    E_barrier = lines.Line2D([6,8],[8,8],3, color="red")
    E_trap = lines.Line2D([6,8],[4,4],3, color="red")
    ax.add_line(E0)
    ax.add_line(El)
    ax.add_line(E_barrier)
    ax.add_line(E_trap)

    # Draw Arrows
    arrow1_x = [2,4]
    arrow2_x = [4,7]
    ax.annotate("", xytext=(arrow1_x[0], 2), xy=(arrow1_x[1], 6),
            arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xytext=(arrow1_x[1]-.2, 6), xy=(arrow1_x[0]-.2, 2),
            arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xytext=(arrow2_x[0], 6+.2), xy=(arrow2_x[1], 8-.2),
            arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xytext=(arrow2_x[1]+.4, 8-.2), xy=(arrow2_x[0]+.4, 6+.2),
            arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xytext=(arrow2_x[0], 6-.2), xy=(arrow2_x[1], 4+.2),
            arrowprops=dict(arrowstyle="->"))
    ax.annotate("", xytext=(arrow2_x[1]+.4, 4+.2), xy=(arrow2_x[0]+.4, 6-.2),
            arrowprops=dict(arrowstyle="->"))
    
    # Draw Text
    ax.text(.25,1.9,"$E_0$", color='green', fontsize=20)
    ax.text(2.25,5.9,"$E_k$", color='green', fontsize=20)
    ax.text(4,7.9,"$E_{barrier}$", color='red', fontsize=20)
    ax.text(4.5,3.9,"$E_{trap}$", color='red', fontsize=20)
    ax.text(2,4, "$\Delta_k$", fontsize=14)
    ax.text(6,6.5, "$\Delta_{k \\rightleftarrows barrier}$", fontsize=14)
    ax.text(6,5.2, "$\Delta_{k \\rightleftarrows trap}$", fontsize=14)

    # Draw Axis Labels
    ax.axis('off')

    plt.show()

#QP_Barrier_Trap()
