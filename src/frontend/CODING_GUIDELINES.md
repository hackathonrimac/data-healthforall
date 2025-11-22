# Guía de Código Frontend

## 1. Principios de Arquitectura (SOLID)

- **Responsabilidad Única**: Un componente, un propósito
- **Abierto/Cerrado**: Extiende vía props/composición, nunca modifiques el core
- **Sustitución de Liskov**: Los componentes deben ser intercambiables con sus tipos
- **Segregación de Interfaces**: Interfaces pequeñas y específicas
- **Inversión de Dependencias**: Importa abstracciones, inyecta dependencias

## 2. Librería de Componentes

**Siempre usa ShadCN/UI**
- Copia componentes directamente de ShadCN
- Personaliza solo con clases de Tailwind
- No uses librerías UI externas

## 3. Sistema de Diseño

### Paleta de Colores
- Fondo: solo `bg-white`
- Texto: `text-gray-900`, `text-gray-600`, `text-gray-400`
- Acentos: Mínimos, usa con moderación

### Efecto Glassmorphism
```tsx
className="bg-white/70 backdrop-blur-md border border-white/20 shadow-lg"
```

**Reglas del Efecto Glass:**
- Fondos translúcidos: `bg-white/70` o `bg-white/60`
- Desenfoque: `backdrop-blur-md` o `backdrop-blur-lg`
- Bordes: `border border-white/20` o `border-gray-200/50`
- Sombras: `shadow-lg` o `shadow-xl`
- Esquinas redondeadas: `rounded-xl` o `rounded-2xl`

### Tipografía
- Encabezados: `font-semibold` o `font-bold`
- Cuerpo: `font-normal`
- Tamaños: Usa escala Tailwind (`text-sm`, `text-base`, `text-lg`, etc.)

### Espaciado
- Padding consistente: `p-4`, `p-6`, `p-8`
- Márgenes: Usa utilidades gap (`gap-4`, `gap-6`)
- El espacio en blanco es esencial

## 4. Calidad de Código

### Mantenlo Simple
- Evita sobre-ingeniería
- No hagas abstracciones innecesarias
- No uses código defensivo a menos que sea crítico
- Confía en el sistema de tipos

### Estructura de Componentes
```tsx
// 1. Imports
// 2. Types
// 3. Component
// 4. Exports
```

### Nomenclatura de Archivos
- Todos los archivos: `snake_case.tsx` / `snake_case.ts`
- Hooks: `use_[nombre].ts`
- Exportación de componentes: `PascalCase` (el archivo sigue siendo snake_case)

## 5. Integración de API

### Estructura de API Routes de Next.js
```
app/api/
  ├── search/
  │   └── route.ts          # GET /api/search?query=...
  ├── clinics/
  │   └── route.ts          # GET /api/clinics
  ├── doctors/
  │   └── route.ts          # GET /api/doctors
  ├── especialidades/
  │   └── route.ts          # GET /api/especialidades
  └── seguros/
      └── route.ts          # GET /api/seguros
```

### Patrón de API Route
```tsx
// app/api/search/route.ts
import { NextRequest, NextResponse } from 'next/server';

const AWS_BASE_URL = process.env.AWS_API_URL;

export async function GET(request: NextRequest) {
  const query = request.nextUrl.searchParams.get('query');
  
  const response = await fetch(`${AWS_BASE_URL}/search/doctors?query=${query}`);
  const data = await response.json();
  
  return NextResponse.json(data);
}
```

### Patrón de Cliente Frontend
```tsx
// services/search_service.ts
export async function searchDoctors(query: string) {
  return fetch(`/api/search?query=${encodeURIComponent(query)}`)
    .then(r => r.json());
}
```

**Reglas:**
- Las API routes hacen proxy al backend AWS
- Un archivo route por endpoint
- Tipifica las respuestas: `types/api_types.ts`
- Usa React Query/SWR para llamadas del cliente
- Maneja errores con toast de ShadCN

## 6. Rendimiento

- Usa `'use client'` solo cuando sea necesario
- Server components por defecto
- Lazy load de componentes pesados
- Optimiza imágenes con Next.js Image

## 7. Prácticas Prohibidas

- ❌ Estilos inline
- ❌ CSS modules (solo usa Tailwind)
- ❌ Cualquier librería UI que no sea ShadCN
- ❌ Manejadores de estado complejos (usa React state/Context)
- ❌ Fondos de color (solo blanco)
- ❌ Código sobre-comentado

## 8. Ejemplo de Glass Card

```tsx
export function GlassCard({ children }: { children: React.ReactNode }) {
  return (
    <div className="bg-white/70 backdrop-blur-md border border-white/20 shadow-xl rounded-2xl p-6">
      {children}
    </div>
  );
}
```

---

**Recuerda: Simplicidad > Complejidad. Hermoso > Exceso funcional.**
