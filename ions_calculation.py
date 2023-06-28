def number_of_ions(path_to_signal):
    
    from collector import signal_to_frame
    import pandas as pd

    df_collector = signal_to_frame(path_to_signal)

    s = 0.0
    for k in range(len(df_collector) - 1):
        s += (df_collector['time'][k+1] - df_collector['time'][k]) * (df_collector['signal'][k+1] + df_collector['signal'][k]) / 2

    Ne = s/1.6e-19

    Ni = Ne / (1 * 0.5 + 2 * 0.25 + 3 * 0.185 + 4 * 0.06 + 5 * 0.005)

    number_of_ions = pd.DataFrame({'C+1':Ni * 0.5,
                                'C+2': Ni * 0.25,
                                'C+3':Ni * 0.185,
                                'C+4':Ni * 0.06,
                                'C+5':Ni * 0.005}, index=[0])

    number_of_ions = number_of_ions.T.reset_index().rename(columns={'index': 'ion', 0: 'n_ions'})

    number_of_ions['element'] = number_of_ions['ion'].apply(lambda x: x.split('+')[0])

    return number_of_ions