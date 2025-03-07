
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print('TensorFlow version:', tf.__version__)
print('NumPy version:', np.__version__)
print('Pandas version:', pd.__version__)

# Test TensorFlow
print('GPU Available:', tf.config.list_physical_devices('GPU'))

# Create a simple plot
plt.figure(figsize=(4, 3))
plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
plt.title('Test Plot')
plt.savefig('test_plot.png')
print('Plot saved to test_plot.png')

