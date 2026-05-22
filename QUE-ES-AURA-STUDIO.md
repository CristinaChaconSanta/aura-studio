# ¿Qué es Aura Studio y qué construimos?

Este documento explica en detalle todo lo que se creó, por qué existe cada parte y cómo funciona el plugin completo.

---

## El punto de partida: inspiración en 3Qs

Todo empezó copiando un plugin de GitHub llamado **`felipeverce/3Qs`**, creado por Felipe Vergara.  
Ese plugin conecta Claude Code con la **Meta Marketing API** (la API de anuncios pagados de Facebook/Instagram) y analiza campañas publicitarias usando una metodología llamada las 3 Preguntas:

1. ¿Qué pasó?
2. ¿Por qué pasó?
3. ¿Qué haremos?

Ese plugin es excelente para analizar **campañas de pauta**. El problema: no sirve para analizar **contenido orgánico** (posts normales, reels, stories sin dinero de por medio).

**Aura Studio es la versión orgánica de ese plugin.** Misma metodología, diferente API, diferente enfoque.

---

## ¿Qué hace Aura Studio exactamente?

Aura Studio conecta Claude Code con la **Instagram Graph API** y analiza el rendimiento de tus publicaciones orgánicas: imágenes, carruseles, reels y stories.

Al activarlo, Claude:
1. Verifica tu token de acceso y permisos
2. Trae la información de tu cuenta (seguidores, tipo de cuenta)
3. Lista tus publicaciones recientes
4. Descarga las métricas de cada post
5. Calcula tasas (engagement rate, save rate, share rate, reach rate)
6. Asigna un semáforo 🔴🟡🟢 basado en benchmarks para LATAM
7. Hace el análisis de las 3 Preguntas con recomendaciones concretas

Todo esto **solo leyendo datos**. Nunca escribe, modifica ni publica nada en tu cuenta.

---

## La diferencia clave: Marketing API vs Instagram Graph API

Esto es importante entenderlo porque **son dos APIs completamente distintas**.

| | Meta Marketing API (3Qs) | Instagram Graph API (Aura Studio) |
|---|---|---|
| **Para qué sirve** | Leer y gestionar campañas de pauta | Leer métricas de contenido orgánico |
| **Qué necesita** | Business Manager + cuenta publicitaria | Cuenta Instagram Business o Creator |
| **Riesgo de bloqueo** | Alto si se abusa | Bajo (solo lectura de tu propia cuenta) |
| **Token** | System User Token (complejo de obtener) | Token de usuario largo (más sencillo) |
| **Permisos** | `ads_read`, `business_management` | `instagram_basic`, `instagram_manage_insights` |
| **Métrica de video** | `impressions` | `views` (actualizado 2025) |

---

## ¿Qué métricas mide?

### Para Imágenes y Carruseles
- **Reach** — cuántas personas únicas vieron el post
- **Likes** — me gusta
- **Comments** — comentarios
- **Shares** — veces que se compartió
- **Saves** — veces que se guardó (el indicador más valioso)
- **Total Interactions** — suma de todas las interacciones

### Para Reels
Todo lo anterior más:
- **Views** — reproducciones (reemplazó a `impressions` en la API 2025)
- **Avg Watch Time** — tiempo promedio de reproducción en segundos

### Para Stories
- **Reach** — personas que la vieron
- **Exits** — cuántos cerraron la story
- **Replies** — respuestas directas
- **Taps Forward** — cuántos la saltaron hacia adelante
- **Taps Back** — cuántos retrocedieron a verla de nuevo

---

## El semáforo: benchmarks para LATAM 2025

El semáforo compara cada métrica contra rangos definidos para cuentas en América Latina. Estos no son números inventados — son rangos basados en promedios reales del mercado.

### Engagement Rate *(total_interactions ÷ reach × 100)*
| 🟢 Excelente | 🟡 Normal | 🔴 Bajo |
|---|---|---|
| Mayor a 5% | Entre 2% y 5% | Menor a 2% |

> El engagement rate mide qué tan activa reacciona tu audiencia al ver el contenido.

### Save Rate *(saves ÷ reach × 100)*
| 🟢 Excelente | 🟡 Normal | 🔴 Bajo |
|---|---|---|
| Mayor a 3% | Entre 1% y 3% | Menor a 1% |

> El save rate es el indicador más poderoso de contenido útil. Si alguien guarda un post, significa que lo quiere consultar después — eso es contenido de valor real.

### Share Rate *(shares ÷ reach × 100)*
| 🟢 Excelente | 🟡 Normal | 🔴 Bajo |
|---|---|---|
| Mayor a 1.5% | Entre 0.5% y 1.5% | Menor a 0.5% |

> El share rate indica contenido que la gente quiere que otros vean. Es el mejor amplificador orgánico.

### Reach Rate *(reach ÷ seguidores × 100)*
| 🟢 Excelente | 🟡 Normal | 🔴 Bajo |
|---|---|---|
| Mayor a 15% | Entre 7% y 15% | Menor a 7% |

> El reach rate dice qué porcentaje de tus seguidores realmente vio el post. Un reach rate bajo puede indicar problemas con el algoritmo, baja frecuencia de publicación u horarios incorrectos.

### Reel Avg Watch Time *(tiempo visto ÷ duración del video × 100)*
| 🟢 Excelente | 🟡 Normal | 🔴 Bajo |
|---|---|---|
| Mayor a 50% del video | Entre 25% y 50% | Menor a 25% |

### Story Exit Rate *(exits ÷ reach × 100)*
| 🟢 Excelente | 🟡 Normal | 🔴 Alto |
|---|---|---|
| Menor a 15% | Entre 15% y 35% | Mayor a 35% |

> En Stories el semáforo está invertido: un exit rate alto es malo porque significa que la gente cerró antes de terminar de ver.

---

## Las 3 Preguntas aplicadas al contenido orgánico

### 1. ¿Qué pasó?
Claude presenta una tabla con todos los posts del periodo analizado, con sus métricas y semáforos. Incluye:
- Cuántos posts se publicaron
- Promedio de reach rate de la cuenta
- Promedio de engagement rate
- El post con mejor y peor performance

### 2. ¿Por qué pasó?
Claude diagnostica buscando patrones:
- **Formato:** ¿Los reels tienen más reach que las imágenes? ¿Los carruseles generan más saves?
- **Timing:** ¿Hay días u horas donde el performance es claramente mejor?
- **Contenido:** ¿Los posts educativos (listas, tutoriales) generan más saves? ¿Los de opinión generan más shares?
- **Consistencia:** ¿Cuántos días pasan entre publicaciones? La irregularidad penaliza el algoritmo.

### 3. ¿Qué haremos?
Recomendaciones priorizadas por urgencia:
- 🔴 **URGENTE** — problemas críticos que están limitando el crecimiento
- 🟡 **IMPORTANTE** — oportunidades de mejora claras
- 🟢 **POTENCIAR** — lo que ya funciona y hay que hacer más

---

## Estructura de archivos del plugin

```
aura-studio/
│
├── CLAUDE.md                    ← Las reglas de comportamiento de Claude
├── README.md                    ← Instrucciones de instalación para alumnos
├── .gitignore                   ← Protege tokens y datos sensibles
│
├── .claude-plugin/
│   └── plugin.json              ← Manifiesto: define el plugin para Claude Code
│
├── skills/aura/
│   └── SKILL.md                 ← La metodología completa (las 3 Preguntas)
│
└── scripts/
    ├── _common.py               ← Base técnica compartida
    ├── verify_token.py          ← Verifica el token antes de hacer cualquier cosa
    ├── fetch_account.py         ← Trae datos de la cuenta de Instagram
    ├── fetch_media.py           ← Lista los posts recientes
    ├── fetch_insights.py        ← Descarga métricas detalladas de cada post
    └── fetch_stories.py         ← Métricas de Stories activas
```

### ¿Qué hace cada archivo en detalle?

**`CLAUDE.md`** — Es el "cerebro de seguridad" del plugin. Le dice a Claude cómo comportarse: cuánto tiempo esperar entre llamadas a la API, qué hacer si un token está expirado, cómo registrar cada acción en un log, qué hacer si Instagram bloquea el acceso. También define el tono de comunicación: lenguaje de negocio, no de desarrollador.

**`SKILL.md`** — Es el "cerebro de análisis". Contiene toda la metodología: el flujo de 6 fases, los benchmarks del semáforo, cómo estructurar las 3 Preguntas, qué métricas pedir para cada tipo de contenido.

**`_common.py`** — Es la base técnica que usan todos los demás scripts. Maneja la conexión a la API, los reintentos si hay error, la paginación de resultados y el logging. También tiene las funciones del semáforo.

**`verify_token.py`** — Antes de hacer cualquier otra cosa, Claude corre este script para confirmar que el token es válido, no está expirado y tiene los permisos correctos (`instagram_basic`, `instagram_manage_insights`, `pages_read_engagement`). Si falta algún permiso, para ahí y le explica al usuario cómo solucionarlo.

**`fetch_account.py`** — Trae el nombre de la cuenta, @username, número de seguidores, total de posts y tipo de cuenta (Business o Creator). Los seguidores son necesarios para calcular el reach rate.

**`fetch_media.py`** — Lista los posts recientes con su tipo (IMAGEN / CARRUSEL / REEL), fecha, preview del caption y métricas básicas. Detecta automáticamente el tipo de cada post.

**`fetch_insights.py`** — El script más importante. Para cada post, hace una sola llamada a la API pidiendo todas las métricas a la vez (optimización clave para no saturar la API). Calcula todos los rates y asigna el semáforo. Al final calcula los promedios de la cuenta para poder comparar.

**`fetch_stories.py`** — Especial para Stories porque sus métricas solo están disponibles mientras están activas (24 horas). Trae exit rate, taps forward/back y replies.

---

## La protección anti-bloqueo

A diferencia de la Marketing API (que tiene límites muy estrictos de 60 llamadas cada 5 minutos), la Instagram Graph API es más permisiva. Pero igual implementamos protecciones:

- **Intervalo mínimo de 2 segundos** entre cada llamada a la API
- **Máximo 20 posts por sesión** para no saturar
- **Análisis secuencial** — un post a la vez, no todos en paralelo
- **Log de todas las llamadas** en `ig_api.log`
- **Verificación de token** antes de cualquier acción
- **Tokens protegidos** — nunca aparecen en logs ni mensajes, solo en `.env`
- **`.gitignore`** que excluye todos los archivos con datos sensibles

---

## Cómo lo instalan tus alumnos el sábado

### Requisitos previos
1. Cuenta de Instagram **Business o Creator** (no personal)
2. Cuenta conectada a una **Página de Facebook**
3. Claude Code activo (plan Pro o superior)
4. Python instalado (`python --version` para verificar)
5. Librería requests: `pip install requests`

### Pasos de instalación
1. En Claude Code escribir `/manage-plugins`
2. Ir a **Marketplace**
3. Buscar `CristinaChaconSanta/aura-studio`
4. Instalar
5. Abrir una carpeta de trabajo nueva
6. Escribir `/aura` para activar el skill
7. Claude pide el token y guía el resto

### Cómo obtener el token
1. Ir a [developers.facebook.com](https://developers.facebook.com)
2. Crear una app (o usar una existente)
3. En Herramientas → Explorador de la API Graph
4. Generar token con permisos: `instagram_basic`, `instagram_manage_insights`, `pages_read_engagement`, `pages_show_list`
5. Convertir a token de larga duración (60 días)

---

## Dónde está el plugin

**GitHub público:** [github.com/CristinaChaconSanta/aura-studio](https://github.com/CristinaChaconSanta/aura-studio)

Cualquier persona puede instalarlo desde Claude Code usando ese repositorio.

---

## En resumen: qué tiene de especial este plugin

1. **Es el primer plugin de Claude Code** enfocado en análisis orgánico de Instagram (no de pauta)
2. **Usa la API actualizada de 2025** con la métrica `views` para Reels (la mayoría de tutoriales usan `impressions` que ya fue deprecado)
3. **Benchmarks específicos para LATAM** — no son promedios globales genéricos
4. **Metodología estructurada** — no es solo "dame mis métricas", es un análisis de 3 Preguntas con diagnóstico y recomendaciones accionables
5. **Protección real** — el CLAUDE.md previene que Claude haga llamadas inseguras o exponga tokens
6. **Lenguaje de marketer, no de dev** — Claude traduce todo a términos de negocio, no de API

---

*Aura Studio v1.0 — Construido para la masterclass de análisis de contenido orgánico para líderes de marketing en LATAM.*
