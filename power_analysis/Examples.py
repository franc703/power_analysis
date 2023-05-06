# Load your data (replace with your actual data)
data = pd.read_csv("your_data_file.csv")

# Replace these with your actual variables
outcome_var = 'outcome'
treatment_var = 'treatment'
individual_var = 'individual'

# Define your desired significance level and number of bootstrap repetitions
alpha = 0.05
n_bootstrap = 1000

# Initialize the PowerAnalysis class with your data and variables
power_analysis = PowerAnalysis(
    data, outcome_var, treatment_var, individual_var)

# Specify the range of observations (N) and effect sizes you want to analyze
n_values = list(range(10, 200, 10))
effect_sizes = np.arange(0.1, 1.1, 0.1)

# Calculate power by varying N and effect size
power_by_n_df = power_analysis.calculate_power_by_n(
    n_values, alpha, n_bootstrap)
power_by_effect_size_df = power_analysis.calculate_power_by_effect_size(
    effect_sizes, alpha, n_bootstrap)

print("Power by varying N:")
print(power_by_n_df)

print("\nPower by varying effect size:")
print(power_by_effect_size_df)
