[![Python package CI](https://github.com/franc703/power_analysis/actions/workflows/python-package.yml/badge.svg)](https://github.com/franc703/power_analysis/actions/workflows/python-package.yml)

# power-analysis 💪🔍

`power-analysis` is a Python package for performing power analysis and calculating sample sizes for statistical models. The package provides classes for defining statistical models, performing power analysis, calculating sample sizes for two-sample t-tests, and conducting power analysis on observational panel data using a clustered bootstrap method.

## Installation 📥

You can install the `power_analysis` package using pip:

```bash
pip install power-analysis
```

## Usage 🧑‍💻

### Panel Data Power Analysis

To use the `PanelBootstrapObs` class for power analysis on observational panel data, you can follow these steps:

1. Import the required packages and classes:

```python
import numpy as np
import pandas as pd
from power_analysis import PanelBootstrap
```

2. Load your panel data into a pandas DataFrame:

```python
data = pd.read_csv('your_data.csv')
```

3. Create a `PanelBootstrap` object with the required parameters:

```python
power_analysis = PanelBootstrap(data, outcome_var='outcome', treatment_var='treatment', individual_var='individual', random_seed=42)
```

4. Use the `fit_model` method to fit a linear regression model and obtain the treatment effect and p-value:

```python
treatment_effect, p_value = power_analysis.fit_model(data)
```

5. Perform a clustered bootstrap analysis to obtain the mean effect size, standard deviation of effect sizes, and a list of p-values:

```python
mean_effect_size, std_effect_size, p_values = power_analysis.clustered_bootstrap(n_bootstrap=1000)
```

6. Calculate the statistical power when varying the number of observations (N) or effect sizes:

```python
n_values = [50, 100, 150, 200, 250, 300]
alpha = 0.05
n_bootstrap = 1000

power_by_n = power_analysis.calculate_power_by_n(n_values, alpha, n_bootstrap)
power_by_effect_size = power_analysis.calculate_power_by_effect_size(effect_sizes, alpha, n_bootstrap)
```

## Contributing 🤝

Contributions to `power-analysis` are welcome! If you find a bug or would like to suggest a new feature, please open an issue on GitHub, thank you.

## License 📜

`power-analysis` is licensed under the MIT license. See `LICENSE` for more information.
