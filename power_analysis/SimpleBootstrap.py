import numpy as np
from scipy.stats import norm

class Model:
    def __init__(self, model_func):
        self.model_func = model_func
    
    def effect_size(self, n):
        return self.model_func(n)


class PowerAnalysis:
    def __init__(self, model, n, alpha=0.05, power=0.8, effect_size=0.5, iterations=1000):
        self.model = model
        self.n = n
        self.alpha = alpha
        self.power = power
        self.effect_size = effect_size
        self.iterations = iterations
        self.mde = np.zeros(self.iterations)
        for i in range(self.iterations):
            self.mde[i] = self.sample_size(self.model, self.alpha, self.power, self.effect_size, n=self.n)

    def sample_size(self, model, alpha, power, effect_size, n=None):
        """
        Calculate the sample size required to achieve a desired power level for a given model.

        Parameters
        ----------
        model : Model
            A model object that takes a sample size as input and returns the estimated effect size of the model.
        alpha : float
            The significance level to use for the power analysis.
        power : float
            The desired power level for the analysis.
        effect_size : float
            The expected effect size of the model.
        n : int, optional
            The starting sample size to use for the power analysis. If not specified, a default value of 50 is used.

        Returns
        -------
        int
            The sample size required to achieve the desired power level.
        """
        if n is None:
            n = 50

        delta = effect_size
        z_alpha = norm.ppf(1-alpha/2)
        z_beta = norm.ppf(power)
        sd = np.sqrt((model.effect_size(n)*(1-model.effect_size(n))) + (model.effect_size(n+z_alpha*delta)*(1-model.effect_size(n+z_alpha*delta))))
        n_star = ((z_alpha + z_beta) * sd / delta) ** 2

        while abs(n_star - n) > 1:
            n = n_star
            sd = np.sqrt((model.effect_size(n)*(1-model.effect_size(n))) + (model.effect_size(n+z_alpha*delta)*(1-model.effect_size(n+z_alpha*delta))))
            n_star = ((z_alpha + z_beta) * sd / delta) ** 2

        return int(n_star)

    def results(self):
        return {
            'minimum_detectable_effect': np.median(self.mde),
            'sample_size': self.n,
            'alpha': self.alpha,
            'power': self.power,
            'effect_size': self.effect_size,
            'iterations': self.iterations
        }


class TTestSampleSize:
    def __init__(self, mean_diff, sd, alpha, power, n=None):
        self.mean_diff = mean_diff
        self.sd = sd
        self.alpha = alpha
        self.power = power
        self.n = n
        self.calculate_sample_size()

    def calculate_sample_size(self):
        if self.n is None:
            self.n = 50

        delta = self.mean_diff
        z_alpha = norm.ppf(1-self.alpha/2)
        z_beta = norm.ppf(self.power)
        n_star = ((z_alpha + z_beta) * self.sd / delta) ** 2

        while abs(n_star - self.n) > 1:
            self.n = n_star
            n_star = ((z_alpha + z_beta) * self.sd/ delta) ** 2
        return int(n_star)
  
