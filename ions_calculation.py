def number_of_ions(path_to_signal):
    
    from collector import signal_to_frame
    import pandas as pd

    """
        The function takes as input a path to a folder containing files with data on certain elements. Data files contain information about time 
            registration of all ions and the magnitude of the collector signal. Then it counts the number of ions by "Trapezoidal rule".
    """

    df_collector = signal_to_frame(path_to_signal)

    # counting number of ions
    s = 0.0
    for k in range(len(df_collector) - 1):
        s += (df_collector['time'][k+1] - df_collector['time'][k]) * (df_collector['signal'][k+1] + df_collector['signal'][k]) / 2
    
    #calculating the whole charge of ions on collector
    Ne = s/1.6e-19

    # calculating the number of particular ions with destribution obtained fro mass-spectr
    Ni = Ne / (1 * 0.5 + 2 * 0.25 + 3 * 0.185 + 4 * 0.06 + 5 * 0.005)

    number_of_ions = pd.DataFrame({'C+1':Ni * 0.5,
                                'C+2': Ni * 0.25,
                                'C+3':Ni * 0.185,
                                'C+4':Ni * 0.06,
                                'C+5':Ni * 0.005}, index=[0])

    number_of_ions = number_of_ions.T.reset_index().rename(columns={'index': 'ion', 0: 'n_ions'})

    number_of_ions['element'] = number_of_ions['ion'].apply(lambda x: x.split('+')[0])

    return number_of_ions