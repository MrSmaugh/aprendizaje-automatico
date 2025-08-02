import pandas as pd

#este script solo maneja la limpieza de datos y crea un nuevo archivo.csv para ser utilizado en weka
# Ruta de tu archivo
input_csv_path = '/sports_performance_data - copia- transformado.csv'
input_delimiter = ',' 

# Ruta para el nuevo archivo
output_csv_path = '/sports_performance_data_cleaned_columns-transformadoV2.csv'
output_delimiter = ','

# Lista de columnas a eliminar
#columns_to_drop = ['a1', 'a2', 'a6', 'a7', 'a14', 'a15', 'a16']
columns_to_drop = ['Athlete_ID', 'Athlete_Name', 'Average_Heart_Rate', 'BMI', 'Resting_Heart_Rate', 'Body_Fat_Percentage', 'VO2_Max']


try:
    # 1. Cargar el archivo
    df = pd.read_csv(input_csv_path, delimiter=input_delimiter)
    print(f"Archivo cargado exitosamente. Filas iniciales: {len(df)}")
    print("Columnas iniciales:")
    print(df.columns.tolist())

    # 2. Eliminar las columnas especificadas
    df_processed = df.drop(columns=columns_to_drop, errors='ignore')
    
    print(f"\nColumnas después de la eliminación inicial: {df_processed.columns.tolist()}")
    print(f"Filas después de la eliminación inicial: {len(df_processed)}")
    print("Tipos de datos después de la eliminación de columnas:")
    print(df_processed.info())

    # 3. Contar filas con *cualquier* valor faltante en el DataFrame PROCESADO
    rows_with_any_missing_values = df_processed.isnull().any(axis=1).sum()
    print(f"\nNúmero de filas con al menos un valor faltante (después de eliminar columnas): {rows_with_any_missing_values}")

    # 4. Decisión de eliminación de filas faltantes basadas en un umbral
    if rows_with_any_missing_values > 0:
        print("\nSe han encontrado filas con valores faltantes en las columnas restantes.")
        
        while True:
            try:
                min_missing_for_removal = int(input("¿Cuántos valores faltantes MÍNIMO debe tener una fila para ser eliminada? (ej: 2, 3): "))
                if min_missing_for_removal < 1:
                    print("Por favor, ingresa un número mayor o igual a 1.")
                else:
                    break
            except ValueError:
                print("Entrada inválida. Por favor, ingresa un número entero.")

        # Calcular el umbral para dropna: minimo de valores NO nulos para conservar la fila
        
        num_cols_remaining = len(df_processed.columns)    
        non_null_counts = df_processed.count(axis=1)
        rows_to_keep_mask = df_processed.isnull().sum(axis=1) < min_missing_for_removal
        df_final = df_processed[rows_to_keep_mask].copy()
        rows_removed_due_to_missing = len(df_processed) - len(df_final)
        print(f"Se eliminaron {rows_removed_due_to_missing} filas porque tenían {min_missing_for_removal} o más valores faltantes.")
        print(f"Filas restantes en el DataFrame final: {len(df_final)}")
    else:
        print("\nNo se encontraron filas con valores faltantes en las columnas restantes. El DataFrame ya está limpio.")
        df_final = df_processed # Si no hay faltantes, el DataFrame procesado es el final

    # 5. Generar el nuevo archivo CSV
    df_final.to_csv(output_csv_path, index=False, sep=output_delimiter)
    print(f"\nNuevo archivo CSV generado en: {output_csv_path}")
    print("Primeras 5 filas del nuevo DataFrame:")
    print(df_final.head())
    print(f"Total de datos procesados y guardados: {len(df_final)}")

except FileNotFoundError:
    print(f"Error: El archivo no se encontró en la ruta especificada: {input_csv_path}")
except KeyError as e:
    print(f"Error: Una de las columnas a eliminar no se encontró en el DataFrame. Por favor, verifica los nombres de las columnas en 'columns_to_drop'. Error: {e}")
    # Si 'df' existe, intentar mostrar sus columnas
    if 'df' in locals():
        print(f"Columnas disponibles en el archivo: {df.columns.tolist()}")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")