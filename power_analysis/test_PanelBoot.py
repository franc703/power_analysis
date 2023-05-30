import pytest
import pandas as pd
import numpy as np

from power_analysis.PanelBoostrapObs import PowerAnalysis

# Prepare a mock DataFrame
df = pd.DataFrame({
    'outcome_var': np.random.normal(size=100),
    'treatment_var': np.random.choice([0, 1], size=100),
    'individual_var': np.repeat(np.arange(10), 10)
})

# Parameters for the power analysis
n_values = [10, 20, 30, 40, 50]
alpha = 0.05
n_bootstrap = 1000
effect_sizes = [0.1, 0.2, 0.3, 0.4, 0.5]


@pytest.fixture
def power_analysis():
    return PowerAnalysis(df, 'outcome_var', 'treatment_var', 'individual_var')

# pylint: disable=redefined-outer-name
def test_fit_model(power_analysis):
    effect, pvalue = power_analysis.fit_model(df)
    assert isinstance(effect, float)
    assert isinstance(pvalue, float)

# pylint: disable=redefined-outer-name
def test_clustered_bootstrap(power_analysis):
    mean_effect, std_effect, pvalues = power_analysis.clustered_bootstrap(n_bootstrap)
    assert isinstance(mean_effect, float)
    assert isinstance(std_effect, float)
    assert isinstance(pvalues, list)
    assert len(pvalues) == n_bootstrap

# pylint: disable=redefined-outer-name
def test_calculate_power_by_n(power_analysis):
    power_df = power_analysis.calculate_power_by_n(n_values, alpha, n_bootstrap)
    assert isinstance(power_df, pd.DataFrame)
    assert 'N' in power_df.columns
    assert 'Power' in power_df.columns
    assert power_df.shape[0] == len(n_values)


#def test_calculate_power_by_effect_size(power_analysis):
    #power_df = power_analysis.calculate_power_by_effect_size(effect_sizes, alpha, n_bootstrap)
    #assert isinstance(power_df, pd.DataFrame)
    #assert 'Effect Size' in power_df.columns
    #assert 'Power' in power_df.columns
    #assert power_df.shape[0] == len(effect_sizes)
