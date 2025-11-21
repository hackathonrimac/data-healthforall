# 📋 Entregable 1: Información del equipo y propuesta inicial

> **⚠️ Importante:** Este entregable debe completarse antes del **viernes 21 de noviembre a las 5:30 PM** para continuar en la competencia.

---

## ✅ Cómo entregar este documento

1. **Completa todas las secciones** de este archivo con la información de tu equipo
2. **Guarda los cambios:**
   - Desde GitHub: Presiona "Commit changes" al terminar de editar
   - Localmente: Ejecuta `git add .` y `git commit -m "Entregable 1 completo"`
3. **Sube a GitHub:** 
   - Desde GitHub: Automático al hacer commit
   - Localmente: Ejecuta `git push`
4. **Verifica:** Refresca este repositorio en GitHub y confirma que tus cambios estén visibles

> 💡 **Tip:** No necesitas crear un nuevo repositorio. Solo edita este archivo y guarda los cambios.

---

## Nombre del equipo

HealthForAll 🚀🩺


---

## ¿Cuéntanos a grandes rasgos qué planean hacer?

Desarollaremos una aplicación web para encontrar la facilidad médica más cercana a ti. 
NOTA: Solo trabajaremos en Lima Metropolitana - Callao 

1) Extraeremos la información de doctores, clínicas y ubicación con técnicas de web scrapping.
   Tecnología: Python, BeatifulSoup, Pandas, Selenium
   - Verificamos la información del Colegio Médico del Perú
   - Enlances web de las clínicas existentes en el Perú
   - Link del staff asociado a cada especialdiad y clínica.

2) Desplegaremos un servicio REST API para enviar la información al navegador
   Tecnología: CDK AWS, REST API, Lambda Server Functions
   - Se crearán endpoints para las peticiones requeridas en el flujo del usuario

3) Implementación de una web app para que el usuario pueda encontrar las clínicas más cercanas.
   Tecnología: NextJS, Vercel AI SDK, OpenAI SDK
   - Preguntaremos con los síntomas del paciente
   - Mostraremos un mapa con la información de cada clínica y especialidad
   - Listado de doctores disponibles en cada clínica

---

## ¿Qué retos/riesgos visualizan? (¿Con qué te podemos ayudar?)

Los retos que vemos es que mucha información sobre la disponibilidad médica no está disponible, debido a que los sistemas virtuales de cada hospital son cerrados y existen clínicas con poca virtualización de sus datos. 


---

## Tecnologías planificadas

Lista las principales tecnologías, frameworks y herramientas que planean utilizar:

**Frontend:**
- NextJS, Tailwind CSS, Vercel AI, SDK

**Backend:**
- FastAPI, Postgres SQL

**IA/ML:**
- Open AI API 

**Cloud/DevOps:**
- AWS Lambda Server functions

**Otras:**
- Beautiful Soup y Pandas para ETL
---

## Notas adicionales

Para asegurar que toda la información sea válida y podamos revisarla de forma manual para evitar halucinaciones, nos limitamos a trabajar únicamente con Lima Metropolitana y Callao. 