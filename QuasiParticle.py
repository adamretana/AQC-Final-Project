import numpy as np
import math

from Calculations import *

rng = np.random.default_rng()

class QuasiParticle:

    boltzmann_constant = math.pow(1.380649, -23) # joules / kelvin
    Tc_aluminum = 1.2 # kelvin

    Annihilated = False
    density_cooper_pairs = math.pow(2.8, 0^6) # 1 / micrometers^3
    band_gap_no_QPs = 1.764 * boltzmann_constant * Tc_aluminum
    #trapped = False
    #step_size = .5

    def __init__(self, position, position_bounds, energy, trap_bounds=None, trapped=False, step_size=.1):
        self.pos = position
        self.bounds = position_bounds
        self.trap = trap_bounds
        self.E = energy
        self.trapped = trapped
        self.step_size = step_size

    def Update_Pos(self, Ei=0, Ej=0):
        move_options_x = []
        move_options_y = []

        scattered = self.Check_Scattered(Ei, Ej)

        if self.trap != None:
            if self.Check_Inside_Trap():
                if self.trapped:
                    if self.trap[0][0]-self.step_size <= self.pos[0] <= self.trap[0][0]+self.step_size: 
                        if scattered: move_options_x = [0, -1]
                        else: move_options_x = [0, 1]
                    if self.trap[0][1]-self.step_size <= self.pos[0] <= self.trap[0][1]+self.step_size: 
                        if scattered: move_options_x = [0, 1]
                        else: move_options_x = [0, -1]
                    if self.trap[1][0]-self.step_size <= self.pos[1] <= self.trap[1][0]+self.step_size: 
                        if scattered: move_options_y = [0, -1]
                        else: move_options_y = [0, 1]
                    if self.trap[1][1]-self.step_size <= self.pos[1] <= self.trap[1][1]+self.step_size: 
                        if scattered: move_options_y = [0, 1]
                        else: move_options_y = [0, -1]
                    if scattered: self.trapped = False
                else:
                    if self.trap[0][0]-self.step_size <= self.pos[0] <= self.trap[0][0]+self.step_size: 
                        if scattered: move_options_x = [0, 1]
                        else: move_options_x = [0, -1]
                    if self.trap[0][1]-self.step_size <= self.pos[0] <= self.trap[0][1]+self.step_size: 
                        if scattered: move_options_x = [0, -1]
                        else: move_options_x = [0, 1]
                    if self.trap[1][0]-self.step_size <= self.pos[1] <= self.trap[1][0]+self.step_size: 
                        if scattered: move_options_y = [0, 1]
                        else: move_options_y = [0, -1]
                    if self.trap[1][1]-self.step_size <= self.pos[1] <= self.trap[1][1]+self.step_size: 
                        if scattered: move_options_y = [0, -1]
                        else: move_options_y = [0, 1]
                    if scattered: self.trapped = True

        if self.bounds[0][0]-self.step_size <= self.pos[0] <= self.bounds[0][0]+self.step_size: move_options_x = [0, 1]
        elif self.bounds[0][1]-self.step_size <= self.pos[0] <= self.bounds[0][1]+self.step_size: move_options_x = [0, -1]
        if move_options_x == []: move_options_x = [-1, 0, 1]
        self.pos[0] = self.pos[0] + rng.choice(move_options_x) * self.step_size

        if self.bounds[1][0]-self.step_size <= self.pos[1] <= self.bounds[1][0]+self.step_size: move_options_y = [0, 1]
        elif self.bounds[1][1]-self.step_size <= self.pos[1] <= self.bounds[1][1]+self.step_size: move_options_y = [0, -1]
        if move_options_y == []: move_options_y = [-1, 0, 1]
        self.pos[1] = self.pos[1] + rng.choice(move_options_y) * self.step_size

    def Check_Scattered(self, Ei_factor, Ej_factor):
        chance = Scattering_Chance(Ei_factor, Ej_factor)
        if chance <= 0: return False
        else: return rng.random() <= chance

    def Check_Recombined(self, Ei_factor=0, Ej_factor=0):
        chance = Recombination_Chance(Ei_factor, Ej_factor)
        if chance <= 0: return False
        else: return rng.random() <= chance

    def Check_Inside_Trap(self):
        if self.trap is None: return False
        else: return self.trap[1][0]-self.step_size <= self.pos[1] <= self.trap[1][1]+self.step_size and self.trap[0][0]-self.step_size <= self.pos[0] <= self.trap[0][1]+self.step_size

if __name__ == "__main__":

    QP = QuasiParticle([5, 5], [[0, 10], [0, 10]], 1, [[4.5,7.5], [4.5,5.5]])

    for i in range(1):
        print(QP.pos)
        #QP.Update_Pos()
        print(QP.Check_Scattered(20, 2))
        print(QP.Check_Recombined())
        print(QP.Check_Inside_Trap())