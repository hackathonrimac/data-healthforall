import { NextResponse } from 'next/server';

// Ubigeo data from final_tables/transformed/ubigeo.jsonl
const UBIGEO_DISTRICTS = [
  { ubigeoId: '70101', nombreDistrito: 'Callao', departamento: 'Callao', provincia: 'Callao', distritoId: '70101', idCercanos: ['70102', '70103', '70104', '70105', '70106'] },
  { ubigeoId: '70102', nombreDistrito: 'Bellavista', departamento: 'Callao', provincia: 'Callao', distritoId: '70102', idCercanos: ['70101', '70103', '70104', '70105', '70106'] },
  { ubigeoId: '70103', nombreDistrito: 'Carmen de la Legua - Reynoso', departamento: 'Callao', provincia: 'Callao', distritoId: '70103', idCercanos: ['70102', '70104', '70101', '70105', '70106'] },
  { ubigeoId: '70104', nombreDistrito: 'La Perla', departamento: 'Callao', provincia: 'Callao', distritoId: '70104', idCercanos: ['70103', '70105', '70102', '70106', '70101'] },
  { ubigeoId: '70105', nombreDistrito: 'La Punta', departamento: 'Callao', provincia: 'Callao', distritoId: '70105', idCercanos: ['70104', '70106', '70103', '70102', '70101'] },
  { ubigeoId: '70106', nombreDistrito: 'Ventanilla', departamento: 'Callao', provincia: 'Callao', distritoId: '70106', idCercanos: ['70105', '70104', '70103', '70102', '70101'] },
  { ubigeoId: '150101', nombreDistrito: 'Lima Cercado', departamento: 'Lima', provincia: 'Lima', distritoId: '150101', idCercanos: ['150102', '150104', '150105', '150106', '150107'] },
  { ubigeoId: '150102', nombreDistrito: 'Ancón', departamento: 'Lima', provincia: 'Lima', distritoId: '150102', idCercanos: ['150101', '150104', '150105', '150106', '150107'] },
  { ubigeoId: '150104', nombreDistrito: 'Ate', departamento: 'Lima', provincia: 'Lima', distritoId: '150104', idCercanos: ['150105', '150106', '150102', '150107', '150101'] },
  { ubigeoId: '150105', nombreDistrito: 'Barranco', departamento: 'Lima', provincia: 'Lima', distritoId: '150105', idCercanos: ['150104', '150106', '150107', '150108', '150102'] },
  { ubigeoId: '150106', nombreDistrito: 'Breña', departamento: 'Lima', provincia: 'Lima', distritoId: '150106', idCercanos: ['150107', '150105', '150104', '150108', '150109'] },
  { ubigeoId: '150107', nombreDistrito: 'Carabayllo', departamento: 'Lima', provincia: 'Lima', distritoId: '150107', idCercanos: ['150108', '150106', '150109', '150105', '150104'] },
  { ubigeoId: '150108', nombreDistrito: 'Chaclacayo', departamento: 'Lima', provincia: 'Lima', distritoId: '150108', idCercanos: ['150109', '150107', '150110', '150106', '150105'] },
  { ubigeoId: '150109', nombreDistrito: 'Chorrillos', departamento: 'Lima', provincia: 'Lima', distritoId: '150109', idCercanos: ['150110', '150108', '150107', '150111', '150112'] },
  { ubigeoId: '150110', nombreDistrito: 'Cieneguilla', departamento: 'Lima', provincia: 'Lima', distritoId: '150110', idCercanos: ['150109', '150111', '150112', '150108', '150113'] },
  { ubigeoId: '150111', nombreDistrito: 'Comas', departamento: 'Lima', provincia: 'Lima', distritoId: '150111', idCercanos: ['150112', '150110', '150113', '150109', '150114'] },
  { ubigeoId: '150112', nombreDistrito: 'El Agustino', departamento: 'Lima', provincia: 'Lima', distritoId: '150112', idCercanos: ['150113', '150111', '150114', '150110', '150115'] },
  { ubigeoId: '150113', nombreDistrito: 'Independencia', departamento: 'Lima', provincia: 'Lima', distritoId: '150113', idCercanos: ['150114', '150112', '150115', '150111', '150116'] },
  { ubigeoId: '150114', nombreDistrito: 'Jesús María', departamento: 'Lima', provincia: 'Lima', distritoId: '150114', idCercanos: ['150115', '150113', '150116', '150112', '150117'] },
  { ubigeoId: '150115', nombreDistrito: 'La Molina', departamento: 'Lima', provincia: 'Lima', distritoId: '150115', idCercanos: ['150116', '150114', '150117', '150113', '150118'] },
  { ubigeoId: '150116', nombreDistrito: 'La Victoria', departamento: 'Lima', provincia: 'Lima', distritoId: '150116', idCercanos: ['150117', '150115', '150118', '150114', '150119'] },
  { ubigeoId: '150117', nombreDistrito: 'Lince', departamento: 'Lima', provincia: 'Lima', distritoId: '150117', idCercanos: ['150116', '150118', '150119', '150115', '150114'] },
  { ubigeoId: '150118', nombreDistrito: 'Los Olivos', departamento: 'Lima', provincia: 'Lima', distritoId: '150118', idCercanos: ['150119', '150117', '150120', '150116', '150121'] },
  { ubigeoId: '150119', nombreDistrito: 'Lurigancho', departamento: 'Lima', provincia: 'Lima', distritoId: '150119', idCercanos: ['150120', '150118', '150121', '150117', '150122'] },
  { ubigeoId: '150120', nombreDistrito: 'Lurín', departamento: 'Lima', provincia: 'Lima', distritoId: '150120', idCercanos: ['150119', '150121', '150122', '150118', '150123'] },
  { ubigeoId: '150121', nombreDistrito: 'Magdalena del Mar', departamento: 'Lima', provincia: 'Lima', distritoId: '150121', idCercanos: ['150120', '150122', '150123', '150119', '150124'] },
  { ubigeoId: '150122', nombreDistrito: 'Miraflores', departamento: 'Lima', provincia: 'Lima', distritoId: '150122', idCercanos: ['150123', '150121', '150120', '150124', '150125'] },
  { ubigeoId: '150123', nombreDistrito: 'Pachacámac', departamento: 'Lima', provincia: 'Lima', distritoId: '150123', idCercanos: ['150124', '150122', '150125', '150121', '150120'] },
  { ubigeoId: '150124', nombreDistrito: 'Pucusana', departamento: 'Lima', provincia: 'Lima', distritoId: '150124', idCercanos: ['150123', '150125', '150122', '150126', '150121'] },
  { ubigeoId: '150125', nombreDistrito: 'Pueblo Libre', departamento: 'Lima', provincia: 'Lima', distritoId: '150125', idCercanos: ['150126', '150124', '150127', '150123', '150128'] },
  { ubigeoId: '150126', nombreDistrito: 'Puente Piedra', departamento: 'Lima', provincia: 'Lima', distritoId: '150126', idCercanos: ['150127', '150125', '150124', '150128', '150129'] },
  { ubigeoId: '150127', nombreDistrito: 'Punta Hermosa', departamento: 'Lima', provincia: 'Lima', distritoId: '150127', idCercanos: ['150128', '150126', '150125', '150129', '150124'] },
  { ubigeoId: '150128', nombreDistrito: 'Punta Negra', departamento: 'Lima', provincia: 'Lima', distritoId: '150128', idCercanos: ['150129', '150127', '150126', '150130', '150131'] },
  { ubigeoId: '150129', nombreDistrito: 'Rímac', departamento: 'Lima', provincia: 'Lima', distritoId: '150129', idCercanos: ['150130', '150128', '150127', '150131', '150126'] },
  { ubigeoId: '150130', nombreDistrito: 'San Bartolo', departamento: 'Lima', provincia: 'Lima', distritoId: '150130', idCercanos: ['150131', '150129', '150132', '150128', '150133'] },
  { ubigeoId: '150131', nombreDistrito: 'San Borja', departamento: 'Lima', provincia: 'Lima', distritoId: '150131', idCercanos: ['150132', '150130', '150129', '150133', '150128'] },
  { ubigeoId: '150132', nombreDistrito: 'San Isidro', departamento: 'Lima', provincia: 'Lima', distritoId: '150132', idCercanos: ['150131', '150133', '150130', '150134', '150135'] },
  { ubigeoId: '150133', nombreDistrito: 'San Juan de Lurigancho', departamento: 'Lima', provincia: 'Lima', distritoId: '150133', idCercanos: ['150134', '150132', '150135', '150131', '150136'] },
  { ubigeoId: '150134', nombreDistrito: 'San Juan de Miraflores', departamento: 'Lima', provincia: 'Lima', distritoId: '150134', idCercanos: ['150135', '150133', '150132', '150136', '150137'] },
  { ubigeoId: '150135', nombreDistrito: 'San Luis', departamento: 'Lima', provincia: 'Lima', distritoId: '150135', idCercanos: ['150136', '150134', '150137', '150133', '150138'] },
  { ubigeoId: '150136', nombreDistrito: 'San Martín de Porres', departamento: 'Lima', provincia: 'Lima', distritoId: '150136', idCercanos: ['150137', '150135', '150138', '150134', '150139'] },
  { ubigeoId: '150137', nombreDistrito: 'San Miguel', departamento: 'Lima', provincia: 'Lima', distritoId: '150137', idCercanos: ['150138', '150136', '150139', '150135', '150140'] },
  { ubigeoId: '150138', nombreDistrito: 'Santa Anita', departamento: 'Lima', provincia: 'Lima', distritoId: '150138', idCercanos: ['150139', '150137', '150140', '150136', '150141'] },
  { ubigeoId: '150139', nombreDistrito: 'Santa María del Mar', departamento: 'Lima', provincia: 'Lima', distritoId: '150139', idCercanos: ['150140', '150138', '150141', '150137', '150142'] },
  { ubigeoId: '150140', nombreDistrito: 'Santa Rosa', departamento: 'Lima', provincia: 'Lima', distritoId: '150140', idCercanos: ['150141', '150139', '150142', '150138', '150143'] },
  { ubigeoId: '150141', nombreDistrito: 'Santiago de Surco', departamento: 'Lima', provincia: 'Lima', distritoId: '150141', idCercanos: ['150142', '150140', '150143', '150139', '150144'] },
  { ubigeoId: '150142', nombreDistrito: 'Surquillo', departamento: 'Lima', provincia: 'Lima', distritoId: '150142', idCercanos: ['150143', '150141', '150144', '150140', '150139'] },
  { ubigeoId: '150143', nombreDistrito: 'Villa El Salvador', departamento: 'Lima', provincia: 'Lima', distritoId: '150143', idCercanos: ['150144', '150142', '150141', '150140', '150139'] },
  { ubigeoId: '150144', nombreDistrito: 'Villa María del Triunfo', departamento: 'Lima', provincia: 'Lima', distritoId: '150144', idCercanos: ['150143', '150142', '150141', '150140', '150139'] },
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

