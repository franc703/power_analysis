# power_analysis 💪🔍

`power-analysis` is a Python package for performing power analysis and calculating sample sizes for statistical models. The package provides classes for defining statistical models, performing power analysis, and calculating sample sizes for two-sample t-tests.

## Installation 📥

You can install the `power_analysis` package using pip:

```bash
pip install power_analysis
```

## Usage 🧑‍💻

To use the `power-analysis` package, you first need to define a statistical model using a Python function that takes a sample size as input and returns the estimated effect size of the model. For example:

```python
def my_model(n):
    # define your model here
    effect_size = ...
    return effect_size
```

You can then create a `Model` object using this function:

```python
from power_analysis import Model

model = Model(my_model)
```

You can perform a power analysis for this model using the `PowerAnalysis` class:

```python
from power_analysis import PowerAnalysis

power_analysis = PowerAnalysis(model, n=100, alpha=0.05, power=0.8, effect_size=0.5, iterations=1000)
results = power_analysis.results()
```

This will calculate the minimum detectable effect and sample size required to achieve a power of 0.8 for the given model, starting with an initial sample size of 100.

You can also calculate the sample size required for a two-sample t-test using the `TTestSampleSize` class:

```python
from power_analysis import TTestSampleSize

mean_diff = 1.5
sd = 2.0
alpha = 0.05
power = 0.8

sample_size = TTestSampleSize(mean_diff, sd, alpha, power, n=None)
n = sample_size.result()
```

This will calculate the sample size required to achieve a power of 0.8 for a two-sample t-test with a difference in means of 1.5, a standard deviation of 2.0, and a significance level of 0.05.

## Contributing 🤝

Contributions to `power-analysis` are welcome! If you find a bug or would like to suggest a new feature, please open an issue on GitHub.

## License 📜

`power-analysis` is licensed under the MIT license. See `LICENSE` for more information.
