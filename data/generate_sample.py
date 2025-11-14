import pandas as pd
import numpy as np
import os
import random

np.random.seed(42)
N = 1000 

races = ['Caucasian', 'AfricanAmerican', 'Other']
genders = ['Male', 'Female']
ages = ['[0-10)', '[10-20)', '[20-30)', '[30-40)', '[40-50)', '[50-60)', '[60-70)', '[70-80)', '[80-90)', '[90-100)']
readmitted_status = ['NO', '>30', '<30']
meds = ['No', 'Up', 'Down']

df = pd.DataFrame({
    'race': np.random.choice(races, size=N),
    'gender': np.random.choice(genders, size=N),
    'age': np.random.choice(ages, size=N),
    'time_in_hospital': np.random.randint(1, 15, size=N),
    'num_lab_procedures': np.random.randint(10, 80, size=N),
    'num_medications': np.random.randint(5, 50, size=N),
    'number_inpatient': np.random.poisson(1.5, size=N),
    'insulin': np.random.choice(meds, size=N),
    'metformin': np.random.choice(meds, size=N),
    'change': np.random.choice(['Ch', 'No'], size=N),
    'readmitted': np.random.choice(readmitted_status, size=N, p=[0.75, 0.15, 0.10])
})

output_path = 'data/diabetic_data_sample.csv'
df.to_csv(output_path, index=False)
print(f"Saved sample data to {output_path}")
