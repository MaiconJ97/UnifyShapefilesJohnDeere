import os
import json
import geopandas as gpd
import pandas as pd

# Parameters
input_dir = r'path/to/your/files'
output_dir = f'{input_dir}/unificados'

# Obtener archivos SHP y JSON
shp_files = [f for f in os.listdir(input_dir) if f.endswith('.shp')]
json_files = {f.replace('.json', ''): f for f in os.listdir(
    input_dir) if f.endswith('.json')}

# Crear carpeta de salida si no existe
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Carpeta creada: {output_dir}")

# Agrupar archivos
shp_groups = {}
for shp in shp_files:
    try:
        parts = shp.split('_')
        if len(parts) < 4:
            print(f"Archivo {shp} no sigue el formato esperado")
            continue

        cliente, organizacion, area, trabajo = parts[:4]
        group_name = f"{cliente}_{organizacion}_{area}_{trabajo}"

        if group_name not in shp_groups:
            shp_groups[group_name] = []

        shp_groups[group_name].append(shp)
    except Exception as e:
        print(f"Error procesando {shp}: {str(e)}")
        continue

# Procesar cada grupo
for group_name, group_files in shp_groups.items():
    try:
        output_file = os.path.join(output_dir, f"{group_name}.gpkg")
        gdfs = []

        for shp_file in group_files:
            try:
                # Leer shapefile
                shp_path = os.path.join(input_dir, shp_file)
                gdf = gpd.read_file(shp_path)

                # Buscar JSON correspondiente
                base_name = shp_file.replace('.shp', '')
                json_file = None

                for json_key in json_files.keys():
                    if json_key.startswith(base_name):
                        json_file = json_files[json_key]
                        break

                # Si existe JSON, agregar info de máquina
                if json_file and 'Machine' in gdf.columns:
                    json_path = os.path.join(input_dir, json_file)
                    with open(json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # Extraer info de máquinas
                    machine_usage = data.get('MachineUsage', {})

                    # Crear función para mapear Machine ID a Serial y Operador
                    def get_machine_serial(machine_id):
                        machine_id_str = str(int(machine_id)) if pd.notna(
                            machine_id) and machine_id != 0 else '0'
                        return machine_usage.get(machine_id_str, {}).get('MachineSerial', '')

                    def get_operator_name(machine_id):
                        machine_id_str = str(int(machine_id)) if pd.notna(
                            machine_id) and machine_id != 0 else '0'
                        return machine_usage.get(machine_id_str, {}).get('OperatorName', '')

                    # Agregar columnas basadas en Machine ID
                    gdf['MachineSerial'] = gdf['Machine'].apply(
                        get_machine_serial)
                    gdf['OperatorName'] = gdf['Machine'].apply(
                        get_operator_name)

                gdfs.append(gdf)

            except Exception as e:
                print(f"Error leyendo {shp_file}: {str(e)}")
                continue

        # Combinar y guardar
        if gdfs:
            combined_gdf = pd.concat(gdfs, ignore_index=True)
            combined_gdf = gpd.GeoDataFrame(combined_gdf, geometry='geometry')
            combined_gdf.to_file(output_file, driver='GPKG')
            print(f"Combinados {len(gdfs)} archivos en {output_file}")
        else:
            print(f"No se pudieron procesar archivos para {group_name}")

    except Exception as e:
        print(f"Error procesando grupo {group_name}: {str(e)}")
        continue

print("\nProceso completado!")
