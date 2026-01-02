import random
from datetime import datetime

FRASES_SISTEMA = [
    "Estabilidad antes que optimización",
    "Este sistema no maximiza resultados externos, maximiza sostenibilidad humana",
    "El éxito en 2026 no es cumplir todo, sino: estabilidad sostenida, continuidad sin colapsos, vocación viva sin presión",
    "Si no hay energía: dejar vacío",
    "Hoy sostengo el día, no demuestro nada",
    "No todo lo importante se hace hoy",
    "Mi valor no depende de este día",
    "El día no es un proyecto",
    "No inventar tareas para llenar el día",
    "Las obligaciones de contexto no se tachan. No son tareas, son realidades del día",
    "No todo lo que nace debe crecer. Y no todo lo que crece debe mostrarse",
    "Las tareas ancla NO se reemplazan automáticamente. Puede haber semanas sin tareas ancla activas. Eso es un estado válido",
    "Este sistema no se perfecciona. Se habita",
    "Consultar mientras aprendo no es dependencia, es formación del criterio",
    "La creatividad aquí es expresión, no validación",
    "Nada de lo que hagas hoy debe obligarte a sostenerlo mañana",
    "Si terminas solo el Bloque 1 → el sistema funcionó",
    "Pensar menos en sistemas y más en vivir el día",
    "Solo 1 frente variable puede estar activo a la vez. Los demás quedan en mantenimiento activo, observación o latentes",
    "Solo se ajustan sistemas cuando hay dolor real sostenido",
    "El inventario es observación, no obligación",
    "Muchas cosas del inventario no se ejecutan esa semana. Eso es normal y esperado. No es fracaso, es realismo",
    "Ante la duda, déjalo como nota (no como tarea registrable)",
    "Ajustar está bien, la rigidez no",
    "Antes de añadir algo al sistema, pregúntate: ¿Esto me ayuda a reflexionar y mantener estabilidad, o me presiona a optimizar y medir constantemente?"
]

def obtener_frase_sistema(plan_actual, ultimo_inventario, ultimo_ajuste):
    """
    Selecciona una frase del sistema basada en condiciones del estado actual,
    o retorna una aleatoria si no hay condiciones críticas.
    """
    
    # 1. Detectar estrés por sobrecarga de obligaciones registrables
    obligaciones = plan_actual.get('obligaciones', [])
    # Contar obligacines que son registrables (listas o dicts con 'registrable': True implícito si son checkbox)
    # Asumimos que si está en obligaciones es porque es algo del día.
    if len(obligaciones) > 5:
        return "No todo lo importante se hace hoy"

    # 2. Detectar falta de tarea ancla (Validar si es un estado válido o olvido)
    tarea_ancla = plan_actual.get('tarea_ancla', '')
    if not tarea_ancla:
        return "No tener tarea ancla activa está bien. Puede haber semanas sin tareas ancla. Eso es un estado válido"

    # 3. Detectar si hubo ajuste reciente (flexibilidad)
    if ultimo_ajuste:
        try:
            timestamp_str = ultimo_ajuste.get('timestamp', '')
            # Formato esperado "YYYY-MM-DD HH:MM"
            if timestamp_str:
                fecha_ajuste = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M")
                delta = datetime.now() - fecha_ajuste
                if delta.days < 1: # Ajuste en las últimas 24h
                    return "Ajustar está bien, la rigidez no"
        except (ValueError, TypeError):
            pass # Ignorar errores de parseo de fecha

    # 4. Detectar falta de inventario reciente (> 7 días)
    if ultimo_inventario:
        try:
            timestamp_inv = ultimo_inventario.get('timestamp', '')
            if timestamp_inv:
                fecha_inv = datetime.strptime(timestamp_inv, "%Y-%m-%d %H:%M")
                delta_inv = datetime.now() - fecha_inv
                if delta_inv.days > 7:
                    return "El inventario es observación, no obligación"
        except (ValueError, TypeError):
             pass
    else:
        # Si no hay inventario nunca
        return "El inventario es observación, no obligación"

    # 5. Si no aplica ninguna regla específica, random
    return random.choice(FRASES_SISTEMA)
