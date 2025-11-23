export interface UbigeoDistrict {
  code: string;
  name: string;
  department: string;
  province: string;
}

export const LIMA_CALLAO_DISTRICTS: UbigeoDistrict[] = [
  // Lima Metropolitana
  { code: '150101', name: 'Lima', department: 'Lima', province: 'Lima' },
  { code: '150102', name: 'Ancón', department: 'Lima', province: 'Lima' },
  { code: '150103', name: 'Ate', department: 'Lima', province: 'Lima' },
  { code: '150104', name: 'Barranco', department: 'Lima', province: 'Lima' },
  { code: '150105', name: 'Breña', department: 'Lima', province: 'Lima' },
  { code: '150106', name: 'Carabayllo', department: 'Lima', province: 'Lima' },
  { code: '150107', name: 'Chaclacayo', department: 'Lima', province: 'Lima' },
  { code: '150108', name: 'Chorrillos', department: 'Lima', province: 'Lima' },
  { code: '150109', name: 'Cieneguilla', department: 'Lima', province: 'Lima' },
  { code: '150110', name: 'Comas', department: 'Lima', province: 'Lima' },
  { code: '150111', name: 'El Agustino', department: 'Lima', province: 'Lima' },
  { code: '150112', name: 'Independencia', department: 'Lima', province: 'Lima' },
  { code: '150113', name: 'Jesús María', department: 'Lima', province: 'Lima' },
  { code: '150114', name: 'La Molina', department: 'Lima', province: 'Lima' },
  { code: '150115', name: 'La Victoria', department: 'Lima', province: 'Lima' },
  { code: '150116', name: 'Lince', department: 'Lima', province: 'Lima' },
  { code: '150117', name: 'Los Olivos', department: 'Lima', province: 'Lima' },
  { code: '150118', name: 'Lurigancho', department: 'Lima', province: 'Lima' },
  { code: '150119', name: 'Lurín', department: 'Lima', province: 'Lima' },
  { code: '150120', name: 'Magdalena del Mar', department: 'Lima', province: 'Lima' },
  { code: '150121', name: 'Pueblo Libre', department: 'Lima', province: 'Lima' },
  { code: '150122', name: 'Miraflores', department: 'Lima', province: 'Lima' },
  { code: '150123', name: 'Pachacámac', department: 'Lima', province: 'Lima' },
  { code: '150124', name: 'Pucusana', department: 'Lima', province: 'Lima' },
  { code: '150125', name: 'Puente Piedra', department: 'Lima', province: 'Lima' },
  { code: '150126', name: 'Punta Hermosa', department: 'Lima', province: 'Lima' },
  { code: '150127', name: 'Punta Negra', department: 'Lima', province: 'Lima' },
  { code: '150128', name: 'Rímac', department: 'Lima', province: 'Lima' },
  { code: '150129', name: 'San Bartolo', department: 'Lima', province: 'Lima' },
  { code: '150130', name: 'San Borja', department: 'Lima', province: 'Lima' },
  { code: '150131', name: 'San Isidro', department: 'Lima', province: 'Lima' },
  { code: '150132', name: 'San Juan de Lurigancho', department: 'Lima', province: 'Lima' },
  { code: '150133', name: 'San Juan de Miraflores', department: 'Lima', province: 'Lima' },
  { code: '150134', name: 'San Luis', department: 'Lima', province: 'Lima' },
  { code: '150135', name: 'San Martín de Porres', department: 'Lima', province: 'Lima' },
  { code: '150136', name: 'San Miguel', department: 'Lima', province: 'Lima' },
  { code: '150137', name: 'Santa Anita', department: 'Lima', province: 'Lima' },
  { code: '150138', name: 'Santa María del Mar', department: 'Lima', province: 'Lima' },
  { code: '150139', name: 'Santa Rosa', department: 'Lima', province: 'Lima' },
  { code: '150140', name: 'Santiago de Surco', department: 'Lima', province: 'Lima' },
  { code: '150141', name: 'Surquillo', department: 'Lima', province: 'Lima' },
  { code: '150142', name: 'Villa El Salvador', department: 'Lima', province: 'Lima' },
  { code: '150143', name: 'Villa María del Triunfo', department: 'Lima', province: 'Lima' },
  
  // Callao
  { code: '070101', name: 'Callao', department: 'Callao', province: 'Callao' },
  { code: '070102', name: 'Bellavista', department: 'Callao', province: 'Callao' },
  { code: '070103', name: 'Carmen de la Legua Reynoso', department: 'Callao', province: 'Callao' },
  { code: '070104', name: 'La Perla', department: 'Callao', province: 'Callao' },
  { code: '070105', name: 'La Punta', department: 'Callao', province: 'Callao' },
  { code: '070106', name: 'Ventanilla', department: 'Callao', province: 'Callao' },
  { code: '070107', name: 'Mi Perú', department: 'Callao', province: 'Callao' },
];

// Sorted districts by name for dropdown display
export const SORTED_DISTRICTS = [...LIMA_CALLAO_DISTRICTS].sort((a, b) => 
  a.name.localeCompare(b.name, 'es')
);

