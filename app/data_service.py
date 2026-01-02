import os
import json
import re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
DATA_DIR = os.path.join(DOCS_DIR, 'data')
BITACORA_PATH = os.path.join(DOCS_DIR, '03_bitacora_ajustes.md')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def parse_bitacora():
    """
    Parse bitácora to extract latest entry.
    Returns dict with: timestamp, tipo, que_cambio, por_que
    """
    if not os.path.exists(BITACORA_PATH):
        return None
    
    with open(BITACORA_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all entries with pattern ## YYYY-MM-DD HH:MM
    entry_pattern = r'## (\d{4}-\d{2}-\d{2} \d{2}:\d{2})'
    entries = list(re.finditer(entry_pattern, content))
    
    if not entries:
        return None
    
    # Get the last entry
    last_entry = entries[-1]
    timestamp_str = last_entry.group(1)
    start_pos = last_entry.end()
    
    # Extract content until next entry or end of file
    if len(entries) > 1:
        # Find where this entry ends (start of next entry, working backwards)
        entry_content = content[start_pos:]
    else:
        entry_content = content[start_pos:]
    
    # Look for next ## to find end of this entry
    next_entry = re.search(r'\n## ', entry_content)
    if next_entry:
        entry_content = entry_content[:next_entry.start()]
    
    # Extract fields
    tipo_match = re.search(r'\*\*Tipo:\*\*\s*(.+?)(?:\n|$)', entry_content)
    que_match = re.search(r'\*\*Qué cambió:\*\*\s*(.+?)(?:\n\*\*|$)', entry_content, re.DOTALL)
    por_que_match = re.search(r'\*\*Por qué:\*\*\s*(.+?)(?:\n\*\*|$)', entry_content, re.DOTALL)
    
    return {
        'timestamp': timestamp_str,
        'tipo': tipo_match.group(1).strip() if tipo_match else 'Sin especificar',
        'que_cambio': que_match.group(1).strip() if que_match else '',
        'por_que': por_que_match.group(1).strip() if por_que_match else ''
    }

def get_latest_plan_diario():
    """Load latest daily plan from JSON storage."""
    plan_path = os.path.join(DATA_DIR, 'latest_plan.json')
    if not os.path.exists(plan_path):
        return None
    
    try:
        with open(plan_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def get_latest_inventario():
    """Load latest weekly inventory from JSON storage."""
    inv_path = os.path.join(DATA_DIR, 'latest_inventario.json')
    if not os.path.exists(inv_path):
        return None
    
    try:
        with open(inv_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def save_plan_diario(obligaciones, tarea_ancla, resto_dia):
    """Persist daily plan to JSON storage."""
    plan_path = os.path.join(DATA_DIR, 'latest_plan.json')
    data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'obligaciones': obligaciones,
        'tarea_ancla': tarea_ancla,
        'resto_dia': resto_dia
    }
    with open(plan_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_inventario(energia, claridad_frentes, ajuste_necesario):
    """Persist weekly inventory to JSON storage."""
    inv_path = os.path.join(DATA_DIR, 'latest_inventario.json')
    data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'energia': energia,
        'claridad_frentes': claridad_frentes,
        'ajuste_necesario': ajuste_necesario
    }
    with open(inv_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def update_obligation_status(item_id, status):
    """Update the status of a specific obligation in the latest plan."""
    plan_path = os.path.join(DATA_DIR, 'latest_plan.json')
    if not os.path.exists(plan_path):
        return False
        
    try:
        with open(plan_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        obligaciones = data.get('obligaciones')
        if not isinstance(obligaciones, list):
            return False
            
        found = False
        for item in obligaciones:
            if item.get('id') == item_id:
                item['estado'] = status
                found = True
                break
        
        if found:
            with open(plan_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        return False
    except Exception as e:
        print(f"Error updating obligation: {e}")
        return False

def get_home_state():
    """
    Aggregate all data for homepage display.
    Returns dict with: plan_diario, inventario, ultimo_ajuste
    """
    return {
        'plan_diario': get_latest_plan_diario(),
        'inventario': get_latest_inventario(),
        'ultimo_ajuste': get_ultimo_ajuste()  # Usar nueva función
    }


# ============================================================================
# Funciones para gestión de ajustes del plan diario
# ============================================================================

def obtener_plan_actual():
    """
    Obtiene el plan diario actual almacenado.
    
    Returns:
        dict: Diccionario con el plan actual, o un dict vacío si no existe
        
    Estructura del plan retornado:
        {
            'timestamp': '2026-01-01 19:00',
            'obligaciones': [...],
            'tarea_ancla': '...',
            'resto_dia': '...'
        }
    """
    plan = get_latest_plan_diario()
    if plan is None:
        return {
            'timestamp': '',
            'obligaciones': [],
            'tarea_ancla': '',
            'resto_dia': ''
        }
    return plan


def actualizar_plan_actual(plan_ajustado):
    """
    Actualiza el plan diario actual con los nuevos datos ajustados.
    
    Args:
        plan_ajustado (dict): Diccionario con las nuevas datos del plan
            Debe contener: obligaciones, tarea_ancla, resto_dia
    
    Returns:
        bool: True si se guardó correctamente, False en caso contrario
    """
    try:
        plan_path = os.path.join(DATA_DIR, 'latest_plan.json')
        data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'obligaciones': plan_ajustado.get('obligaciones', []),
            'tarea_ancla': plan_ajustado.get('tarea_ancla', ''),
            'resto_dia': plan_ajustado.get('resto_dia', '')
        }
        with open(plan_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error actualizando plan actual: {e}")
        return False


def guardar_ajuste_plan(que_cambio, por_que, plan_original, plan_ajustado):
    """
    Registra un ajuste del plan diario en los archivos del sistema.
    
    Esta función:
    1. Guarda el ajuste en ultimo_ajuste.json para el dashboard
    2. Añade una entrada en la bitácora markdown
    
    Args:
        que_cambio (str): Descripción de los cambios realizados (con formato HTML o markdown)
        por_que (str): Razón proporcionada por el usuario para el ajuste
        plan_original (dict): Plan antes del ajuste
        plan_ajustado (dict): Plan después del ajuste
    
    Returns:
        bool: True si se guardó correctamente, False en caso contrario
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # 1. Guardar en ultimo_ajuste.json para el dashboard
    try:
        ajuste_path = os.path.join(DATA_DIR, 'ultimo_ajuste.json')
        ajuste_data = {
            'timestamp': timestamp,
            'tipo': 'Plan Diario — Ajuste',
            'que_cambio': que_cambio,
            'por_que': por_que
        }
        with open(ajuste_path, 'w', encoding='utf-8') as f:
            json.dump(ajuste_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error guardando ultimo_ajuste.json: {e}")
        return False
    
    # 2. Añadir entrada en bitácora markdown
    try:
        agregar_entrada_bitacora_ajuste(
            timestamp=timestamp,
            cambios=que_cambio,
            razon=por_que,
            plan_resultante=plan_ajustado
        )
    except Exception as e:
        print(f"Error añadiendo entrada a bitácora: {e}")
        return False
    
    return True


def agregar_entrada_bitacora_ajuste(timestamp, cambios, razon, plan_resultante):
    """
    Añade una entrada de ajuste de plan a la bitácora markdown.
    
    Args:
        timestamp (str): Marca temporal del ajuste
        cambios (str): Descripción de los cambios (formato markdown)
        razon (str): Razón del ajuste proporcionada por el usuario
        plan_resultante (dict): Plan después del ajuste
    """
    # Formatear obligaciones para la bitácora
    obligaciones_md = ""
    obligaciones = plan_resultante.get('obligaciones', [])
    
    if isinstance(obligaciones, list) and obligaciones:
        for obl in obligaciones:
            if obl.get('tipo') == 'registrable':
                estado = '☑' if obl.get('estado') == 'hecho' else '☐'
                obligaciones_md += f"- {estado} {obl.get('texto', '')} (Registrable)\n"
            else:
                obligaciones_md += f"  - {obl.get('texto', '')} (Contexto)\n"
    else:
        obligaciones_md = "- (Ninguna)\n"
    
    # Formatear tarea estructural
    tarea_ancla = plan_resultante.get('tarea_ancla', '').strip()
    tarea_md = tarea_ancla if tarea_ancla else "(Ninguna)"
    
    # Formatear espacio reactivo
    resto_dia = plan_resultante.get('resto_dia', '').strip()
    reactivo_md = resto_dia if resto_dia else "(Sin especificar)"
    
    # Construir entrada markdown
    entrada = f"""
## {timestamp} — Plan Diario (Ajuste)

**Tipo:** Plan Diario — Ajuste

**Qué cambió:**
{cambios}

**Por qué:**
{razon}

**Plan resultante:**

*Obligaciones*
{obligaciones_md}
*Estructural*
{tarea_md}

*Reactivo/Libre*
{reactivo_md}

---

"""
    
    # Añadir al archivo de bitácora
    with open(BITACORA_PATH, 'a', encoding='utf-8') as f:
        f.write(entrada)


def get_ultimo_ajuste():
    """
    Obtiene el último ajuste registrado para mostrar en el dashboard.
    
    Returns:
        dict: Diccionario con el último ajuste, o None si no existe
        
    Estructura retornada:
        {
            'timestamp': '2026-01-01 19:00',
            'tipo': 'Plan Diario — Ajuste',
            'que_cambio': '...',
            'por_que': '...'
        }
    """
    ajuste_path = os.path.join(DATA_DIR, 'ultimo_ajuste.json')
    
    if not os.path.exists(ajuste_path):
        # Intentar parsear de la bitácora como fallback
        return parse_bitacora()
    
    try:
        with open(ajuste_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        # Si falla, intentar parsear de la bitácora
        return parse_bitacora()


# ============================================================================
# Funciones para visualización de bitácora
# ============================================================================

def obtener_entradas_bitacora_estructuradas():
    """
    Parsea el archivo de bitácora y retorna todas las entradas estructuradas.
    
    Returns:
        list: Lista de diccionarios con entradas ordenadas (más reciente primero)
        
    Estructura de cada entrada:
        {
            'timestamp': '2026-01-01 19:17',
            'tipo': 'Plan Diario — Ajuste',
            'campos': {
                'que_cambio': '...',
                'por_que': '...',
                'contenido': '...',
                # ... otros campos según el tipo
            },
            'contenido_completo': '...'  # Para búsqueda
        }
    """
    if not os.path.exists(BITACORA_PATH):
        return []
    
    with open(BITACORA_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Encontrar todas las entradas con pattern ## YYYY-MM-DD HH:MM
    entry_pattern = r'## (\d{4}-\d{2}-\d{2} \d{2}:\d{2})(.*?)(?=\n## \d{4}-\d{2}-\d{2}|\Z)'
    matches = list(re.finditer(entry_pattern, content, re.DOTALL))
    
    entradas = []
    
    for match in matches:
        timestamp = match.group(1).strip()
        entry_content = match.group(2).strip()
        
        # Extraer campos comunes
        tipo_match = re.search(r'\*\*Tipo:\*\*\s*(.+?)(?:\n|$)', entry_content)
        tipo = tipo_match.group(1).strip() if tipo_match else 'Sin especificar'
        
        # Extraer todos los campos posibles
        campos = {}
        
        # Campos para ajustes de plan
        que_cambio_match = re.search(r'\*\*Qué cambió:\*\*\s*(.+?)(?:\n\*\*|\n\n|\Z)', entry_content, re.DOTALL)
        if que_cambio_match:
            campos['que_cambio'] = que_cambio_match.group(1).strip()
        
        por_que_match = re.search(r'\*\*Por qué:\*\*\s*(.+?)(?:\n\*\*|\n\n|\Z)', entry_content, re.DOTALL)
        if por_que_match:
            campos['por_que'] = por_que_match.group(1).strip()
        
        plan_resultante_match = re.search(r'\*\*Plan resultante:\*\*\s*(.+?)(?:\n---|\Z)', entry_content, re.DOTALL)
        if plan_resultante_match:
            campos['plan_resultante'] = plan_resultante_match.group(1).strip()
        
        # Campos para inventario semanal
        energia_match = re.search(r'\*\*Energía/Estado:\*\*\s*(.+?)(?:\n\*\*|\n\n|\Z)', entry_content, re.DOTALL)
        if energia_match:
            campos['energia'] = energia_match.group(1).strip()
        
        claridad_match = re.search(r'\*\*Claridad de Frentes:\*\*\s*(.+?)(?:\n\*\*|\n\n|\Z)', entry_content, re.DOTALL)
        if claridad_match:
            campos['claridad_frentes'] = claridad_match.group(1).strip()
        
        ajuste_match = re.search(r'\*\*Ajuste Necesario:\*\*\s*(.+?)(?:\n\*\*|\n\n|\Z)', entry_content, re.DOTALL)
        if ajuste_match:
            campos['ajuste_necesario'] = ajuste_match.group(1).strip()
        
        # Campos para plan diario
        contenido_match = re.search(r'\*\*Contenido:\*\*\s*(.+?)(?:\n\*\*|\n\n|\Z)', entry_content, re.DOTALL)
        if contenido_match:
            campos['contenido'] = contenido_match.group(1).strip()
        
        # Crear entrada estructurada
        entrada = {
            'timestamp': timestamp,
            'tipo': tipo,
            'campos': campos,
            'contenido_completo': entry_content.lower()  # Para búsqueda
        }
        
        entradas.append(entrada)
    
    # Retornar en orden inverso (más reciente primero)
    return list(reversed(entradas))

