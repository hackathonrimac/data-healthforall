import { NextResponse } from 'next/server';

// Ubigeo data matching sample_data.py
const UBIGEO_DISTRICTS = [
  { ubigeoId: '150101', nombreDistrito: 'San Isidro', departamento: 'Lima', provincia: 'Lima', distritoId: '150101' },
  { ubigeoId: '150108', nombreDistrito: 'Jesús María', departamento: 'Lima', provincia: 'Lima', distritoId: '150108' },
  { ubigeoId: '150132', nombreDistrito: 'Santiago de Surco', departamento: 'Lima', provincia: 'Lima', distritoId: '150132' },
  { ubigeoId: '150140', nombreDistrito: 'Miraflores', departamento: 'Lima', provincia: 'Lima', distritoId: '150140' },
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

