#cython: boundscheck=False
#cython: wraparound=False
cimport numpy as np

{0}
    
def RK4(np.ndarray[complex_t, ndim=4] U_hat, 
        np.ndarray[complex_t, ndim=4] U_hat0, 
        np.ndarray[complex_t, ndim=4] U_hat1, 
        np.ndarray[complex_t, ndim=4] dU,
        np.ndarray[real_t, ndim=1] a, 
        np.ndarray[real_t, ndim=1] b,
        real_t dt,
        ComputeRHS):
    cdef complex_t z
    cdef unsigned int rk, i, j, k, l
    for i in xrange(dU.shape[0]):
        for j in xrange(dU.shape[1]):
            for k in xrange(dU.shape[2]):
                for l in xrange(dU.shape[3]):
                    z = U_hat[i,j,k,l]
                    U_hat1[i,j,k,l] = z 
                    U_hat0[i,j,k,l] = z
        
    for rk in xrange(4):
        dU = ComputeRHS(dU, rk)
        if rk < 3:
            for i in xrange(dU.shape[0]):
                for j in xrange(dU.shape[1]):
                    for k in xrange(dU.shape[2]):
                        for l in xrange(dU.shape[3]):
                            U_hat[i,j,k,l] = U_hat0[i,j,k,l] + b[rk]*dt*dU[i,j,k,l]
            
        for i in xrange(dU.shape[0]):
            for j in xrange(dU.shape[1]):
                for k in xrange(dU.shape[2]):
                    for l in xrange(dU.shape[3]):
                        U_hat1[i,j,k,l] = U_hat1[i,j,k,l] + a[rk]*dt*dU[i,j,k,l]
                        
    for i in xrange(dU.shape[0]):
        for j in xrange(dU.shape[1]):
            for k in xrange(dU.shape[2]):
                for l in xrange(dU.shape[3]):
                    U_hat[i,j,k,l] = U_hat1[i,j,k,l]
                    
    return U_hat

def ForwardEuler(np.ndarray[complex_t, ndim=4] U_hat, 
                 np.ndarray[complex_t, ndim=4] U_hat0, 
                 np.ndarray[complex_t, ndim=4] dU, 
                 real_t dt,
                 ComputeRHS):
    cdef complex_t z
    cdef unsigned int rk, i, j, k, l
    dU = ComputeRHS(dU, 0)
    for i in xrange(dU.shape[0]):
        for j in xrange(dU.shape[1]):
            for k in xrange(dU.shape[2]):
                for l in xrange(dU.shape[3]):
                    U_hat[i,j,k,l] = U_hat[i,j,k,l] + dU[i,j,k,l]*dt 
    return U_hat

def AB2(np.ndarray[complex_t, ndim=4] U_hat, 
        np.ndarray[complex_t, ndim=4] U_hat0, 
        np.ndarray[complex_t, ndim=4] dU,
        real_t dt, int tstep,
        ComputeRHS):
    cdef complex_t z
    cdef real_t p0 = 1.5
    cdef real_t p1 = 0.5
    cdef unsigned int rk, i, j, k, l
    dU = ComputeRHS(dU, 0)
    
    if tstep == 1:
        for i in xrange(dU.shape[0]):
            for j in xrange(dU.shape[1]):
                for k in xrange(dU.shape[2]):
                    for l in xrange(dU.shape[3]):
                        U_hat[i,j,k,l] = U_hat[i,j,k,l] + dU[i,j,k,l]*dt
                        
    else:
        for i in xrange(dU.shape[0]):
            for j in xrange(dU.shape[1]):
                for k in xrange(dU.shape[2]):
                    for l in xrange(dU.shape[3]):
                        U_hat[i,j,k,l] = U_hat[i,j,k,l] + p0*dU[i,j,k,l]*dt - p1*U_hat0[i,j,k,l]   
                    
    for i in xrange(dU.shape[0]):
        for j in xrange(dU.shape[1]):
            for k in xrange(dU.shape[2]):
                for l in xrange(dU.shape[3]):                    
                    U_hat0[i,j,k,l] = dU[i,j,k,l]*dt
    return U_hat

def RK4_2D(np.ndarray[complex_t, ndim=3] U_hat, 
        np.ndarray[complex_t, ndim=3] U_hat0, 
        np.ndarray[complex_t, ndim=3] U_hat1, 
        np.ndarray[complex_t, ndim=3] dU,
        np.ndarray[real_t, ndim=1] a, 
        np.ndarray[real_t, ndim=1] b,
        real_t dt,
        ComputeRHS):
    cdef complex_t z
    cdef unsigned int rk, i, j, k
    for i in xrange(dU.shape[0]):
        for j in xrange(dU.shape[1]):
            for k in xrange(dU.shape[2]):
                z = U_hat[i,j,k]
                U_hat1[i,j,k] = z 
                U_hat0[i,j,k] = z
        
    for rk in xrange(4):
        dU = ComputeRHS(dU, rk)
        if rk < 3:
            for i in xrange(dU.shape[0]):
                for j in xrange(dU.shape[1]):
                    for k in xrange(dU.shape[2]):
                        U_hat[i,j,k] = U_hat0[i,j,k] + b[rk]*dt*dU[i,j,k]
            
        for i in xrange(dU.shape[0]):
            for j in xrange(dU.shape[1]):
                for k in xrange(dU.shape[2]):
                    U_hat1[i,j,k] = U_hat1[i,j,k] + a[rk]*dt*dU[i,j,k]
                        
    for i in xrange(dU.shape[0]):
        for j in xrange(dU.shape[1]):
            for k in xrange(dU.shape[2]):
                U_hat[i,j,k] = U_hat1[i,j,k]
                    
    return U_hat

def ForwardEuler_2D(np.ndarray[complex_t, ndim=3] U_hat, 
                    np.ndarray[complex_t, ndim=3] U_hat0, 
                    np.ndarray[complex_t, ndim=3] dU, 
                    real_t dt,
                    ComputeRHS):
    cdef complex_t z
    cdef unsigned int rk, i, j, k
    dU = ComputeRHS(dU, 0)
    for i in xrange(dU.shape[0]):
        for j in xrange(dU.shape[1]):
            for k in xrange(dU.shape[2]):
                U_hat[i,j,k] = U_hat[i,j,k] + dU[i,j,k]*dt 
    return U_hat

def AB2_2D(np.ndarray[complex_t, ndim=3] U_hat, 
           np.ndarray[complex_t, ndim=3] U_hat0, 
           np.ndarray[complex_t, ndim=3] dU,
           real_t dt, int tstep,
           ComputeRHS):
    cdef complex_t z
    cdef real_t p0 = 1.5
    cdef real_t p1 = 0.5
    cdef unsigned int rk, i, j, k
    dU = ComputeRHS(dU, 0)
    
    if tstep == 1:
        for i in xrange(dU.shape[0]):
            for j in xrange(dU.shape[1]):
                for k in xrange(dU.shape[2]):
                    U_hat[i,j,k] = U_hat[i,j,k] + dU[i,j,k]*dt
                        
    else:
        for i in xrange(dU.shape[0]):
            for j in xrange(dU.shape[1]):
                for k in xrange(dU.shape[2]):
                    U_hat[i,j,k] = U_hat[i,j,k] + p0*dU[i,j,k]*dt - p1*U_hat0[i,j,k]   
                    
    for i in xrange(dU.shape[0]):
        for j in xrange(dU.shape[1]):
            for k in xrange(dU.shape[2]):
                U_hat0[i,j,k] = dU[i,j,k]*dt
    return U_hat
