import os
import json
import urllib.request
import urllib.error
from system_prompt import SYSTEM_PROMPT
import data_service

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
HISTORY_FILE = os.path.join(DOCS_DIR, 'chat_history.json')

DOC_FILES = {
    'doc1': '01_mapa_estrategico_2026.md',
    'doc2': '02_manual_operativo_diario.md',
    'doc3': '03_bitacora_ajustes.md',
    'doc4': '04_contexto_psicologico.md'
}

def load_document_content():
    """Loads all documents + current dynamic state to provide full context."""
    context = ""
    
    # Load static documents
    for name, filename in DOC_FILES.items():
        path = os.path.join(DOCS_DIR, filename)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                context += f"\n\n--- CONTENIDO DE {name.upper()} ({filename}) ---\n"
                context += f.read()
    
    # Load dynamic state
    state = data_service.get_home_state()
    context += "\n\n--- ESTADO ACTUAL DEL SISTEMA (DINÁMICO) ---\n"
    
    if state['plan_diario']:
        context += f"\n**Plan Diario Activo:**\n"
        context += f"- Timestamp: {state['plan_diario']['timestamp']}\n"
        if state['plan_diario'].get('obligaciones'):
            context += f"- Obligaciones: {state['plan_diario']['obligaciones']}\n"
        if state['plan_diario'].get('tarea_ancla'):
            horizonte = state['plan_diario'].get('horizonte_tarea_ancla', '')
            ancla_full = f"{state['plan_diario']['tarea_ancla']} (Horizonte: {horizonte})" if horizonte else state['plan_diario']['tarea_ancla']
            context += f"- Tarea Ancla: {ancla_full}\n"
        if state['plan_diario'].get('resto_dia'):
            context += f"- Espacio Reactivo: {state['plan_diario']['resto_dia']}\n"
    else:
        context += "\n**Plan Diario:** No hay plan diario activo.\n"
    
    if state['inventario']:
        context += f"\n**Inventario Semanal:**\n"
        context += f"- Timestamp: {state['inventario']['timestamp']}\n"
        if state['inventario'].get('energia'):
            context += f"- Energía/Estado: {state['inventario']['energia']}\n"
        if state['inventario'].get('focos_activos'):
            context += f"- 🔴 Focos Activos (Capa 2): {state['inventario']['focos_activos']}\n"
        if state['inventario'].get('mantenimiento'):
            context += f"- 🟢 Mantenimiento (Capa 1): {state['inventario']['mantenimiento']}\n"
        if state['inventario'].get('semillas'):
            context += f"- 🔵 Semillas/Latentes (Capa 3): {state['inventario']['semillas']}\n"
    else:
        context += "\n**Inventario Semanal:** No hay inventario reciente.\n"
    
    if state['ultimo_ajuste']:
        context += f"\n**Último Ajuste Registrado:**\n"
        context += f"- Timestamp: {state['ultimo_ajuste']['timestamp']}\n"
        context += f"- Tipo: {state['ultimo_ajuste']['tipo']}\n"
        context += f"- Qué cambió: {state['ultimo_ajuste']['que_cambio']}\n"
        context += f"- Por qué: {state['ultimo_ajuste']['por_que']}\n"
    else:
        context += "\n**Bitácora:** No hay ajustes registrados.\n"
    
    return context

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def call_gemini_api(messages):
    """Calls Google Gemini API using standard library to avoid deps."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: No GEMINI_API_KEY found in environment variables."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"
    
    # Format content for Gemini
    # Gemini expects: {"contents": [{"role": "user", "parts": [{"text": "..."}]}]}
    # We need to prepend system prompt as a user message or system instruction if supported.
    # Flash 2.0 supports system_instruction, but for simplicity with v1beta endpoint structure
    # we can often just prepend it to the first user message or use system_instruction field.
    
    system_instruction = {"role": "model", "parts": [{"text": "Entendido. Operaré bajo esas reglas estrictas."}]} 
    # Actually, proper way for rest api: 
    # payload = { "system_instruction": { "parts": { "text": ... } }, "contents": [...] }
    
    contents = []
    for msg in messages:
        role = "user" if msg['role'] == 'user' else "model"
        contents.append({
            "role": role,
            "parts": [{"text": msg['content']}]
        })

    payload = {
        "system_instruction": {
            "parts": {"text": SYSTEM_PROMPT + "\n\nCONTEXTO ACTUAL DE DOCUMENTOS:\n" + load_document_content()}
        },
        "contents": contents,
        "generationConfig": {
            "temperature": 0.3, # Low temp for standardized/sober responses
            "maxOutputTokens": 800
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )

    try:
        with urllib.request.urlopen(req) as response:
            result = json.load(response)
            # Parse response
            try:
                answer = result['candidates'][0]['content']['parts'][0]['text']
                return answer
            except (KeyError, IndexError):
                return "Error: Respuesta inválida del modelo."
    except urllib.error.HTTPError as e:
        return f"Error API: {e.code} - {e.read().decode('utf-8')}"
    except Exception as e:
        return f"Error inesperado: {str(e)}"

def process_user_message(user_text):
    history = load_history()
    
    # Add user message
    history.append({"role": "user", "content": user_text})
    
    # Get response
    # We construct a limited history window for context if needed, but let's send full relevant history
    # Caution with token limits, but for text files it should be okay.
    response_text = call_gemini_api(history)
    
    # Append model response
    history.append({"role": "assistant", "content": response_text})
    
    # Save
    save_history(history)
    
    return response_text
