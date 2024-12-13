import unittest
from differential_privacy import add_noise_to_data, private_histogram

class TestPrivacy(unittest.TestCase):
    
    def test_add_noise_to_data(self):
        data = [1, 2, 3, 4, 5]
        epsilon = 0.5
        noisy_data = add_noise_to_data(data, epsilon)
        self.assertNotEqual(noisy_data, sum(data))  # Should not be the same as the sum of the original data
    
    def test_private_histogram(self):
        data = [1, 2, 2, 3, 3, 3, 4, 4, 5]
        epsilon = 1.0
        histogram = private_histogram(data, epsilon)
        self.assertIsInstance(histogram, dict)  # Assuming the output is a dictionary of frequencies

if __name__ == '__main__':
    unittest.main()
