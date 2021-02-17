def weight_estimate(S_exposed, S_wetted, W_motors, W_battery):
    '''
    weight_estimate
    Function to give a (very) rough estimate of the TOGW based on Raymer Table 15.2

    Inputs:
        S_exposed: Exposed planform wing area (m^2)
        S_wetted: Wetted area of the fuselage (m^2)
        W_motors: Weight of the motors (kg)
        W_battery: Weight of the batteries (kg)

    Outputs:
        TOGM: (kg) Takeoff gross mass
           
    Calls:
        {none}

    Notes:
        1. A "fudge factor" of 2 is applied to motor weights to account for tilt mechanisms, etc.

    History:
        02.16.2021: Created, MP
    '''

    W_wing = 12*S_exposed
    W_ht   = 10*S_exposed
    W_vt   = 10*S_exposed

    W_f = 7*S_wetted

    subtotal = W_wing + W_ht + W_vt + W_motors*2 + W_battery # See note 1 for motor weight factor

    TOGM = subtotal/(1 - 0.157) # TOGM = subtotal + 0.157*TOGM

    return TOGM

if __name__ == "__main__":
    # Using C-182 Values for reference areas to test
    S_exposed = 16.2  # m^2
    S_wetted  = 26.94 # m^2
    W_motors  = 16.5  # kg
    W_battery = 168   # kg

    print("\n Testing Weight Estimate Function \n")
    TOGM = weight_estimate(S_exposed, S_wetted, W_motors, W_battery)
    print("\t Estimated Aircraft Weight", TOGM)