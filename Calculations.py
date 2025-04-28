import numpy as np

tau0 = 400 #ns characteristic_electron_phonon_time
kB = np.power(1.380649, -23) # boltzmann_constant
Tc = 1.2 # critical_temperature
kBTc = kB*Tc
Nqp_over_Ncp = 1 - .001 # QuasiParticle density over cooper pair density
Delta = 1.764 * kBTc * Nqp_over_Ncp # energy_band_gap_with_qps


def Np(Energy): 
    return 1 / abs(np.power(np.e, -(Energy)/kBTc) - 1) # phonon_occupation_factor
def Rho(Energy):
    return Energy / np.emath.sqrt(np.power(Energy,2) - np.power(Delta,2)) # normalized density of quasiparticle states

def Scattering_Chance(Ei_factor, Ej_factor):
    if Ei_factor == Ej_factor: return 0
    Ei = Ei_factor * kBTc
    Ej = Ej_factor * kBTc
    if Ej < Delta: return 0
    Ei_minus_Ej = Ei-Ej
    Np_curr = Np(Ei_minus_Ej)
    rho = Rho(Ej)
    rate = np.power((Ei_minus_Ej),2) / (tau0 * np.power((kBTc),3)) * (1 - np.power(Delta,2) / (Ei*Ej)) * Np_curr * rho
    return 1 - np.power(np.e, -rate)

def Recombination_Chance(Ei_factor, Ej_factor):
    if Ei_factor == Ej_factor: return 21.8/tau0 * Nqp_over_Ncp
    Ei = Ei_factor * kBTc
    Ej = Ej_factor * kBTc
    if Ej < Delta: return 0
    Ei_plus_Ej = Ei+Ej
    Np_curr = Np(Ei_plus_Ej)
    rho = Rho(Ej)
    f = 1 / (1 + np.power(np.e, Ej/kBTc)) # occupation probability
    rate = np.power((Ei_plus_Ej),2) / (tau0 * np.power((kBTc),3)) * (1 + np.power(Delta,2) / (Ei*Ej)) * Np_curr * rho * f
    return 1 - np.power(np.e, -rate)

if __name__ == "__main__":
    print(Delta)
    E1, E2 = 2, 2
    print(Scattering_Chance(E1,E2))
    print(Recombination_Chance(E1,E2))

    #print(1 - np.power(np.e, -(Recombination_Rate(E1,E2))))
    #print(1 - np.power(np.e, -(Scattering_Rate(E1,E2))))

