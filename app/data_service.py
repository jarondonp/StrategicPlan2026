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

def get_home_state():
    """
    Aggregate all data for homepage display.
    Returns dict with: plan_diario, inventario, ultimo_ajuste
    """
    return {
        'plan_diario': get_latest_plan_diario(),
        'inventario': get_latest_inventario(),
        'ultimo_ajuste': parse_bitacora()
    }
