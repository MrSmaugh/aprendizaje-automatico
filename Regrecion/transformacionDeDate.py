import pandas as pd

#es script maneja la comvercion de la fecha del dataset
#ruta del .csv
input_csv_path = '/sports_performance_data - copia.csv' 
#salida del archivo
output_csv_path = '/sports_performance_data - copia- transformado2.csv' 

try:
    
    #se le especifica con que se separan las columnas
    df = pd.read_csv(input_csv_path, delimiter=',')
    
    #verifica si la columna Competition_Date existe
    if 'Competition_Date' in df.columns:
        #cambia el formato de las fechas
        df['Competition_Date'] = pd.to_datetime(df['Competition_Date'], errors= 'coerce')
        
        #se extrase solo el año creando el nuevo formato
        df['Competition_Date'] = df ['Competition_Date'].dt.strftime('%Y')
        
        #guarda lo modificado en un nuevo archivo .csv
        df.to_csv(output_csv_path, index=False, sep=',')
        
        print(f"Archivo modificado guardado exitosamente en: {output_csv_path}")
        print("Primeras 5 filas del nuevo DataFRame:")
        print(df.head())
        print(f"Total de datos transformados: {len(df)}")
    else:
        print(f"Error: La columna 'Competition_Date' no se encontró en el archivo CSV. Por favor, verifica el nombre de la columna.")
        print(f"Columnas disponibles: {df.columns.tolist()}")
        
        #por si hay errores
except FileNotFoundError:
    print(f"Error: El archivo no se encontró en la ruta especificada: {input_csv_path}")
except Exception as e:
    print(f"Ocurrió un error: {e}")