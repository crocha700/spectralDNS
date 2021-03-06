__author__ = "Mikael Mortensen <mikaem@math.uio.no> and Diako Darian <diako.darian@mn.uio.no>"
__date__ = "2014-11-07"
__copyright__ = "Copyright (C) 2014 " + __author__
__license__  = "GNU Lesser GPL version 3 or any later version"

from spectralinit import *

hdf5file = HDF5Writer(comm, N, float, {"U":U[0], "V":U[1], "rho":rho, "P":P}, config.solver+".h5")
Ri = float(config.Ri)
Pr = float(config.Pr)

@optimizer
def add_pressure_diffusion(dU, P_hat, U_hat, rho_hat, K_over_K2, K, K2, nu, Ri, Pr):
    # Compute pressure (To get actual pressure multiply by 1j)
    P_hat  = sum(dU[:2]*K_over_K2, 0, out=P_hat)
    
    P_hat -= Ri*rho_hat*K_over_K2[1]
    
    # Add pressure gradient
    dU[:2] -= P_hat*K

    # Add contribution from diffusion                      
    dU[0] -= nu*K2*U_hat[0]
    
    dU[1] -= (nu*K2*U_hat[1] + Ri*rho_hat)
    dU[2] -= nu * K2 * rho_hat/Pr  
    return dU

def ComputeRHS(dU, rk):
    if rk > 0: # For rk=0 the correct values are already in U, V, W
        for i in range(3):
            Ur[i] = ifft2_mpi(Ur_hat[i], Ur[i])

    F_tmp[0] = cross2(F_tmp[0], K, U_hat)
    curl[:] = ifft2_mpi(F_tmp[0], curl)
    dU[0] = fft2_mpi(U[1]*curl, dU[0])
    dU[1] = fft2_mpi(-U[0]*curl, dU[1])
   
    F_tmp[0] = fft2_mpi(U[0]*rho, F_tmp[0])
    F_tmp[1] = fft2_mpi(U[1]*rho, F_tmp[1])
    dU[2] = -1j*(K[0]*F_tmp[0]+K[1]*F_tmp[1])
    
    #U_tmp[0] = ifft2_mpi(1j*K[0]*rho_hat, U_tmp[0])
    #U_tmp[1] = ifft2_mpi(1j*K[1]*rho_hat, U_tmp[1])          
    #F_tmp[0] = fft2_mpi(U[0]*U_tmp[0], F_tmp[0])      
    #F_tmp[1] = fft2_mpi(U[1]*U_tmp[1], F_tmp[1])    
    #dU[2] = -1.0*(F_tmp[0] + F_tmp[1])    
    
    dU = dealias_rhs(dU, dealias)
    
    dU = add_pressure_diffusion(dU, P_hat, U_hat, rho_hat, K_over_K2, K, K2, nu, Ri, Pr)
    
    return dU

# Set up function to perform temporal integration (using config.integrator parameter)
integrate = getintegrator(**vars())

def regression_test(**kw):
    pass

def solve():
    timer = Timer()
    t = 0.0
    tstep = 0
    while t < config.T-1e-8:
        t += dt 
        tstep += 1
        
        Ur_hat[:] = integrate(t, tstep, dt)

        for i in range(3):
            Ur[i] = ifft2_mpi(Ur_hat[i], Ur[i])
                 
        update(t, tstep, **globals())
        
        timer()
        
        if tstep == 1 and config.make_profile:
            #Enable profiling after first step is finished
            profiler.enable()

    timer.final(MPI, rank)
    
    if config.make_profile:
        results = create_profile(**globals())
        
    regression_test(**globals())        
        
    hdf5file.close()
