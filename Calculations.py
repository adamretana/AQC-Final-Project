import numpy as np
from scipy.special import gamma, factorial

tau0 = 438 #ns characteristic_electron_phonon_time
kB = 8.617 * np.power(10.0, -5) # eV/K boltzmann_constant
Tc = 1.19 # K critical_temperature
kBTc = kB*Tc
#Nqp_over_Ncp = 1 - .001 # QuasiParticle density over cooper pair density
Delta0 = 1.764 * kBTc  # fermi_energy_level
gamma_zeta_constant = 3.74453 # Gamma[3.5] * Zeta[3.5]

def Scattering_Lifetime_Limit(energy_omega):
    a = 1.764 # constant of Delta0
    ratio_omega_delta = energy_omega/Delta0

    limit = tau0 / (np.power(a,3) * (((1/3)*np.power((ratio_omega_delta**2-1),3/2)) + (5/2)*np.power((ratio_omega_delta**2-1),.5) - (1/(2*ratio_omega_delta)) * (1+4*ratio_omega_delta**2) * np.log(ratio_omega_delta+np.power((ratio_omega_delta**2-1),.5))))
    return limit
def Scattering_Lifetime(energy_omega, temperature):
    tau_s = tau0 / (gamma_zeta_constant * np.power((kB*Tc/energy_omega),.5)*np.power((temperature/Tc),3.5))
    if energy_omega > Delta0: 
        limit = Scattering_Lifetime_Limit(energy_omega)
        return limit*tau_s / (limit+tau_s)
    else:
        return tau_s
def Scattering_Probability(time, energy_omega, temperature):
    lifetime = Scattering_Lifetime(energy_omega, temperature)
    return 1-np.e**(-time/lifetime)

def Recombination_Lifetime(energy_omega, temperature):
    tau_r = tau0 / (np.pi**(1/2) * (energy_omega/kBTc)**(5/2) * (temperature/Tc)**(1/2) * np.power(np.e, -Delta0/(kB*temperature)))
    return tau_r
def Recombination_Probability(time, energy_omega, temperature):
    lifetime = Recombination_Lifetime(energy_omega, temperature)
    return 1-np.e**(-time/lifetime)

if __name__ == "__main__":
    E = 4*Delta0
    T = 20 * 10**-3
    print(Scattering_Probability(1, E, T))
    print(Recombination_Probability(1, E, T))

    L1 = [1, 0]
    L2 = [0, 1]
    print(list(map(lambda x, y: x + y, L1, L2)))
