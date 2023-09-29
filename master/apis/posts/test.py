import numpy as np

# Your word embedding as a string
embedding_str = """[-4.51856017e-01 6.01150155e-01 1.21269770e-01 -6.36690110e-02
  5.67807059e-04 -7.72317126e-02 8.67062032e-01 -4.49611455e-01
  1.61486730e-01 3.11046690e-01 5.14357209e-01 -2.76766479e-01
  ]"""

# Remove line breaks and split the string into individual numbers
print(embedding_str)
embedding_str = embedding_str.replace('\n', ' ').strip()
print(embedding_str)
embedding_str = embedding_str.strip('[]')
embedding_list = embedding_str.split()

# Convert the list of strings to a NumPy array of floats
embedding = np.array([float(num) for num in embedding_list])

# Now 'embedding' contains your word embedding as a NumPy array
print(embedding)
