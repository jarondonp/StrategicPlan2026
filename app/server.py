import os
import datetime
import json
from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
import agent_service
import data_service

app = Flask(__name__)
# ... configuration ...
DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs'))
BITACORA_FILE = os.path.join(DOCS_DIR, '03_bitacora_ajustes.md')

DOC_FILES = {
    'estrategico': '01_mapa_estrategico_2026.md',
    'operativo': '02_manual_operativo_diario.md',
    'bitacora': '03_bitacora_ajustes.md'
}

TITLES = {
    'estrategico': 'Sistema de Planificación Estratégica',
    'operativo': 'Sistema de Gestión Operativa',
    'bitacora': 'Bitácora de Ajustes'
}

@app.route('/')
def index():
    return redirect(url_for('list_docs'))

@app.route('/docs')
def list_docs():
    state = data_service.get_home_state()
    return render_template('home.html', state=state)

@app.route('/docs/<doc_id>')
def view_doc(doc_id):
    if doc_id not in DOC_FILES:
        abort(404)
    
    # Caso especial: Bitácora usa vista estructurada
    if doc_id == 'bitacora':
        entradas = data_service.obtener_entradas_bitacora_estructuradas()
        return render_template('bitacora_viewer.html', entradas=entradas)
    
    # Otros documentos: vista markdown tradicional
    filename = DOC_FILES[doc_id]
    filepath = os.path.join(DOCS_DIR, filename)
    
    if not os.path.exists(filepath):
        content = "Archivo no encontrado."
    else:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
    # Simple formatting: escape HTML, but we will render it inside a <pre> or simple viewer
    # For a bit more niceness without deps, we could do basics, but user asked for "simple".
    # We will pass raw content to template and let template decide (likely <pre> or marked.js if we wanted, 
    # but I'll stick to a simple textarea or pre tag for editing/viewing to avoid complexity).
    # actually, user said "markdown renderizado simple" is preferred.
    # I will try to use `markdown` lib if available, else plain text.
    
    try:
        import markdown
        # Enable extra extensions for better list/table support, and smarty for nice quotes
        # attr_list allows us to add classes like {: .my-class} to elements
        html_content = markdown.markdown(content, extensions=['extra', 'smarty', 'attr_list', 'def_list'])
        is_markdown = True
    except ImportError:
        html_content = content
        is_markdown = False

    return render_template('doc_viewer.html', 
                           title=TITLES.get(doc_id, doc_id), 
                           content=html_content, 
                           is_markdown=is_markdown,
                           doc_id=doc_id)

@app.route('/plantillas')
def plantillas():
    state = data_service.get_home_state()
    return render_template('plantillas.html', inventario=state['inventario'])

@app.route('/bitacora/nueva')
def nueva_bitacora():
    return render_template('bitacora_form.html')

@app.route('/api/guardar', methods=['POST'])
def guardar_entrada():
    tipo = request.form.get('tipo')
    que_cambio = request.form.get('que_cambio')
    por_que = request.form.get('por_que')
    
    # Optional fields for daily/weekly templates
    contenido = request.form.get('contenido')
    obligaciones = request.form.get('obligaciones')
    tarea_ancla = request.form.get('tarea_ancla')
    resto_dia = request.form.get('resto_dia')
    energia = request.form.get('energia')
    claridad_frentes = request.form.get('claridad_frentes')
    ajuste_necesario = request.form.get('ajuste_necesario')
    
    # Save templates to data service if applicable
    if tipo == 'Plan Diario' and obligaciones:
        # Try to parse obligations as JSON if it looks like it
        try:
            if obligaciones.startswith('[') or obligaciones.startswith('{'):
                obligaciones_data = json.loads(obligaciones)
            else:
                obligaciones_data = obligaciones
        except (json.JSONDecodeError, AttributeError):
            obligaciones_data = obligaciones

        data_service.save_plan_diario(obligaciones_data, tarea_ancla or '', resto_dia or '')
    elif tipo == 'Inventario Semanal' and energia:
        data_service.save_inventario(energia, claridad_frentes or '', ajuste_necesario or '')
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    entry = f"\n\n## {timestamp}\n"
    entry += f"**Tipo:** {tipo}\n"
    
    # Different format based on entry type
    if tipo == 'Plan Diario' and contenido:
        # Plan Diario uses structured content
        entry += f"**Contenido:**\n{contenido}\n"
    elif tipo == 'Inventario Semanal':
        # Inventario Semanal uses specific fields
        if energia:
            entry += f"**Energía/Estado:**\n{energia}\n"
        if claridad_frentes:
            entry += f"**Claridad de Frentes:**\n{claridad_frentes}\n"
        if ajuste_necesario:
            entry += f"**Ajuste Necesario:**\n{ajuste_necesario}\n"
    else:
        # Manual adjustments use standard format
        entry += f"**Qué cambió:**\n{que_cambio or ''}\n"
        entry += f"**Por qué:**\n{por_que or ''}\n"

    # Append to bitacora
    try:
        with open(BITACORA_FILE, 'a', encoding='utf-8') as f:
            f.write(entry)
        return render_template('success.html', message="Entrada guardada correctamente.")
    except Exception as e:
        return f"Error al guardar: {e}", 500

@app.route('/api/obligacion/toggle', methods=['POST'])
def toggle_obligation():
    data = request.json
    item_id = data.get('id')
    status = data.get('status') # 'done', 'pending', 'omitted'
    
    if not item_id or not status:
        return jsonify({'error': 'Missing id or status'}), 400
        
    success = data_service.update_obligation_status(item_id, status)
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Item not found'}), 404

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    data = request.json
    user_message = data.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    response = agent_service.process_user_message(user_message)
    return jsonify({'response': response})

@app.route('/api/chat/history', methods=['GET'])
def chat_history():
    history = agent_service.load_history()
    return jsonify(history)


# ============================================================================
# Rutas para edición y ajuste de plan diario
# ============================================================================

@app.route('/editar-plan')
def editar_plan():
    """
    Renderiza el formulario para editar el plan diario actual.
    Pre-carga los datos del plan guardado para permitir su modificación.
    """
    import plan_adjuster  # Import here to avoid circular dependencies
    
    plan_actual = data_service.obtener_plan_actual()
    
    return render_template(
        'editar_plan.html',
        obligaciones=plan_actual.get('obligaciones', []),
        tarea_ancla=plan_actual.get('tarea_ancla', ''),
        resto_dia=plan_actual.get('resto_dia', '')
    )


@app.route('/api/guardar-ajuste-plan', methods=['POST'])
def guardar_ajuste_plan():
    """
    Procesa el formulario de ajuste del plan diario.
    
    Pasos:
    1. Obtiene el plan original (antes del ajuste)
    2. Parsea el nuevo plan desde el formulario
    3. Detecta cambios automáticamente
    4. Valida la razón del ajuste
    5. Guarda el ajuste en bitácora y archivo de datos
    6. Actualiza el plan actual
    7. Redirige al dashboard con mensaje de confirmación
    """
    import plan_adjuster  # Import here to avoid circular dependencies
    
    # 1. Obtener plan original
    plan_original = data_service.obtener_plan_actual()
    
    # 2. Parsear nuevo plan desde formulario
    try:
        obligaciones_json = request.form.get('obligaciones', '[]')
        obligaciones = json.loads(obligaciones_json) if obligaciones_json else []
    except json.JSONDecodeError:
        return "Error: Formato inválido de obligaciones", 400
    
    plan_ajustado = {
        'obligaciones': obligaciones,
        'tarea_ancla': request.form.get('tarea_ancla', '').strip(),
        'resto_dia': request.form.get('resto_dia', '').strip()
    }
    
    # 3. Validar razón del ajuste
    razon = request.form.get('por_que', '').strip()
    es_valida, mensaje_error = plan_adjuster.validar_razon_ajuste(razon)
    
    if not es_valida:
        return f"Error: {mensaje_error}", 400
    
    # 4. Detectar cambios automáticamente
    cambios = plan_adjuster.detectar_todos_cambios(plan_original, plan_ajustado)
    
    # 5. Formatear cambios para diferentes destinos
    cambios_markdown = plan_adjuster.formatear_cambios_para_markdown(cambios)
    cambios_html = plan_adjuster.formatear_cambios_para_html(cambios)
    
    # 6. Guardar ajuste en bitácora y ultimo_ajuste.json
    exito = data_service.guardar_ajuste_plan(
        que_cambio=cambios_html,  # Para dashboard (HTML)
        por_que=razon,
        plan_original=plan_original,
        plan_ajustado=plan_ajustado
    )
    
    if not exito:
        return "Error al guardar el ajuste", 500
    
    # 7. Actualizar plan actual con datos ajustados
    data_service.actualizar_plan_actual(plan_ajustado)
    
    # 8. Redirigir al dashboard con mensaje de confirmación
    return render_template(
        'success.html', 
        message="Plan ajustado correctamente. Recuerda: ajustar está bien, la rigidez no."
    )


if __name__ == '__main__':
    # Local security guardrails
    app.run(host='127.0.0.1', port=8000, debug=True)
