# pylint: disable=import-outside-toplevel

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requisitos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minúsculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """

    import pandas as pd
    import re

    # 1. Leer todas las líneas del archivo
    ruta = 'files/input/clusters_report.txt'
    with open(ruta, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 2. Detectar la línea separadora de cabecera (la que contiene muchos guiones)
    header_end = None
    for i, line in enumerate(lines):
        if line.strip().startswith('-'):
            header_end = i
            break
    if header_end is None:
        raise ValueError("No encontré la línea separadora de cabecera en el archivo")

    # 3. A partir de la siguiente línea, acumulamos los bloques de cada cluster
    data_lines = lines[header_end + 1:]
    blocks = []
    current = ''
    for ln in data_lines:
        if ln.strip() == '':
            continue
        if re.match(r'^\s*\d+', ln):
            # nueva entrada
            if current:
                blocks.append(current.strip())
            current = ln.strip()
        else:
            # continuación de la línea anterior
            current += ' ' + ln.strip()
    if current:
        blocks.append(current.strip())

    # 4. Parsear cada bloque con regex y normalizar
    clusters = []
    counts = []
    percents = []
    keywords = []

    for blk in blocks:
        # colapsar espacios múltiples
        norm = ' '.join(blk.split())
        # extraer: número, cantidad, porcentaje y resto
        m = re.match(r'^(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)$', norm)
        if not m:
            # por si el % viene pegado
            m = re.match(r'^(\d+)\s+(\d+)\s+([\d,]+)%\s+(.*)$', norm)
        if not m:
            raise ValueError(f"No pude parsear el bloque:\n{norm}")

        cluster_id = int(m.group(1))
        cantidad = int(m.group(2))
        porcentaje = float(m.group(3).replace(',', '.'))
        kw = m.group(4).rstrip('.')  # quitar punto final si existe

        # asegurar un único espacio tras cada coma
        parts = [p.strip() for p in kw.split(',') if p.strip()]
        kw_clean = ', '.join(parts)

        clusters.append(cluster_id)
        counts.append(cantidad)
        percents.append(porcentaje)
        keywords.append(kw_clean)

    # 5. Armar el DataFrame
    df = pd.DataFrame({
        'cluster': clusters,
        'cantidad_de_palabras_clave': counts,
        'porcentaje_de_palabras_clave': percents,
        'principales_palabras_clave': keywords
    })

    return df
