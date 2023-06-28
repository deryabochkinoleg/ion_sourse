def signal_to_frame(path_to_folder):

    import os
    import pandas as pd

    
    """ 
            The function takes as input a path to a folder containing files with data on certain elements. Data files contain information about time 
        registration of all ions and the magnitude of the collector signal. A function reads the data and adds it to the resulting table after
        some processing.
        
            A resulting table contains next columns:
                1. time - signal registration time
                2. signal - magnitude of the collector signal
                3. element - type of material ions of which are being exploring
    """
    
    # signal_to-current conversion factor 
    k = 1/2048 * 1/29 

    df_col = pd.DataFrame()

    for adds, dirs, files in os.walk(path_to_folder):
        for file in files:
            df_temp = pd.read_csv(os.path.join(adds, file),
                     header=None)
            df_temp = df_temp[0].str.split(expand=True)

            df_temp.drop(columns=[0], inplace=True)

            df_temp.rename(columns={1: 'signal'}, inplace=True)

            df_temp['signal'] = df_temp['signal'].astype('int')

            # move signal to zero point
            df_temp['signal'] = df_temp['signal'] - df_temp['signal'].loc[len(df_temp) - 1000:].mean()

            # convert signal to current
            df_temp['signal'] = k * df_temp['signal'] / 5

            df_temp['element'] = adds.split('/')[-1]

            df_temp['time'] = df_temp.index * 0.000000025  

            df_col = pd.concat([df_col, df_temp])  
            
    df_col = df_col.sort_values(['element', 'time'], ascending=[True, True])
    df_col = df_col.reset_index(drop=True)

    return df_col
            
       