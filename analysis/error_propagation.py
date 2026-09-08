"""
PHYD57: Error Propagation & Non-linear Exponential Fitting Routine
Fits exponential decay data with Poisson counting uncertainties using SciPy curve_fit.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def decay_model(t, N0, tau, B):
    """Exponential decay with constant background."""
    return N0 * np.exp(-t / tau) + B

def fit_muon_data(t_data, counts):
    """
    Fits radioactive/particle decay data using Poisson weighting (sigma = sqrt(N)).
    """
    # Poisson counting error: sigma = sqrt(counts)
    sigma = np.sqrt(np.maximum(counts, 1.0))
    
    # Initial parameter guesses: [N0, tau, B]
    p0 = [counts[0], 2.2, np.mean(counts[-10:])]
    
    popt, pcov = curve_fit(decay_model, t_data, counts, p0=p0, sigma=sigma, absolute_sigma=True)
    
    perr = np.sqrt(np.diag(pcov))
    N0_fit, tau_fit, B_fit = popt
    tau_err = perr[1]

    # Goodness of fit: Reduced Chi-Square
    residuals = counts - decay_model(t_data, *popt)
    chi2 = np.sum((residuals / sigma)**2)
    dof = len(t_data) - len(popt)
    reduced_chi2 = chi2 / dof

    print(f"--- Fit Results ---")
    print(f"Mean Lifetime tau = {tau_fit:.4f} +/- {tau_err:.4f} microseconds")
    print(f"Reduced Chi^2 = {reduced_chi2:.3f} (dof = {dof})")

    return popt, pcov

if __name__ == '__main__':
    # Generate synthetic muon decay experiment data (tau_true = 2.197 us)
    np.random.seed(42)
    t = np.linspace(0.5, 10.0, 50)
    true_counts = decay_model(t, 2000, 2.197, 15)
    noisy_counts = np.random.poisson(true_counts)

    popt, pcov = fit_muon_data(t, noisy_counts)
