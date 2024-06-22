def get_table_display(SapModel, TableKey, Group = ''):
    import os
    import pandas as pd
    csv_folder_path = os.getcwd() + r'\csv'
    if not os.path.exists(csv_folder_path):
        os.makedirs(csv_folder_path)
    csv_file_path = os.path.join(csv_folder_path,TableKey+r'.csv')
    SapModel.DatabaseTables.GetTableForDisplayCSVFile(TableKey, '', Group, -1, csv_file_path)
    table = pd.read_csv(csv_file_path)
    os.remove(csv_file_path)
    return table
