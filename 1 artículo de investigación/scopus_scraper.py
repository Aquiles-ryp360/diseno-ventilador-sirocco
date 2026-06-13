import requests
import pandas as pd
import os
import time

# Configuración de la API Key de Scopus (Elsevier)
API_KEY = '4b2ef3adefebb726aa0d6188ab697df8'
BASE_URL = 'https://api.elsevier.com/content/search/scopus'
ABSTRACT_URL = 'https://api.elsevier.com/content/abstract/scopus_id/'
SCOPUS_DIRECT_LINK = 'https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp={}&origin=inward'

def search_scopus(query, count=25):
    headers = {
        'X-ELS-APIKey': API_KEY,
        'Accept': 'application/json'
    }
    params = {
        'query': query,
        'count': count,
        'start': 0,
        'field': 'dc:title,dc:creator,prism:coverDate,prism:publicationName,prism:doi,link,openaccess,dc:identifier'
    }
    all_results = []
    
    # Limitar para evitar saturación de la API
    while len(all_results) < 120:
        print(f"Realizando solicitud a Scopus API (start={params['start']})...")
        try:
            response = requests.get(BASE_URL, headers=headers, params=params)
            print(f"Estado de la respuesta: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                new_results = parse_results(data)
                if new_results:
                    all_results.extend(new_results)
                
                # Si los resultados recibidos son menores que el conteo solicitado, no hay más páginas
                if len(new_results) < count:
                    break
                params['start'] += count
            elif response.status_code == 429:
                print("Límite de solicitudes (Rate Limit) alcanzado. Esperando 5 segundos...")
                time.sleep(5)
                continue
            else:
                print(f"Error en Scopus API: {response.status_code}, {response.text}")
                break
        except Exception as e:
            print(f"Excepción ocurrida durante la consulta: {e}")
            break
            
        # Pequeño retardo entre solicitudes consecutivas
        time.sleep(0.5)
        
    return all_results

def parse_results(data):
    if not data:
        return []
        
    entries = data.get('search-results', {}).get('entry', [])
    results = []
    for entry in entries:
        title = entry.get('dc:title')
        authors = entry.get('dc:creator')
        year = entry.get('prism:coverDate', '').split('-')[0]
        publication_name = entry.get('prism:publicationName')
        doi = entry.get('prism:doi')
        link = entry.get('link', [{}])[0].get('@href')
        scopus_id = entry.get('dc:identifier', '').split(':')[-1]
        open_access = entry.get('openaccess')
        
        # Consultar y extraer el Abstract
        abstract_info = get_abstract(scopus_id)
        objective_purpose = abstract_info.get('objective_purpose', 'N/A')
        methodology = abstract_info.get('methodology', 'N/A')
        results_info = abstract_info.get('results', 'N/A')

        # Filtro de Open Access para descargar libremente
        if open_access == '1':
            results.append({
                'Title': title,
                'Author(s)': authors,
                'Year': year,
                'Objective/Purpose': objective_purpose,
                'Methodology': methodology,
                'Results': results_info,
                'DOI': doi,
                'Link': link,
                'ScopusID': scopus_id,
                'Search Link': f"https://api.elsevier.com/content/abstract/scopus_id/{scopus_id}",
                'Direct Link': SCOPUS_DIRECT_LINK.format(scopus_id)
            })
    return results

def get_abstract(scopus_id):
    headers = {
        'X-ELS-APIKey': API_KEY,
        'Accept': 'application/json'
    }
    try:
        response = requests.get(f"{ABSTRACT_URL}{scopus_id}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            coredata = data.get('coredata', {})
            abstract = coredata.get('dc:description', '')

            objective_purpose, methodology, results = extract_info_from_abstract(abstract)
            return {
                'objective_purpose': objective_purpose,
                'methodology': methodology,
                'results': results
            }
        elif response.status_code == 429:
            print("Rate Limit en consulta de Abstract. Esperando...")
            time.sleep(2)
    except Exception as e:
        print(f"Error consultando abstract {scopus_id}: {e}")
        
    return {}

def extract_info_from_abstract(abstract):
    # Por defecto, estructuramos el abstract completo en la columna de objetivo/propósito
    # Se puede extender con procesamiento de lenguaje natural (NLP)
    return abstract, "N/A", "N/A"

if __name__ == "__main__":
    # Consultas optimizadas para el tema: Gemelo Digital en bombas y ventiladores centrífugos
    # Se añade filtro OPENACCESS(1) para garantizar disponibilidad del artículo completo
    queries = [
        'TITLE-ABS-KEY("digital twin" AND "centrifugal pump" AND "energy") AND DOCTYPE(ar) AND OPENACCESS(1)',
        'TITLE-ABS-KEY("digital twin" AND "pump" AND "optimization") AND DOCTYPE(ar) AND OPENACCESS(1)',
        'TITLE-ABS-KEY("digital twin" AND "pump" AND "fault diagnosis") AND DOCTYPE(ar) AND OPENACCESS(1)',
        'TITLE-ABS-KEY("digital twin" AND "pump" AND "predictive maintenance") AND DOCTYPE(ar) AND OPENACCESS(1)',
        'TITLE-ABS-KEY("digital twin" AND "turbomachinery" AND "efficiency") AND DOCTYPE(ar) AND OPENACCESS(1)'
    ]
    
    all_results = []
    
    for query in queries:
        print(f"\nIniciando búsqueda para: {query}")
        results = search_scopus(query, count=25)
        if results:
            all_results.extend(results)
            print(f"Encontrados {len(results)} artículos viables.")
        else:
            print("No se encontraron resultados o hubo un error en esta consulta.")
            
        time.sleep(1) # Pausa entre consultas grandes
    
    # Limitar a los 120 artículos más relevantes
    all_results = all_results[:120]
    
    if all_results:
        df = pd.DataFrame(all_results)
        
        # Ruta de guardado en la carpeta de artículo de investigación
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(script_dir, 'scopus_digital_twin_results.csv')
        
        # Eliminar archivo si ya existe para evitar sobreescritura fallida
        if os.path.exists(output_file):
            try:
                os.remove(output_file)
            except Exception as e:
                print(f"No se pudo eliminar el archivo anterior: {e}")
        
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\nBúsqueda completada exitosamente.")
        print(f"Se exportaron {len(df)} artículos a: {output_file}")
    else:
        print("\nNo se encontraron resultados válidos en ninguna de las consultas.")
