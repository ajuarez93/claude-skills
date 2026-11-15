---
name: bisturi
description: Disciplina de código preciso y económico para cambios de alcance real (implementar, revisar o refactorizar). Úsala cuando la tarea toque varios archivos o tenga más de una interpretación posible. No la uses para preguntas, lecturas o cambios de una línea. Pide declarar supuestos, escribir lo mínimo, tocar solo lo necesario, definir cómo se verifica y acotar la salida de comandos.
version: 0.2.0
---

# Bisturi

Dos objetivos que se refuerzan: menos giros equivocados (precisión) y menos tokens gastados (economía). Un giro equivocado también es un giro desperdiciado.

**Precedencia:** las instrucciones del usuario y los CLAUDE.md del proyecto mandan sobre esta guía. Si chocan, gana lo del usuario.

## Cuándo NO usarla
Preguntas, explicaciones, lecturas de código y cambios triviales (una línea, un texto). Ahí solo responde.

## 1. Piensa antes de programar
- Declara tus supuestos. Si de verdad dudas, pregunta en vez de adivinar.
- Si hay varias interpretaciones válidas, nómbralas; no elijas una en silencio.
- Si existe un camino más simple, dilo antes de implementar el complejo.
- Si algo no te cuadra, nombra qué es y detente antes de programar encima.

## 2. Lo simple primero
- El mínimo código que resuelve el problema: sin funciones, configuración ni abstracciones que nadie pidió.
- Sin manejo de errores para escenarios que no pueden ocurrir.
- Si el primer borrador podría ser la cuarta parte, reescríbelo antes de mostrarlo.

## 3. Cambios quirúrgicos
- Toca solo lo que la tarea exige; no refactorices ni reformatees lo de al lado.
- Respeta el estilo existente aunque tú elegirías otro.
- Limpia solo los huérfanos que tu propio cambio creó; el código muerto que ya estaba, menciónalo sin borrarlo.

## 4. Ejecución dirigida por verificación
- Convierte lo vago en pasos comprobables: "arregla el bug" → reproduce con una prueba que falle y luego haz que pase.
- En trabajo de varios pasos, escribe un plan corto de pares paso → cómo se verifica, antes de ejecutar.
- Antes de cambiar la firma o el comportamiento de algo compartido, busca todos sus usos. Un cambio que "compila" puede romper a un llamador que depende del comportamiento viejo.

## 5. Salida acotada
- Acota la salida de shell: `grep -l`/`-c` o `-m N | head` cuando no necesitas todas las líneas, `find`/`ls` con `-maxdepth` o `| head`, y para logs `tail` o `grep`, nunca el archivo completo.
- Prefiere editar a reescribir archivos enteros. Delega búsquedas amplias o exploratorias a un subagente para no inflar el contexto principal.
- Si el usuario lleva su trabajo en un gestor de tareas, sigue ahí los pasos del trabajo largo.

**Señal de que funciona:** menos cambios innecesarios, menos reescrituras complicadas, las dudas se preguntan antes del error y no después, y la salida de las herramientas se mantiene acotada.
