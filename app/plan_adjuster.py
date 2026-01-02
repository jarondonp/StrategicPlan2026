"""
Módulo para gestionar ajustes del plan diario.

Este módulo contiene la lógica de negocio para:
- Detectar cambios entre el plan original y el plan ajustado
- Validar razones de ajuste proporcionadas por el usuario
- Formatear cambios para visualización y registro en bitácora

Funciones principales:
    - detectar_todos_cambios: Detecta todos los cambios entre dos planes
    - validar_razon_ajuste: Valida que la razón del ajuste sea adecuada
    - formatear_cambios_para_markdown: Formatea cambios para bitácora
"""

import json
from typing import List, Dict, Any, Optional


def detectar_cambios_obligaciones(original: List[Dict], ajustado: List[Dict]) -> List[str]:
    """
    Detecta cambios en la lista de obligaciones entre plan original y ajustado.
    
    Args:
        original: Lista de obligaciones del plan original
        ajustado: Lista de obligaciones del plan ajustado
    
    Returns:
        Lista de strings describiendo los cambios detectados
        
    Ejemplo:
        >>> original = [{"id": "1", "texto": "Reunión 10am", "tipo": "registrable"}]
        >>> ajustado = [{"id": "2", "texto": "Caso urgente", "tipo": "registrable"}]
        >>> detectar_cambios_obligaciones(original, ajustado)
        ["Eliminada obligación: 'Reunión 10am'", "Añadida obligación: 'Caso urgente'"]
    """
    cambios = []
    
    # Convertir a sets de IDs para comparación
    ids_originales = {obl.get('id') for obl in original}
    ids_ajustados = {obl.get('id') for obl in ajustado}
    
    # Detectar obligaciones eliminadas
    ids_eliminados = ids_originales - ids_ajustados
    for obl in original:
        if obl.get('id') in ids_eliminados:
            cambios.append(f"Eliminada obligación: '{obl.get('texto', '')}'")
    
    # Detectar obligaciones añadidas
    ids_nuevos = ids_ajustados - ids_originales
    for obl in ajustado:
        if obl.get('id') in ids_nuevos:
            cambios.append(f"Añadida obligación: '{obl.get('texto', '')}'")
    
    # Detectar obligaciones modificadas (mismo ID, diferente texto o tipo)
    for obl_original in original:
        id_original = obl_original.get('id')
        if id_original in ids_ajustados:
            obl_ajustado = next((o for o in ajustado if o.get('id') == id_original), None)
            if obl_ajustado:
                if obl_original.get('texto') != obl_ajustado.get('texto'):
                    cambios.append(
                        f"Modificada obligación: '{obl_original.get('texto', '')}' → "
                        f"'{obl_ajustado.get('texto', '')}'"
                    )
                if obl_original.get('tipo') != obl_ajustado.get('tipo'):
                    cambios.append(
                        f"Cambiado tipo de '{obl_ajustado.get('texto', '')}': "
                        f"{obl_original.get('tipo', '')} → {obl_ajustado.get('tipo', '')}"
                    )
    
    return cambios


def detectar_cambios_tarea_ancla(original: str, ajustado: str) -> Optional[str]:
    """
    Detecta cambios en la tarea estructural (tarea ancla).
    
    Args:
        original: Texto de la tarea ancla original
        ajustado: Texto de la tarea ancla ajustada
    
    Returns:
        String describiendo el cambio, o None si no hay cambio
        
    Ejemplo:
        >>> detectar_cambios_tarea_ancla("Documentar casos", "")
        "Tarea estructural eliminada (reducción de carga)"
    """
    original = original.strip() if original else ""
    ajustado = ajustado.strip() if ajustado else ""
    
    # Sin cambios
    if original == ajustado:
        return None
    
    # Tarea eliminada
    if original and not ajustado:
        return "Tarea estructural eliminada (reducción de carga)"
    
    # Tarea añadida
    if not original and ajustado:
        return f"Tarea estructural añadida: '{ajustado}'"
    
    # Tarea modificada
    return f"Tarea estructural modificada: '{original}' → '{ajustado}'"


def detectar_cambios_espacio_reactivo(original: str, ajustado: str) -> Optional[str]:
    """
    Detecta cambios en el espacio reactivo/libre.
    
    Args:
        original: Texto del espacio reactivo original
        ajustado: Texto del espacio reactivo ajustado
    
    Returns:
        String describiendo el cambio, o None si no hay cambio
    """
    original = original.strip() if original else ""
    ajustado = ajustado.strip() if ajustado else ""
    
    if original != ajustado:
        return "Espacio reactivo/libre actualizado"
    
    return None


def detectar_todos_cambios(plan_original: Dict[str, Any], plan_ajustado: Dict[str, Any]) -> List[str]:
    """
    Detecta todos los cambios entre el plan original y el plan ajustado.
    
    Esta es la función principal que coordina la detección de cambios
    en todas las secciones del plan diario.
    
    Args:
        plan_original: Diccionario con el plan antes del ajuste
        plan_ajustado: Diccionario con el plan después del ajuste
    
    Returns:
        Lista de strings describiendo todos los cambios detectados
        
    Ejemplo:
        >>> plan_original = {
        ...     "obligaciones": [{"id": "1", "texto": "Reunión", "tipo": "registrable"}],
        ...     "tarea_ancla": "Documentar",
        ...     "resto_dia": "Emails"
        ... }
        >>> plan_ajustado = {
        ...     "obligaciones": [],
        ...     "tarea_ancla": "",
        ...     "resto_dia": "Emails"
        ... }
        >>> cambios = detectar_todos_cambios(plan_original, plan_ajustado)
        >>> len(cambios)
        2
    """
    todos_cambios = []
    
    # Detectar cambios en obligaciones
    obligaciones_original = plan_original.get('obligaciones', [])
    obligaciones_ajustado = plan_ajustado.get('obligaciones', [])
    
    # Si obligaciones es string (formato legacy), convertir a lista vacía
    if isinstance(obligaciones_original, str):
        obligaciones_original = []
    if isinstance(obligaciones_ajustado, str):
        obligaciones_ajustado = []
    
    cambios_obligaciones = detectar_cambios_obligaciones(
        obligaciones_original, 
        obligaciones_ajustado
    )
    todos_cambios.extend(cambios_obligaciones)
    
    # Detectar cambios en tarea ancla
    cambio_tarea = detectar_cambios_tarea_ancla(
        plan_original.get('tarea_ancla', ''),
        plan_ajustado.get('tarea_ancla', '')
    )
    if cambio_tarea:
        todos_cambios.append(cambio_tarea)
    
    # Detectar cambios en espacio reactivo
    cambio_espacio = detectar_cambios_espacio_reactivo(
        plan_original.get('resto_dia', ''),
        plan_ajustado.get('resto_dia', '')
    )
    if cambio_espacio:
        todos_cambios.append(cambio_espacio)
    
    # Si no hay cambios detectados
    if not todos_cambios:
        todos_cambios.append("Sin cambios estructurales detectados")
    
    return todos_cambios


def validar_razon_ajuste(razon: str) -> tuple[bool, Optional[str]]:
    """
    Valida que la razón del ajuste proporcionada sea adecuada.
    
    Criterios de validación:
    - Debe tener al menos 20 caracteres
    - No debe exceder 300 caracteres
    - No debe ser texto genérico como "test", "prueba", etc.
    
    Args:
        razon: Texto de la razón del ajuste proporcionada por el usuario
    
    Returns:
        Tupla (es_valida, mensaje_error)
        - es_valida: True si la razón es válida, False en caso contrario
        - mensaje_error: String con el mensaje de error si no es válida, None si es válida
    
    Ejemplo:
        >>> validar_razon_ajuste("test")
        (False, "La razón debe tener al menos 20 caracteres")
        >>> validar_razon_ajuste("Surgió una tarea urgente del cliente que requiere atención")
        (True, None)
    """
    if not razon or not razon.strip():
        return False, "Debes proporcionar una razón para el ajuste"
    
    razon = razon.strip()
    
    # Validar longitud mínima
    if len(razon) < 20:
        return False, "La razón debe tener al menos 20 caracteres. Sé específico sobre por qué ajustas el plan."
    
    # Validar longitud máxima
    if len(razon) > 300:
        return False, "La razón no debe exceder 300 caracteres. Sé conciso."
    
    # Validar que no sea texto genérico
    razones_invalidas = ['test', 'prueba', 'testing', 'porque sí', 'porque si']
    if razon.lower() in razones_invalidas:
        return False, "Por favor proporciona una razón real y reflexiva para el ajuste"
    
    return True, None


def formatear_cambios_para_markdown(cambios: List[str]) -> str:
    """
    Formatea la lista de cambios como texto markdown para la bitácora.
    
    Args:
        cambios: Lista de strings describiendo los cambios
    
    Returns:
        String formateado con viñetas en markdown
    
    Ejemplo:
        >>> cambios = ["Eliminada obligación: 'Reunión'", "Tarea estructural eliminada"]
        >>> print(formatear_cambios_para_markdown(cambios))
        - Eliminada obligación: 'Reunión'
        - Tarea estructural eliminada
    """
    if not cambios:
        return "- Sin cambios detectados"
    
    return '\n'.join(f"- {cambio}" for cambio in cambios)


def formatear_cambios_para_html(cambios: List[str]) -> str:
    """
    Formatea la lista de cambios como HTML para el dashboard.
    
    Args:
        cambios: Lista de strings describiendo los cambios
    
    Returns:
        String en formato HTML con viñetas
    """
    if not cambios:
        return "<em>Sin cambios detectados</em>"
    
    items = ''.join(f"<li>{cambio}</li>" for cambio in cambios)
    return f"<ul style='margin: 0; padding-left: 1.5rem;'>{items}</ul>"
