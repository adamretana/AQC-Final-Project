import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Polygon
import matplotlib.animation as animation

import numpy as np
from QuasiParticle import QuasiParticle as QP
from Calculations import *

rng = np.random.default_rng()

# CONSTANTS
dt = 1 # nanoseconds
#print(dt)
t_tot = 1*10**3 * dt 
tickrate = 10**-20
dist_step = .5
E = 4*Delta0
T = 20 * 10**-3

substrate_Lx = 20
substrate_Ly = 4
SC_thin_Lx = 12
SC_thin_Ly = 2
SC_thick1_Lx = 8
SC_thick1_Ly = 8
insulator_thickness = 1
trap_Lx = 4
trap_Ly = 1

#SC_E1 = Delta0
#SC_E2 = .2 * Delta0

x_bins = []
y_bins = []
for i in range(2, 9):
    x_bins.append(i)
    y_bins.append(i)


#QPs = []
#QPs.append(QP([8,4], [[2,2+SC_thin_Lx],[substrate_Ly,substrate_Ly+SC_thin_Ly]], 1, [[9,11],[4.5,5.5]]))

fig, axs = plt.subplots(1, 2, figsize=(8,4), gridspec_kw={'width_ratios': [2, 1]})
def Simulate_QP_Injection(trap_on_or_off, draw_sim):
    QPs = []
    total_qps = 0
    barriered_qps = 0
    errored_qps = 0
    recombined_qps = 0
    trapped_qps = 0

    t = 0.0
    time_since_error = 0
    error_times = []
    amount_errored_per_t = []
    error_time_gaps = []

    if trap_on_or_off: trap_bounds = [[9,9+trap_Lx],[4.5,4.5+trap_Ly]]
    else: 
        trap_bounds = None
        curr_trapped = False

    #if draw_sim: fig, ax = plt.subplots()
    while t < t_tot:

        # Time Steps
        t += dt
        time_since_error += dt
        #if t % 10**2 == 0: print(t)

        if draw_sim:
            axs[0].clear()
            # SET CHART BOUNDS
            axs[0].set_xlim([0, 24])
            axs[0].set_ylim([0, 18])

            # DRAW CIRCUIT
            Substrate = patches.Rectangle((2,0), substrate_Lx, substrate_Ly, alpha=.5, color='purple')
            S_thin = patches.Rectangle((2, substrate_Ly), SC_thin_Lx, SC_thin_Ly, alpha=.5, color='blue')
            S_Thick1 = patches.Rectangle((2, substrate_Ly + SC_thin_Ly), SC_thick1_Lx, SC_thick1_Ly, alpha=.5, color='green')
            Trap = patches.Rectangle((9,4.5), trap_Lx, trap_Ly, color='orange', alpha=.5)
            axs[0].add_patch(Substrate)
            axs[0].text(substrate_Lx/2, substrate_Ly/2-1, "Substrate")
            axs[0].add_patch(S_thin)
            axs[0].text(SC_thin_Lx/2-3, substrate_Ly+SC_thin_Ly/2-.25, "Thin Layer")
            axs[0].add_patch(S_Thick1)
            axs[0].text(SC_thin_Lx/2-3, substrate_Ly+SC_thin_Ly+SC_thick1_Ly/2, "Thick Layer")
            if trap_on_or_off: 
                axs[0].add_patch(Trap)
                axs[0].text(SC_thin_Lx/2+4, substrate_Ly+SC_thin_Ly/2-.25, "Trap")

            insulator_edges = np.array([[SC_thin_Lx+2, substrate_Ly], [SC_thin_Lx+2, substrate_Ly+SC_thin_Ly], [SC_thin_Lx-insulator_thickness+2, substrate_Ly+SC_thin_Ly], [SC_thin_Lx-insulator_thickness+2, substrate_Ly+SC_thin_Ly+insulator_thickness], [SC_thin_Lx+insulator_thickness+2, substrate_Ly+SC_thin_Ly+insulator_thickness], [SC_thin_Lx+insulator_thickness+2, substrate_Ly]])
            Insulator = Polygon(insulator_edges, color='black', alpha=.5)

            thick2_start_x = SC_thin_Lx-insulator_thickness+2
            thick2_start_y = substrate_Ly+SC_thin_Ly+insulator_thickness
            s_thick2 = np.array([[thick2_start_x, thick2_start_y], [thick2_start_x, thick2_start_y+SC_thick1_Ly-insulator_thickness], [thick2_start_x+2, thick2_start_y+SC_thick1_Ly-insulator_thickness], [thick2_start_x+2, thick2_start_y+SC_thick1_Ly-2-insulator_thickness], [thick2_start_x+6, thick2_start_y+SC_thick1_Ly-2-insulator_thickness], [thick2_start_x+6, thick2_start_y+SC_thick1_Ly-insulator_thickness], [thick2_start_x+8+insulator_thickness, thick2_start_y+SC_thick1_Ly-insulator_thickness], [thick2_start_x+8+insulator_thickness, thick2_start_y-SC_thin_Ly-insulator_thickness], [thick2_start_x+2, thick2_start_y-SC_thin_Ly-insulator_thickness], [thick2_start_x+2, thick2_start_y], [thick2_start_x, thick2_start_y]])
            S_Thick2 = Polygon(s_thick2, color='green', alpha=.5)

            axs[0].add_patch(Insulator)
            axs[0].text(SC_thin_Lx+1, substrate_Ly+SC_thin_Ly+1.25, "Insulator")
            axs[0].add_patch(S_Thick2)
            axs[0].text(thick2_start_x+2, substrate_Ly+SC_thin_Ly+SC_thick1_Ly/2, "Thick Layer")
            

        # SIMULATE QPs
        for i in range(np.random.randint(0,2)) : 
            starting_y = np.random.randint(substrate_Ly,SC_thin_Ly+substrate_Ly+SC_thick1_Ly)
            if starting_y > SC_thin_Ly+substrate_Ly: barriered_qps += 1
            else: 
                starting_pos = [np.random.randint(2,2+SC_thin_Lx), starting_y]
                SC_bounds = [[2,2+SC_thin_Lx],[substrate_Ly,substrate_Ly+SC_thin_Ly]]
                if trap_on_or_off: 
                    if trap_bounds[0][0] <= starting_pos[0] <= trap_bounds[0][1] and trap_bounds[1][0] <= starting_pos[1] <= trap_bounds[1][1]:
                        curr_trapped = True
                    else: curr_trapped = False
                QPs.append(QP(starting_pos, SC_bounds, 1, trap_bounds, trapped=curr_trapped, step_size=dist_step))
                total_qps += 1


        QPs_To_Delete = []
        num_trapped = 0
        num_errored = 0
        for i, qp in zip(range(len(QPs)), QPs):
            if draw_sim: axs[0].scatter(qp.pos[0], qp.pos[1], label = '1', color = 'r')
            if qp.trapped: 
                qp.Update_Pos(E, T)
                QPs_To_Delete.append(i)
                num_trapped += 1
                trapped_qps += 1
            elif qp.Check_Recombined(E, T): 
                recombined_qps += 1
                QPs_To_Delete.append(i)
            elif (14-dist_step <= qp.pos[0] <= 14+dist_step) or (13-dist_step <= qp.pos[0] <= 13+dist_step and 6-dist_step <= qp.pos[1] <= 6+dist_step):
                num_errored += 1
                error_times.append(t)
                error_time_gaps.append(time_since_error)
                time_since_error = 0
                QPs_To_Delete.append(i)
            else: qp.Update_Pos(E, T)
        errored_qps += num_errored
        #amount_errored_per_t.append(num_errored)
        amount_errored_per_t.append(errored_qps)
        
        #print(num_trapped)
        QPs_To_Delete.sort(reverse=False)
        for i in QPs_To_Delete: 
            try: QPs.pop(i)
            except: None

        # DRAW LIVE HISTOGRAM
        if draw_sim:
            if trap_on_or_off: 
                labels = ['tot_QPs', 'Errors', 'Trapped']
                counts = [total_qps, errored_qps, trapped_qps]
                bar_colors = ['blue', 'red', 'green']
            else: 
                labels = ['tot_QPs', 'Errors']
                counts = [total_qps, errored_qps]
                bar_colors = ['blue', 'red']

            axs[1].bar(labels, counts, color=bar_colors)
            axs[1].set_ylim([0, 60])

            plt.suptitle('Time: {} ns'.format(t-1.0))
            plt.pause(tickrate)
            if t == dt: input('Ready?')
            plt.cla()

    print("errored: {}, trapped: {}, barriered: {}, Recombined: {}".format(errored_qps, trapped_qps, barriered_qps, recombined_qps))
    #if errored_qps != 0: print("Average error time {} nanoseconds".format(sum(error_time_gaps)/len(error_time_gaps)))
    
    avg_err_time = 0
    if len(error_time_gaps) != 0: avg_err_time = sum(error_time_gaps)/len(error_time_gaps)
    return amount_errored_per_t, errored_qps, avg_err_time


tot_no_trap_errors = 0
tot_with_trap_errors = 0
no_trap_avg_error_times = []
with_trap_avg_error_times = []
tot_no_trap_errors_list = [0 for x in range(t_tot)]
tot_with_trap_errors_list = [0 for x in range(t_tot)]

#no_trap_errors_per_t = Simulate_QP_Injection(False, False)
#with_trap_errors_per_t = Simulate_QP_Injection(True)

for i in range(10):
    no_trap_errors_per_t, no_trap_curr_error_num, no_trap_avg_err_time = Simulate_QP_Injection(False, False)
    with_trap_errors_per_t, with_trap_curr_error_num, with_trap_avg_err_time = Simulate_QP_Injection(True, False)

    tot_no_trap_errors += no_trap_curr_error_num
    tot_with_trap_errors += with_trap_curr_error_num
    no_trap_avg_error_times.append(no_trap_avg_err_time)
    with_trap_avg_error_times.append(with_trap_avg_err_time)
    tot_no_trap_errors_list = list(map(lambda x, y: x + y, tot_no_trap_errors_list, no_trap_errors_per_t))
    tot_with_trap_errors_list = list(map(lambda x, y: x + y, tot_with_trap_errors_list, with_trap_errors_per_t))

no_trap_avg_err_time = sum(no_trap_avg_error_times)/len(no_trap_avg_error_times)
with_trap_avg_err_time = sum(with_trap_avg_error_times)/len(with_trap_avg_error_times)

print("No Trap - Total errors: {}, Average error time: {} nanoseconds\nWith Trap - Total errors: {}, Average error time: {} nanoseconds".format(tot_no_trap_errors, no_trap_avg_err_time, tot_with_trap_errors, with_trap_avg_err_time))

time_list = [t for t in range(t_tot)]

fig, ax = plt.subplots()

ax.plot(time_list, no_trap_errors_per_t, alpha=.5, label="No Trap", color='red')
ax.plot(time_list, with_trap_errors_per_t, alpha=.5, label="With Trap", color='green')

ax.set_xlabel("Time (ns)")
ax.set_ylabel("Number of Tunneled QuasiParticles")

ax.legend()

plt.show()