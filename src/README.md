# Código fuente

Este directorio contiene el código fuente del proyecto, organizado en tres módulos principales.

## Estructura

### `backend/`

Backend serverless construido con AWS Lambda y API Gateway. Proporciona APIs REST para búsqueda de clínicas, doctores, especialidades y seguros.

**Componentes principales:**
- `lambdas/`: Funciones Lambda organizadas por dominio (clinics, doctors, especialidades, seguros, search)
- `aws/`: Configuración de infraestructura con CloudFormation
- `scripts/`: Scripts de despliegue y población de datos
- `shared/`: Código compartido entre lambdas (repositorios, utilidades, excepciones)

**Documentación:**
- `README.md`: Arquitectura y guía de implementación
- `DATABASE_INFO.md`: Esquema de tablas DynamoDB
- `INSTRUCTIONS.md`: Instrucciones de despliegue

### `frontend/`

Aplicación web construida con Next.js que proporciona una interfaz para búsqueda de clínicas, doctores y un chatbot asistente médico.

**Componentes principales:**
- `app/`: Aplicación Next.js con App Router
  - `api/`: API routes que actúan como proxy hacia el backend AWS
  - `components/`: Componentes React reutilizables
  - `hooks/`: Custom hooks para lógica de negocio
- `lib/`: Utilidades, tipos y constantes compartidas

**Documentación:**
- `README.md`: Guía de desarrollo
- `CODING_GUIDELINES.md`: Estándares de código

### `data/`

Scripts y datos para la recolección, limpieza y transformación de información de clínicas y doctores.

**Componentes principales:**
- `clinicas/`: Scripts de scraping y limpieza por clínica
- `CMP/`: Datos del Colegio Médico del Perú
- `final_tables/`: Tablas finales transformadas y listas para importar a DynamoDB

## Tecnologías

- **Backend**: Python 3.11+, AWS Lambda, API Gateway, DynamoDB
- **Frontend**: Next.js 16, React 19, TypeScript, Tailwind CSS
- **Data processing**: Python, pandas
- **Infrastructure**: AWS CloudFormation

## Requisitos

- Python 3.11+
- Node.js 18+
- AWS CLI configurado con perfil `hackathon`
- Dependencias Python: ver `backend/requirements.txt`
- Dependencias Node: ver `frontend/package.json`

## Uso

### Backend

Ver documentación en `backend/README.md` para instrucciones de despliegue y uso.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

La aplicación estará disponible en `http://localhost:3000`.

### Datos

Los scripts en `data/` procesan información de múltiples fuentes y generan tablas normalizadas en `data/final_tables/`.
