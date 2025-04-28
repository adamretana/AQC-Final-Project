import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np

import matplotlib.animation as animation
from Phonon import Phonon as Phonon


rng = np.random.default_rng()

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

    #active_qps.append(Phonon(random.randint(2,10), 2, random.uniform(-.2,.2), random.uniform(.05,.2), 0.1))
    for t in range(t0, tf):

        if t % 10 == 0: active_qps.append(Phonon(rng.integers(2,10), 2, rng.uniform(-.2,.2), rng.uniform(.05,.2), rng.random()))

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

    print('Captured: {}, Escaped: {}'.format(num_captured, num_escaped))

    fig, ax = plt.subplots()

    for qp in relaxed_qps:
        ax.plot(qp.xpath, qp.ypath, color='g')

    ax.scatter(relaxation_pts_x, relaxation_pts_y, marker='x', color='purple')

    ax.set_xlim([0, 10])
    ax.set_ylim([0, 20])

    # Drawing Simple layers
    Substrate = patches.Rectangle((0+2,0), 6, 6, alpha=.5, color='black')
    S_thin_1 = patches.Rectangle((0+2,6), 4, 2, alpha=.5, color='b')
    S_thin_2 = patches.Rectangle((5+2,6), 1, 2, alpha=.5, color='b')
    S_thick_1 = patches.Rectangle((0+2,8), 2, 6, alpha=.5, color='purple')
    ax.add_patch(Substrate)
    ax.add_patch(S_thin_1)
    ax.add_patch(S_thin_2)
    ax.add_patch(S_thick_1)

    # Drawing complex right thick layer
    pathdata = [ 
        (Path.MOVETO, (5, 8)),
        (Path.LINETO, (5, 14)),
        (Path.LINETO, (6, 14)),
        (Path.LINETO, (6, 12)),
        (Path.LINETO, (7, 12)),
        (Path.LINETO, (7, 14)),
        (Path.LINETO, (8, 14)),
        (Path.LINETO, (8, 8)),
        (Path.LINETO, (7, 8)),
        (Path.LINETO, (7, 6)),
        (Path.LINETO, (6, 6)),
        (Path.LINETO, (6, 8)),
        (Path.CLOSEPOLY, (1.58, -2.57)),
    ]
    codes, verts = zip(*pathdata)
    path = Path(verts, codes)
    patch = patches.PathPatch(
        path, color='purple', alpha=0.5)
    ax.add_patch(patch)

    # Drawing Insulating Layer
    #ax.add_line()


    plt.show()

main()