def mass_estimate(S_exposed, S_wetted_fuse, motors_mass, power_system_mass, payload):
    '''
    mass_estimate
    Function to give a (very) rough estimate of the Takeoff Gross Mass (TOGM) based on Raymer Table 15.2

    Inputs:
        S_exposed: Exposed planform wing area (m^2)
        S_wetted_fuse: Wetted area of the fuselage (m^2)
        motors_mass: Weight of the motors (kg)
        power_system_mass: Weight of the batteries (kg)
        payload: Mass of payload (kg)

    Outputs:
        TOGM: (kg) Takeoff gross mass

    Calls:
        {none}

    Notes:
        1. A "fudge factor" of 2 is applied to motor weights to account for tilt mechanisms, etc.

    History:
        02.16.2021: Created, MP
        02.16.2021: Modified to reflect masses rather than weights and debugged, TVG
        02.17.2021: Added payload as an input
    '''

    wing_mass = 12 * S_exposed
    ht_mass = 10 * S_exposed * 0.17
    vt_mass = 10 * S_exposed * 0.13

    fuse_mass = 7 * S_wetted_fuse

    print(fuse_mass)

    subtotal = fuse_mass + wing_mass + ht_mass + vt_mass + motors_mass * 3 * 1.4 + power_system_mass + payload  # See note 1 for motor weight factor

    TOGM = subtotal / (1 - 0.157)  # TOGM = subtotal + 0.157*TOGM

    return TOGM


if __name__ == "__main__":
    # Using C-182 Values for reference areas to test
    S_exposed = 16.2  # m^2
    S_wetted = 26.94  # m^2
    motors_mass = 16.5  # kg
    power_system_mass = 168  # kg
    payload = 100 * 3  # kg

    print("\n Testing Weight Estimate Function \n")
    TOGM = mass_estimate(S_exposed, S_wetted, motors_mass, power_system_mass, payload)
    print("\t Estimated Aircraft Weight", TOGM)

    rows, cols = (5, 2)
    T_W = [[0 for i in range(cols)] for j in range(rows)]

    a = [[1,2], [3,4], [5,6]]
    print(a[0][0])
