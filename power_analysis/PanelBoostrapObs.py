import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.power import TTestIndPower
from optional import Optional


class PowerAnalysis:
    """
    This class conducts power analysis on observational panel data using a clustered bootstrap method.

    It calculates statistical power by varying the number of observations (N) and effect sizes.
    The class takes the following input arguments:

    data: pandas.DataFrame
        A DataFrame containing the observational panel data.

    outcome_var: str
        The name of the column in the DataFrame representing the outcome variable.

    treatment_var: str
        The name of the column in the DataFrame representing the treatment variable.

    individual_var: str
        The name of the column in the DataFrame representing the individual identifier (cluster).

    random_seed: int, optional
        The random seed value for the random number generator to ensure reproducible results. If not provided, the results will vary between runs.

    Methods:
    --------
    fit_model(data: pd.DataFrame) -> Tuple[float, float]:
        Fits a linear regression model to the provided data and returns the treatment effect and p-value.

    clustered_bootstrap(n_bootstrap: int) -> Tuple[float, float, List[float]]:
        Performs a clustered bootstrap by resampling individuals (clusters) and returns the mean effect size, standard deviation of effect sizes, and a list of p-values.

    calculate_power_by_n(n_values: List[int], alpha: float, n_bootstrap: int) -> pd.DataFrame:
        Calculates the statistical power when varying the number of observations (N) and returns a DataFrame containing the N values and their corresponding statistical power.

    calculate_power_by_effect_size(effect_sizes: List[float], alpha: float, n_bootstrap: int) -> pd.DataFrame:
        Calculates the statistical power for a list of effect sizes and returns a DataFrame containing the effect sizes and their corresponding statistical power.
    """

    def __init__(self, data, outcome_var, treatment_var, individual_var, random_seed=None):
        self.data = data
        self.outcome_var = outcome_var
        self.treatment_var = treatment_var
        self.individual_var = individual_var
        if random_seed is not None:
            np.random.seed(random_seed)

    def fit_model(self, data: pd.DataFrame, control_vars: Optional[list[str]] = None,
                  fixed_effects: Optional[list[str]] = None, cluster_var: Optional[str] = None) -> tuple[float, float]:
        """
         Fits a linear regression model to the provided data and returns the treatment effect and p-value.

         Parameters:
         -----------
         data: pd.DataFrame
             A DataFrame containing the observational panel data.

         control_vars: List[str], optional
             A list of variables to include as fixed
              effects in the regression model.

         fixed_effects: List[str], optional
             A list of variables to include as fixed effects in the regression model.

         cluster_var: str, optional
             The name of the column in the DataFrame representing the individual identifier (cluster).

         Returns:  Tuple[float, float]
        """
        if control_vars is None:
            control_vars = []

        if fixed_effects is None:
            fixed_effects = []

        X = data[[self.treatment_var] + control_vars]
        X = pd.get_dummies(X, columns=fixed_effects, drop_first=True)
        X = sm.add_constant(X)
        y = data[self.outcome_var]

        model = sm.OLS(y, X).fit()

        if cluster_var is not None:
            cluster = data[cluster_var]
            model = model.get_robustcov_results(
                cov_type='cluster', groups=cluster)

        return model.params[self.treatment_var], model.pvalues[self.treatment_var]

    def clustered_bootstrap(self, n_bootstrap):
        """
         Performs a clustered bootstrap by resampling individuals (clusters) and returns the mean effect size, standard deviation of effect sizes, and a list of p-values.

         Parameters
         ----------
         n_bootstrap: int
             The number of bootstrap iterations.

         Returns
         -------
         Tuple[float, float
        """
        boot_results = []
        boot_pvalues = []

        for _ in range(n_bootstrap):
            sampled_individuals = np.random.choice(self.data[self.individual_var].unique(
            ), size=len(self.data[self.individual_var].unique()), replace=True)
            boot_data = self.data[self.data[self.individual_var].isin(
                sampled_individuals)]
            boot_result, boot_pvalue = self.fit_model(boot_data)
            boot_results.append(boot_result)
            boot_pvalues.append(boot_pvalue)

        return np.mean(boot_results), np.std(boot_results), boot_pvalues

    def calculate_power_by_n(self, n_values, alpha, n_bootstrap):
        """
         Calculates the statistical power when varying the number of observations (N) and returns a DataFrame containing the N values and their corresponding statistical power.

        Parameters
        ----------
        n_values: List[int]
            A list of N values.

        alpha: float
            The significance level.
        """
        power_by_n = []

        for n in n_values:
            _, _, boot_pvalues = self.clustered_bootstrap(n_bootstrap)
            power = np.mean(np.array(boot_pvalues) < alpha)
            power_by_n.append(power)

        return pd.DataFrame({'N': n_values, 'Power': power_by_n})

    def calculate_power_by_effect_size(self, effect_sizes, alpha, n_bootstrap):
        """
         Calculates the statistical power for a list of effect sizes and returns a DataFrame containing the effect sizes and their corresponding statistical power.

         Parameters
         ----------
         effect_sizes: List[float]
             A list of effect sizes.

         alpha: float
             The significance level.

         n_bootstrap: int
        """
        _, _, boot_pvalues = self.clustered_bootstrap(n_bootstrap)
        power_by_effect_size = []

        for effect_size in effect_sizes:
            pvalues = np.array(boot_pvalues)
            power = np.mean((pvalues < alpha) & (
                np.abs(self.data[self.treatment_var]) >= effect_size))
            power_by_effect_size.append(power)

        return pd.DataFrame({'Effect Size': effect_sizes, 'Power': power_by_effect_size})
