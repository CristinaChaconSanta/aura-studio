# Aura Studio 🌿
### Análisis de contenido orgánico de Instagram para líderes de marketing en LATAM

Analiza el rendimiento de tus publicaciones orgánicas de Instagram usando la metodología de las **3 Preguntas** con semáforo de benchmarks (🔴🟡🟢).

---

## ¿Qué mide Aura Studio?

| Tipo de contenido | Métricas |
|---|---|
| **Imágenes y Carruseles** | Reach, Likes, Comentarios, Shares, Saves, Engagement Rate |
| **Reels** | Views, Reach, Avg Watch Time, Saves, Shares, Engagement Rate |
| **Stories** | Reach, Exits, Taps Forward/Back, Replies |

---

## Requisitos

- Cuenta de Instagram **Business** o **Creator**
- Conectada a una **Página de Facebook**
- Plan de Claude con Claude Code activo (Pro o superior)
- Python 3.9+ instalado
- Librería `requests`: `pip install requests`

---

## Instalación en Claude Code

### Paso 1 — Instalar el plugin

En Claude Code (VS Code), escribe:

```
/manage-plugins
```

Ve a **Marketplace** y busca el repositorio de este plugin, o instálalo directamente con:

```
/manage-plugins → Add from GitHub → [tu-usuario]/aura-studio
```

### Paso 2 — Crear tu carpeta de trabajo

1. En VS Code: **File → Open Folder**
2. Crea una carpeta nueva llamada `aura-[nombre-cliente]` o `aura-micuenta`
3. Abre esa carpeta

### Paso 3 — Obtener tu token de Instagram

1. Ve a [developers.facebook.com](https://developers.facebook.com) → **Mis Apps**
2. Crea una app o usa una existente
3. En **Herramientas → Explorador de la API Graph**, genera un token con estos permisos:
   - `instagram_basic`
   - `instagram_manage_insights`
   - `pages_read_engagement`
   - `pages_show_list`
4. Convierte el token a **larga duración** (60 días) para no tener que renovarlo seguido

### Paso 4 — Activar el skill

En el chat de Claude Code escribe:

```
/aura
```

Claude te pedirá tu token y guiará el resto del proceso automáticamente.

---

## Cómo funciona: las 3 Preguntas

### ¿Qué pasó?
Compara el performance de tus publicaciones contra los promedios de tu propia cuenta y los benchmarks de LATAM.

### ¿Por qué pasó?
Diagnostica qué formatos funcionan mejor, en qué horarios, qué tipo de contenido genera más saves o shares.

### ¿Qué haremos?
Recomendaciones priorizadas por impacto: qué potenciar, qué ajustar y qué dejar de hacer.

---

## Benchmarks LATAM 2025

| Métrica | 🟢 Excelente | 🟡 Normal | 🔴 Bajo |
|---|---|---|---|
| Engagement Rate | > 5% | 2–5% | < 2% |
| Save Rate | > 3% | 1–3% | < 1% |
| Share Rate | > 1.5% | 0.5–1.5% | < 0.5% |
| Reach Rate | > 15% | 7–15% | < 7% |
| Reel Watch Time | > 50% | 25–50% | < 25% |
| Story Exit Rate | < 15% | 15–35% | > 35% |

---

## Archivos generados en tu carpeta

| Archivo | Contenido |
|---|---|
| `token_info.json` | Info del token (permisos, expiración) |
| `account_info.json` | Datos de tu cuenta de Instagram |
| `media_list.json` | Lista de publicaciones recientes |
| `insights.json` | Métricas detalladas con semáforos y rates |
| `stories.json` | Métricas de Stories activas |
| `ig_api.log` | Registro de todas las llamadas a la API |

> Todos los archivos `.json` y el `.env` están en `.gitignore` para proteger tu token.

---

## Importante — Solo lectura

Aura Studio **nunca escribe, modifica ni crea publicaciones** en tu cuenta. Solo lee métricas. Todos los permisos son de lectura.

---

## Créditos

Metodología de las 3 Preguntas adaptada para contenido orgánico de Instagram.
Desarrollado para la masterclass **Aura Studio** — análisis de contenido orgánico para líderes de marketing en LATAM.
