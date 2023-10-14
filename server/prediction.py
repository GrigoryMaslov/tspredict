import pickle
import numpy as np

def predict_mpg(data):

    pkl_filename = 'model\model.pkl'
    param_filename = 'model\param.pkl'
    
    series = np.array([float(close) for close in data['series'].split(',')])

    with open(pkl_filename, 'rb') as f_in:
        pickle_model = pickle.load(f_in)
        
    with open(param_filename, 'rb') as file:
        pickle_model_state = pickle.load(file)

    y_pred = pickle_model.apply({'params': pickle_model_state}, np.flip(series.reshape(-1,19,1)))
    ret = np.flip(y_pred.reshape(-1)).tolist()
    
    return ret