import csv
import random

# Valores disponibles para loc_id_arrays
loc_ids = ['CLIN-4', 'CLIN-5', 'CLIN-52', 'CLIN-53']

# Leer el archivo original
input_file = 'internacional.csv'
output_file = 'internacional_clean.csv'

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    
    reader = csv.DictReader(infile, delimiter=',')
    
    # Obtener los nombres de las columnas originales
    fieldnames = reader.fieldnames.copy()
    # Agregar la nueva columna al final
    fieldnames.append('loc_id_arrays')
    
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=',')
    writer.writeheader()
    
    for row in reader:
        # Seleccionar aleatoriamente entre 1 y 2 valores (menos de 3)
        num_values = random.randint(1, 2)
        selected_ids = random.sample(loc_ids, num_values)
        
        # Formatear como array string
        row['loc_id_arrays'] = str(selected_ids).replace("'", "'")
        
        writer.writerow(row)

print(f"Archivo {output_file} creado exitosamente con la columna loc_id_arrays agregada.")
