import numpy as np 

CAR_NUM = 2000

REGION_NUM = 9

LBD_ARR = np.array([0.0131, 0.0624, 0.0381, 0.0652, 0.0870, 0.1178, 0.0762,0.1438, 0.2751])

P_MAT = np.array([    
    # line sum of data provided in the paper is not 1.
    # data here has been modified.
    [0.230, 0.297, 0.372, 0.004, 0.026, 0.029, 0.009, 0.018, 0.015],    # 1.000
    [0.044, 0.655, 0.145, 0.005, 0.079, 0.038, 0.018, 0.005, 0.011],    # 1.000
    [0.165, 0.291, 0.288, 0.007, 0.054, 0.126, 0.017, 0.025, 0.027],    # 1.000
    [0.0013, 0.010, 0.006, 0.139, 0.031, 0.185, 0.101, 0.117, 0.4097],  # 1.000
    [0.005, 0.096, 0.026, 0.037, 0.249, 0.332, 0.216, 0.012, 0.027],    # 1.000
    [0.004, 0.031, 0.032, 0.087, 0.121, 0.426, 0.148, 0.059, 0.092],    # 1.000
    [0.002, 0.023, 0.011, 0.066, 0.141, 0.269, 0.399, 0.020, 0.069],    # 1.000
    [0.004, 0.008, 0.023, 0.067, 0.011, 0.095, 0.018, 0.400, 0.374],    # 1.000
    [0.001, 0.004, 0.005, 0.095, 0.010, 0.059, 0.030, 0.185, 0.611]     # 1.000
])

MU_MAT = np.reciprocal(np.array([   
    # data provided in the paper is 1/mu.
    # use np.reciprocal to get mu.
    [0.83, 1.87, 1.07, 3.89, 3.25, 2.79, 4.25, 2.94, 4.37],
    [1.78, 0.89, 1.18, 3.24, 1.24, 1.99, 2.89, 3.46, 4.18],
    [1.02, 1.31, 0.78, 2.82, 1.45, 1.36, 3.26, 2.17, 3.04],
    [3.52, 3.13, 2.76, 0.93, 1.5 ,1.26 ,1.49 ,1.75 ,1.6],
    [2.86, 1.42, 1.64, 1.55, 0.84, 1.04, 1.45, 2.88, 2.89],
    [2.61, 2.17, 1.54, 1.31, 1.15, 0.81, 1.86, 1.78, 2.2],
    [4.38, 3.02, 2.79, 1.36, 1.35, 1.65, 0.94, 3.1, 3],
    [2.93, 3.06, 2.26, 1.75, 2.69, 1.62, 3.23, 0.9, 1.482],
    [3.58, 4.18, 2.8, 1.49, 2.46, 2.02, 2.72, 1.43, 1.01]
]))