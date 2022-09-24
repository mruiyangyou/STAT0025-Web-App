import numpy as np

class Input(object):

    num_of_products = 2
    cost_coef = np.array([3, 8])
    resources_coef = np.array([[2, 4], [6,2], [0,1]])
    resources = np.array([1600, 1800, 350])
    product_name = ['No. 1','No.2']
    resource_name = ['Labour', 'Processing', 'assembly']
    save_name = 'fig1.png'