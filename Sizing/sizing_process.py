import numpy
import component_sizing
import weight_estimate



def sizing_process():

    '''
    The sizing analysis process loop based on Fig.4 of the report
        from the report "eVTOL Sizing"
        shared by TVG in Discord #Sizing channel 02.16.2021 12:29pm



    '''


    ## Assumed properties:

    # Efficiencies:
    eta_mech = 0.9
    eta_p = 0.85
    V_hover_climb = 2.54 #m/s (equivalent to 500 ft/min)
    V_climb = 44 #m/s (equivalent to 85.53 knots)
    V_cruise = 62 #m/s (equivalent to 120.52 knots)
    f = 

    # Apply requirements

    # Roughly guess TOGW
    g = 9.81
    TOGM_guess = weight_estimate(S_exposed, S_wetted, W_motors, W_battery)  
    TOGW_guess = TOGM_guess * g
    # Find power required


    cont = True     # signals while loop to continue
    tol = 1         # tolerance for convergence
    iter_num = 0    # time of iteration
    MAX_ITER = 3000 # maximum number of iteration

    while cont:
        ### FIXME: Find power based on mission req & atmosphere

        P_cruise, P_climb, P_hover_climb = component_sizing.power_requirements(
            eta_mech, eta_p, V_hover_climb, V_climb, V_cruise, 
            TOGW_guess, f, M, S_disk, S_wing, rho, CD0, AR, e, gam_climb
        )

        # Final power system weight, find & record battery size
        W_power_system = component_sizing.power_system_mass_sizing(distr, rho_battery, E, P_req_H2, battery_reserve)

        # Electric Motor Weights
        W_motors = component_sizing.electric_motor_weight(max(P_cruise, P_climb, P_hover_climb))
        # Slap on a "fudge factor" of 2 to account for propellers, motor controller, wiring, etc.
        W_motors = W_motors*2
        
        # Find component weights
        


        # Check guess TOGW
        TOGW_est = weight_estimate.weight_estimate(S_exposed, S_wetted, W_motors, W_power_system)
        

        if abs(TOGW_est - TOGW_guess) < tol:    # if converges
            print("The converged TOGW is " + str(TOGW_est) + " lbf")
            return TOGW_est

        else:       # not yet converging
            TOGW_guess = TOGW_est   

            if TOGW_guess > 25000:  #(lbf)
                print("No Convergence, guessed TOGW larger than 25000 lbf")
                return

        iter_num += 1
        
        if iter_num > MAX_ITER:
            print("Iteration number exceeded limit: " + str(MAX_ITER) + ".")
            print("Function not showing convergence.")
            print("Consider re-evaluating assumptions and requirements.")
            return



    
