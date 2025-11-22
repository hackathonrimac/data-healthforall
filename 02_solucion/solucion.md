# 📊 Entregable 2: Avances y hallazgos

> **⚠️ Importante:** Este entregable debe completarse antes del **sábado 22 de noviembre a las 4:00 PM** para continuar en la competencia.

---

## ✅ Cómo entregar este documento

1. **Completa todas las secciones** de este archivo con tus avances y hallazgos
2. **Guarda los cambios:**
   - Desde GitHub: Presiona "Commit changes" al terminar de editar
   - Localmente: Ejecuta `git add .` y `git commit -m "Entregable 2 completo"`
3. **Sube a GitHub:** 
   - Desde GitHub: Automático al hacer commit
   - Localmente: Ejecuta `git push`
4. **Verifica:** Refresca este repositorio en GitHub y confirma que tus cambios estén visibles

> 💡 **Recordatorio:** Este es el mismo repositorio del Entregable 1. Solo actualiza este archivo.

---

## 1. ¿Qué hallazgos han tenido?

*"En el análisis identificamos un total de 120 clínicas, muchas de ellas con información incompleta o con formatos inconsistentes. Para complementar y estandarizar los datos realizamos web scraping en diversas fuentes públicas y en el Colegio Médico del Perú, desde donde obtuvimos especialidades, subespecialidades y el MCP de los doctores. Además, aproximadamente el 30% de las clínicas contaban con APIs abiertas, lo que permitió obtener parte del staff médico de forma estructurada. También encontramos que la información sobre grupos propietarios estaba fragmentada, por lo que construimos una tabla maestra que nos permitió identificar 16 grupos de clínicas que administran múltiples sedes. Finalmente, completamos los ubigeos cruzando distritos y direcciones con tablas oficiales y normalizamos las nomenclaturas médicas, logrando una base integrada, consistente y lista para análisis."*

---

## 2. ¿En qué se van a enfocar para el cierre?

*"Nos concentraremos en:"*
- *Subir y estructurar todas las tablas en AWS.*
- *Habilitar las consultas SQL para buscar clínicas, médicos y especialidades.*
- *Conectar el chatbot que interpretará los síntomas del paciente y asignará la especialidad adecuada.*
- *Relacionar esa especialidad con médicos y con las clínicas donde trabajan.*
- *Recomendar automáticamente la clínica más cercana al paciente usando su ubicación.*
- *Validar el flujo completo end-to-end para entregar una demo funcional.*
