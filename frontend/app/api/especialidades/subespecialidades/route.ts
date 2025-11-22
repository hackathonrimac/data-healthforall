import { NextRequest, NextResponse } from 'next/server';

const AWS_BASE_URL = process.env.AWS_API_URL || process.env.NEXT_PUBLIC_API_URL || '';

export async function GET(request: NextRequest) {
  try {
    if (!AWS_BASE_URL) {
      return NextResponse.json(
        { error: 'API endpoint not configured. Please contact support.' },
        { status: 503 }
      );
    }

    const searchParams = request.nextUrl.searchParams;
    const especialidadId = searchParams.get('especialidadId');

    if (!especialidadId) {
      return NextResponse.json(
        { error: 'especialidadId is required' },
        { status: 400 }
      );
    }

    const params = new URLSearchParams({ especialidadId });

    const url = `${AWS_BASE_URL}/subespecialidades?${params.toString()}`;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const error = await response.text();
      return NextResponse.json(
        { error: `Backend error: ${error}` },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    console.error('Subespecialidades error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

