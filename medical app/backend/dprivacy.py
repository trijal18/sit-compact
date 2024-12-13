from google.privacy.differential_privacy import (
    dp_statistics,
    dp_histogram
)

# Differential privacy for adding noise to data
def add_noise_to_data(data, epsilon=1.0):
    noisy_data = dp_statistics.dp_sum(data, epsilon)
    return noisy_data

# Differentially private histogram
def private_histogram(data, epsilon=1.0):
    histogram = dp_histogram(data, epsilon)
    return histogram
