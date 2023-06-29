def time_to_energy(path_to_folder, path_to_mass_file):
    
    
    import pandas as pd
    import os
    
    """
            The function takes as input a path to a folder containing files with data on certain ions and a path to the file with ions masses of elements.
            Data files contain information about time registration of ions and the magnitude of the analyzer signal.
            The function reads the data and adds it to the resulting table after some processing.
        
            A resulting table contains next columns:
                1. time registration of ions
                2. magnitude of the analyzer signal
                3. type of ion
                4. target material
                5. ions energy
    """
    
    # parameters and constants
    m_proton = 1.67e-27
    tube_length = 4.5
    
    # create DataFrame with ion's elements
    elements = pd.read_csv(path_to_mass_file)
    
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
    
    # add column with name of ion's element
    df['element'] = df.ion.apply(lambda x: ''.join([i for i in x.split('+')[0] if not i.isdigit()]))
    
    # merge df with elements
    full = df.merge(elements, how='inner', on='element')
    
    # add column with ion's velocity
    full['velocity'] = tube_length / (full['time'] / 1e6)
    
    # add column with ion's energy
    full['energy'] = pow(full['velocity'], 2) * full['number'] * m_proton / (2 * 1.6e-19)
    
    
    return full