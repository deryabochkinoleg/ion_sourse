def to_frame(path_to_folder):
    
    import pandas as pd
    import os
    
    """Функция принимает на вход путь к папке, содержащей файлы с данными по определенным ионам в сыром виде, и
    после обработки возвращает датафрейм с информацией по типу мишени, типу ионов, времени прихода ионов и их количество """
    
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