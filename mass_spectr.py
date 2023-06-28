def spectr_to_frame(path_to_folder):
    
    import pandas as pd
    import os
    
    """
            The function takes as input a path to a folder containing files with data on certain ions. Data files contain information about time 
        registration of ions and the magnitude of the analyzer signal. A function reads the data and adds it to the resulting table after some processing.
        
            A resulting table contains next columns:
                1. time registration of ions
                2. magnitude of the analyzer signal
                3. type of ion
                4. target material
    """
    
    # create an empty DataFrame
    df = pd.DataFrame()
    
    for add, dirs, files in os.walk(path_to_folder):
        for file in files:
            temp_df = pd.read_csv(os.path.join(add,file), sep=r'\s{2,}',
                                              engine='python', header=None)

            # rename columns
            temp_df.rename(columns={0:'n_ions', 1:'time'}, inplace=True)

            # sort data by time
            temp_df = temp_df.sort_values('time', ascending=False).reset_index(drop=True)

            # replace negative values with nulls
            temp_df[temp_df < 0] = 0

            # use coefficient 2 to correct data
            temp_df['n_ions'] = temp_df['n_ions'] * 2

            # add column with ion name
            temp_df['ion'] = file.split('.')[0]

            # add column with target name
            temp_df['target'] = add.split('/')[-1]

            # add data to final dataframe
            df = pd.concat([df, temp_df])

    # sort final dataframe    
    df.sort_values(['target', 'ion', 'time'], ascending=[True, True, False], inplace=True)
    df = df.reset_index(drop=True)
    
    return df