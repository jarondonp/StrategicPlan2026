# Bitácora de Ajustes del Sistema

Registro Histórico
{: .metadata }

<div class="bitacora-entry">
<span class="bitacora-date">2025-12-26 14:14</span>
<span class="bitacora-type">Plan Diario</span>

**Obligaciones:**
Test 1

**Estructural:**
Test 2

**Libre/Reactivo:**
Test 3
</div>

<div class="bitacora-entry">
<span class="bitacora-date">Registro Inicial</span>
<span class="bitacora-type">Sistema</span>

Inicio del sistema.
</div>


## 2025-12-26 21:03
**Tipo:** Plan Diario
**Contenido:**
**Obligaciones**
Reunion con equipo a las 10am

**Estructural**
Revisar documentacion tecnica

**Reactivo/Libre**
Responder emails pendientes


## 2025-12-26 21:04
**Tipo:** Plan Diario
**Contenido:**
**Obligaciones**


**Estructural**


**Reactivo/Libre**


## 2025-12-26 23:36
**Tipo:** Plan Diario
**Contenido:**
**Obligaciones**
1. Limpiar Bano y comprar cosas minimas de la casa (Aseo, comida, etc)
2. Evaluar si voy a viajar o no a Garzon para pasar fin de ano
3. Cortarme el cabello


**Estructural**
Tarea ancla: Entender flujo de resolucion de casos Hexagon - Flujo completo (Nivle 2. Meta: Hexagon estable). Meta:)

**Reactivo/Libre**
Pensar ideas , escribirlas, expresion creativa en cualquiera de mis areas de interes


## 2025-12-27 14:42
**Tipo:** Plan Diario
**Contenido:**
**Obligaciones**
- [ ] Tarea Registrable 1 (Registrable)
- Nota Contexto 1


**Estructural**


**Reactivo/Libre**



## 2026-01-01 18:08
**Tipo:** Plan Diario
**Contenido:**
**Obligaciones**
- [ ] cerrar casos(2) hexagon WO (Registrable)
- [ ] Completar sql para insert de ultimo WO (Registrable)
- Definir ruta desarrollo para sitema de control financiero
- Completar registro de primeras cuentas  para cerrar mes de diciembre 2025


**Estructural**
documentar llenado de casos remedy a aprtir de ultima reunion con Huber

**Reactivo/Libre**


## 2026-01-01 19:17 — Plan Diario (Ajuste)

**Tipo:** Plan Diario — Ajuste

**Qué cambió:**
<ul style='margin: 0; padding-left: 1.5rem;'><li>Modificada obligación: 'cerrar casos(2) hexagon WO' → 'cerrar casos(2) hexagon WO , columna adicional y fecha null'</li></ul>

**Por qué:**
mayor detalle de las obligaciones para no olvidar de que casos  WO se tratan especificamente

**Plan resultante:**

*Obligaciones*
- ☐ cerrar casos(2) hexagon WO , columna adicional y fecha null (Registrable)
- ☐ Completar sql para insert de ultimo WO (Registrable)
  - Definir ruta desarrollo para sitema de control financiero (Contexto)
  - Completar registro de primeras cuentas  para cerrar mes de diciembre 2025 (Contexto)

*Estructural*
documentar llenado de casos remedy a aprtir de ultima reunion con Huber

*Reactivo/Libre*
(Sin especificar)

---


## 2026-01-01 19:44 — Rediseño Bitácora

**Tipo:** Sistema — Funcionalidades

**Qué cambió:**
- Implementado diseño profesional con tarjetas y colores diferenciados por tipo
- Añadido sistema de filtros interactivos (búsqueda de texto, rango de fechas, tipo de ajuste)
- Invertido orden cronológico (entradas más recientes aparecen primero)
- Creado nuevo tipo de ajuste "Sistema — Funcionalidades" con color rosa/magenta
- Parseo estructurado de bitácora para mejor presentación

**Por qué:**
La bitácora anterior era difícil de leer y navegar. Presentaba todo el markdown sin formato, sin separación visual entre entradas, y mostraba las entradas antiguas primero (requiriendo scroll hasta el final para ver lo último). Necesitábamos una vista profesional que facilitara la búsqueda y comprensión del historial de cambios del sistema.

**Archivos modificados/creados:**
- app/templates/bitacora_viewer.html (nuevo, ~380 líneas)
- app/data_service.py (+95 líneas, función obtener_entradas_bitacora_estructuradas)
- app/server.py (+7 líneas, detección especial para ruta bitácora)

**Funcionalidades:**
1. Tarjetas visuales con colores por tipo: Sistema-Funcionalidades (rosa), Plan Diario-Ajuste (azul), Plan Diario (verde), Inventario Semanal (amarillo), Ajuste Estratégico (morado)
2. Filtro de búsqueda de texto en todo el contenido
3. Filtro por rango de fechas (desde/hasta)
4. Filtro por tipo de ajuste
5. Contador de resultados dinámico
6. Botón limpiar filtros
7. Diseño responsive (móvil y desktop)
8. Efectos hover en tarjetas

---

## 2026-01-02 05:08

**Tipo:** Inventario Semanal — Ajuste

**Energía/Estado:**
Un poco cansado, con hiperactividad en optimizar el sistema para registar avances en 2026, quiza sea un mecanismo de escape como suele ser, porque vengo pasando fin de ano solo y creo que ponerme hacer esto ocupa mi mente y me regula nose si sanamente o no pero lo hace

**Focos Activos:**
🔹 FRENTE A — TRABAJO & SUSTENTO



Cumplir con Hexagon de forma profesional y sostenible

Mantener JR Techno Solutions viva, no perfecta

Ejecutar asesoría de marca sin sobrecarga



❌ NO rediseñar marca

❌ NO lanzar 5 servicios nuevos



🔹 FRENTE B — APRENDIZAJE VIVO



✅ Aprender haciendo, creando, probando

❌ NO acumular cursos

❌ NO planear currículos

**Mantenimiento:**
1. Documentacion y registros de gastos/deudas/suscripciones 

2. Ausencia de un plan financiero claro y estructurado

3. Seguir trabajo terapeutico / encuentro EPE

4. No descuidar tema espiritual: agradecimiento oracion

**Semillas / Latentes:**
🌱 SLS — PRESENCIA MÍNIMA



- Web existe, Discurso existe



- Puede haber: 1 ajuste, 1 texto, 1 reflexión publicada



- NO objetivos, NO cronogramas


## 2026-01-02 09:58
**Tipo:** Plan Diario
**Qué cambió:**
Horizonte: 1-2 días -> 3-5 días
**Contenido:**
**Obligaciones**
- [ ] 🔴 cerrar casos(2) hexagon WO , columna adicional y fecha null
- [ ] 🔴 Completar sql para insert de ultimo WO
- [ ] 🟢 Definir ruta desarrollo para sitema de control financiero
- [ ] 🟢 Completar registro de primeras cuentas  para cerrar mes de diciembre 2025
- [ ] 🟢 Completar y enviar Factura Hexagon Diciembre 2025 - pedir datos


**Estructural**
documentar llenado de casos remedy a aprtir de ultima reunion con Huber

**Reactivo/Libre**

