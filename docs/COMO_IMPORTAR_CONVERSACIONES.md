# Cómo Agregar Conversaciones de ChatGPT al Agente

## Opción 1: Crear un Documento Adicional (Recomendado)

1. Crea el archivo `docs/04_contexto_psicologico.md`
2. Pega el contenido relevante de tu conversación con ChatGPT
3. Modifica `app/agent_service.py` para incluirlo

### Ejemplo de `04_contexto_psicologico.md`:

```markdown
# Contexto Psicológico y Patrones del Usuario

## Temas Recurrentes
- Tendencia al sobrecontrol
- Ansiedad por dispersión
- etc...

## Decisiones Clave del Pasado
[Tu contenido aquí]
```

### Modificación en `agent_service.py`:

Línea 13-17, agrega:
```python
DOC_FILES = {
    'doc1': '01_mapa_estrategico_2026.md',
    'doc2': '02_manual_operativo_diario.md',
    'doc3': '03_bitacora_ajustes.md',
    'doc4': '04_contexto_psicologico.md'  # <-- NUEVO
}
```

## Opción 2: Editar el Historial Directamente

1. Abre `docs/chat_history.json`
2. Agrega entradas en este formato:

```json
[
  {"role": "user", "content": "Tu pregunta..."},
  {"role": "assistant", "content": "Respuesta del agente..."}
]
```

**⚠️ Advertencia**: Esta opción puede confundir al agente si las entradas no siguen el tono "sobrio" del sistema.

## Recomendación

Usa **Opción 1** y crea un documento separado con:
- Solo lo MÁS relevante de la conversación
- Patrones emocionales/psicológicos (no técnicos)
- Formulado como "contexto", no como "instrucciones"
