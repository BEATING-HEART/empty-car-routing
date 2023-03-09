import numpy as np 
import cvxpy as cp

from logger import log

class FluidModel(object):
    """ fluid model of empty car routing problem """
    
    def __init__(self) -> None:
        pass

    def get_fluid_q(self, r_num: int, lbd: np.ndarray, mu: np.ndarray, p_mat: np.ndarray):

        _p_mat = cp.Parameter((r_num, r_num), nonneg=True, value=p_mat)
        _lbd_vec = cp.Parameter(r_num, nonneg=True, value=lbd)   # ok
        _mu_mat = cp.Parameter((r_num, r_num), nonneg=True, value=mu)

        _avail_vec = cp.Variable(r_num, pos=True)
        _e_mat = cp.Variable((r_num, r_num), pos=True)
        _f_mat = cp.Variable((r_num, r_num), pos=True)

        constraints = []
        car_sum = 0
        obj_func = 0
        
        for i in range(r_num):
            for j in range(r_num):
                obj_func += _avail_vec[i] * _lbd_vec[i] * _p_mat[i, j]    # objective function

                constraints += [_lbd_vec[i] * _p_mat[i, j] * _avail_vec[i] == _mu_mat[i, j] * _f_mat[i, j]]
                constraints += [_e_mat[i, j] >= 0, _e_mat[i, j] <= 1, _f_mat[i, j] >= 0, _f_mat[i, j] <= 1]
                car_sum += (_e_mat[i, j] + _f_mat[i, j])
            
            constraints += [_lbd_vec[i] * _avail_vec[i] + _mu_mat[i, :] @ _e_mat[i, :] - _mu_mat[i, i] * _e_mat[i, i] 
                            == _mu_mat[:, i] @ _e_mat[:, i] - _mu_mat[i, i] * _e_mat[i, i] + _mu_mat[:, i] @ _f_mat[:, i]]
            
            constraints += [_avail_vec[i] >= 0, _avail_vec[i] <= 1]
            
        constraints += [car_sum == 1] 

        obj = cp.Maximize(obj_func)
        prob = cp.Problem(obj, constraints)
        prob.solve()

        log.debug(prob.status)
        log.debug(prob.value)
        
        q_matrix = np.zeros((r_num, r_num))
        for i in range(r_num):
            denominator = _mu_mat.value[:, i] @ _f_mat.value[:, i]
            for j in range(r_num):
                if i == j:
                    log.debug(_lbd_vec[i])
                    q_matrix[i, j] = _lbd_vec.value[i] * _avail_vec.value[i] - (_mu_mat.value[:, i] @ _e_mat.value[:, i] - _mu_mat.value[i, i] * _e_mat.value[i, i])
                else:
                    q_matrix[i, j] = _mu_mat.value[i, j] * _e_mat.value[i, j]
                q_matrix[i, j] /= denominator
        
        return np.round(q_matrix, decimals=5)        