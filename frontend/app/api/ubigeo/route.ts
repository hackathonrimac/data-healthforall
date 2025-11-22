import { NextResponse } from 'next/server';

// Ubigeo data for Lima and Callao districts
const UBIGEO_DISTRICTS = [
  // Lima Metropolitana
  { ubigeoId: '150101', nombreDistrito: 'Lima', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150102', nombreDistrito: 'Ancón', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150103', nombreDistrito: 'Ate', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150104', nombreDistrito: 'Barranco', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150105', nombreDistrito: 'Breña', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150106', nombreDistrito: 'Carabayllo', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150107', nombreDistrito: 'Chaclacayo', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150108', nombreDistrito: 'Chorrillos', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150109', nombreDistrito: 'Cieneguilla', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150110', nombreDistrito: 'Comas', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150111', nombreDistrito: 'El Agustino', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150112', nombreDistrito: 'Independencia', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150113', nombreDistrito: 'Jesús María', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150114', nombreDistrito: 'La Molina', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150115', nombreDistrito: 'La Victoria', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150116', nombreDistrito: 'Lince', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150117', nombreDistrito: 'Los Olivos', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150118', nombreDistrito: 'Lurigancho', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150119', nombreDistrito: 'Lurín', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150120', nombreDistrito: 'Magdalena del Mar', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150121', nombreDistrito: 'Pueblo Libre', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150122', nombreDistrito: 'Miraflores', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150123', nombreDistrito: 'Pachacámac', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150124', nombreDistrito: 'Pucusana', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150125', nombreDistrito: 'Puente Piedra', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150126', nombreDistrito: 'Punta Hermosa', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150127', nombreDistrito: 'Punta Negra', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150128', nombreDistrito: 'Rímac', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150129', nombreDistrito: 'San Bartolo', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150130', nombreDistrito: 'San Borja', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150131', nombreDistrito: 'San Isidro', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150132', nombreDistrito: 'San Juan de Lurigancho', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150133', nombreDistrito: 'San Juan de Miraflores', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150134', nombreDistrito: 'San Luis', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150135', nombreDistrito: 'San Martín de Porres', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150136', nombreDistrito: 'San Miguel', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150137', nombreDistrito: 'Santa Anita', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150138', nombreDistrito: 'Santa María del Mar', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150139', nombreDistrito: 'Santa Rosa', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150140', nombreDistrito: 'Santiago de Surco', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150141', nombreDistrito: 'Surquillo', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150142', nombreDistrito: 'Villa El Salvador', departamento: 'Lima', provincia: 'Lima' },
  { ubigeoId: '150143', nombreDistrito: 'Villa María del Triunfo', departamento: 'Lima', provincia: 'Lima' },
  
  // Callao
  { ubigeoId: '070101', nombreDistrito: 'Callao', departamento: 'Callao', provincia: 'Callao' },
  { ubigeoId: '070102', nombreDistrito: 'Bellavista', departamento: 'Callao', provincia: 'Callao' },
  { ubigeoId: '070103', nombreDistrito: 'Carmen de la Legua Reynoso', departamento: 'Callao', provincia: 'Callao' },
  { ubigeoId: '070104', nombreDistrito: 'La Perla', departamento: 'Callao', provincia: 'Callao' },
  { ubigeoId: '070105', nombreDistrito: 'La Punta', departamento: 'Callao', provincia: 'Callao' },
  { ubigeoId: '070106', nombreDistrito: 'Ventanilla', departamento: 'Callao', provincia: 'Callao' },
  { ubigeoId: '070107', nombreDistrito: 'Mi Perú', departamento: 'Callao', provincia: 'Callao' },
];

export async function GET() {
  try {
    // Return the ubigeo districts list
    return NextResponse.json(UBIGEO_DISTRICTS);
  } catch (error) {
    console.error('Ubigeo error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

