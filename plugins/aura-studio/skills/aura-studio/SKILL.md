# Aura Studio — Analizador de Contenido Orgánico de Instagram

Guía completa para analizar el rendimiento de publicaciones orgánicas en Instagram usando la metodología de las **3 Preguntas** (¿Qué pasó? / ¿Por qué pasó? / ¿Qué haremos?) con semáforo de benchmarks (🔴/🟡/🟢).

---

## Flujo principal

```
Token de acceso → Verificación de cuenta → Selección de periodo →
Tipo de contenido → Análisis 3 Preguntas → Desglose por formato (opcional)
```

**Principio fundamental — Automatización primero:** El usuario solo proporciona el token al inicio y selecciona opciones numeradas. Claude maneja todos los scripts, parseo de JSON y cálculos internamente. El usuario nunca edita archivos manualmente.

---

## Tipos de contenido y métricas disponibles

### Imágenes y Carruseles
Fetch único con todos los campos necesarios:
```
reach, likes, comments, shares, saves, total_interactions
```

### Reels
```
views, reach, likes, comments, shares, saves,
total_interactions, ig_reels_avg_watch_time
```
> ⚠️ Nota API 2025: usar `views` (no `impressions`) para Reels. `impressions` fue deprecado para este formato.

### Stories
```
reach, exits, replies, taps_forward, taps_back
```
> Las Stories solo tienen datos disponibles por 24 horas desde su publicación. Después solo queda disponible el reach histórico.

---

## FASE 1 — Obtener acceso

Claude solicita el token de Instagram al usuario y ejecuta silenciosamente la verificación (FASE 0 del CLAUDE.md). Una vez verificado, reporta:

> "Acceso verificado ✓ — Cuenta Business con permisos de lectura de métricas. ¿Avanzamos?"

Si hay algún problema con el token o los permisos, Claude guía al usuario paso a paso para resolverlo antes de continuar.

---

## FASE 2 — Selección de cuenta e información base

Claude ejecuta `fetch_account.py` y presenta al usuario:

- Nombre de la cuenta y @username
- Número de seguidores actuales
- Total de publicaciones
- Tipo de cuenta (Business / Creator)

Si el token tiene acceso a múltiples cuentas (agencias, managers), Claude lista las cuentas numeradas y espera que el usuario elija una.

---

## FASE 3 — Selección de periodo y contenido

Claude pregunta al usuario qué periodo analizar:

1. Últimos 7 días
2. Últimos 14 días
3. Últimos 30 días *(recomendado para tener suficiente muestra)*
4. Últimos 90 días

Luego pregunta qué tipo de contenido analizar:

1. Todo el contenido (imágenes + carruseles + reels)
2. Solo Reels
3. Solo imágenes y carruseles
4. Stories recientes (últimas 24h)

---

## FASE 4 — Obtención de datos e identificación

Claude ejecuta `fetch_media.py` + `fetch_insights.py` y presenta al usuario la lista de publicaciones encontradas con:

- Número, fecha, tipo (REEL / IMAGE / CAROUSEL)
- Primeras palabras del caption (si existe)
- Reach y total_interactions

Antes de mostrar el análisis completo, Claude pregunta:

> "¿Cuál es tu objetivo principal con el contenido orgánico de esta cuenta? Por ejemplo: ganar seguidores, generar tráfico al sitio, posicionarte como referente, vender productos..."

Esto define el contexto del análisis. Si la respuesta es ambigua, Claude asume "engagement y crecimiento de comunidad".

---

## FASE 5 — Análisis con las 3 Preguntas

### Benchmarks por métrica (semáforo LATAM 2025)

#### Engagement Rate general
*(total_interactions / reach × 100)*

| 🟢 Excelente | 🟡 Normal | 🔴 Bajo |
|---|---|---|
| > 5% | 2% – 5% | < 2% |

#### Save Rate
*(saves / reach × 100)*

| 🟢 Excelente | 🟡 Normal | 🔴 Bajo |
|---|---|---|
| > 3% | 1% – 3% | < 1% |

> El save rate es el indicador más fuerte de contenido de valor. Un post que la gente guarda es un post que resolvió algo.

#### Share Rate
*(shares / reach × 100)*

| 🟢 Excelente | 🟡 Normal | 🔴 Bajo |
|---|---|---|
| > 1.5% | 0.5% – 1.5% | < 0.5% |

#### Reach Rate
*(reach / seguidores × 100)*

| 🟢 Excelente | 🟡 Normal | 🔴 Bajo |
|---|---|---|
| > 15% | 7% – 15% | < 7% |

> Un reach rate bajo indica que el algoritmo no está distribuyendo el contenido. Puede ser señal de baja frecuencia de publicación, horarios incorrectos o bajo engagement inicial.

#### Tasa de comentarios
*(comments / reach × 100)*

| 🟢 Excelente | 🟡 Normal | 🔴 Bajo |
|---|---|---|
| > 0.5% | 0.1% – 0.5% | < 0.1% |

---

#### Métricas específicas de Reels

**Reel Avg Watch Time** (segundos vs duración del video)
> Claude debe calcular: `(ig_reels_avg_watch_time / duración_estimada) × 100`
> Si no se dispone de la duración exacta, Claude pregunta al usuario.

| 🟢 Excelente | 🟡 Normal | 🔴 Bajo |
|---|---|---|
| > 50% del video | 25% – 50% | < 25% |

**Views Rate**
*(views / seguidores × 100 — solo para Reels)*

| 🟢 Excelente | 🟡 Normal | 🔴 Bajo |
|---|---|---|
| > 20% | 8% – 20% | < 8% |

> Un Reel puede alcanzar personas que no siguen la cuenta. Views rate > 100% = el Reel llegó a no-seguidores.

---

#### Métricas específicas de Stories

**Exit Rate**
*(exits / reach × 100)*

| 🟢 Excelente | 🟡 Normal | 🔴 Alto |
|---|---|---|
| < 15% | 15% – 35% | > 35% |

**Taps Forward Rate**
*(taps_forward / reach × 100)*

| 🟢 Excelente | 🟡 Normal | 🔴 Alto |
|---|---|---|
| < 20% | 20% – 40% | > 40% |

> Muchos taps forward = el contenido no engancha, la gente lo está saltando.

---

### Estructura del análisis 3 Preguntas

#### ¿Qué pasó?

Presentar en tabla los posts del periodo con sus métricas principales y semáforo:

| Post | Fecha | Tipo | Reach | Eng. Rate | Save Rate | Share Rate | Estado |
|---|---|---|---|---|---|---|---|
| "..." | 15 may | REEL | 4,200 | 6.2% | 3.8% | 1.2% | 🟢 |
| "..." | 12 may | IMAGE | 1,100 | 1.4% | 0.3% | 0.1% | 🔴 |

Luego resumir:
- Total de publicaciones analizadas
- Promedio de reach rate de la cuenta en el periodo
- Promedio de engagement rate
- Post con mejor performance y post con peor performance

#### ¿Por qué pasó?

Diagnosticar basándose en patrones detectados:

**Formato:**
- ¿Qué formato rinde mejor: reels, carruseles o imágenes?
- ¿Hay diferencia significativa de reach entre formatos?

**Timing:**
- ¿Hay días u horas con mejor performance? (si el dato está disponible en el timestamp)

**Contenido:**
- ¿Los posts con mejor save rate tienen algo en común en el caption? (educativos, listas, tutoriales)
- ¿Los posts con mejor share rate son de opinión, humor o inspiración?
- ¿Los reels con mejor watch time son más cortos o más largos?

**Consistencia:**
- ¿Cuántos días hay entre publicaciones? La irregularidad penaliza el alcance.

#### ¿Qué haremos?

Listar recomendaciones priorizadas por impacto, de mayor a menor urgencia:

Ejemplo de formato:
```
🔴 URGENTE
→ [Recomendación concreta basada en los datos]

🟡 IMPORTANTE  
→ [Recomendación]

🟢 POTENCIAR
→ [Lo que ya está funcionando y hay que hacer más]
```

**Importante:** Claude siempre finaliza con esta nota:

> "Estas recomendaciones son un punto de partida basado en los datos. Tú conoces a tu audiencia — combina este análisis con tu intuición sobre qué contenido resuena con tu comunidad."

---

## FASE 6 (opcional) — Desglose por publicación individual

Si el usuario quiere profundizar en un post específico, Claude ejecuta un análisis detallado de esa publicación usando el mismo framework de 3 Preguntas pero a nivel de post individual, comparándolo contra el promedio de la cuenta en el mismo formato.

---

## Advertencia sobre el Efecto Desglose

Al ver métricas individuales de posts, tener en cuenta:

- Un post nuevo (< 48h) aún está en distribución — sus métricas van a cambiar.
- Instagram puede distribuir un post de forma desigual entre seguidores y no-seguidores según el engagement inicial.
- No tomar decisiones de "pausar" un tipo de contenido con menos de 5 publicaciones de muestra del mismo formato.

---

## Créditos

Metodología de las 3 Preguntas adaptada para contenido orgánico de Instagram.  
Plugin desarrollado para la masterclass **Aura Studio** — análisis de contenido orgánico para líderes de marketing en LATAM.
