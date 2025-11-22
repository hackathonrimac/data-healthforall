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
    const ubigeoId = searchParams.get('ubigeoId');
    const especialidadId = searchParams.get('especialidadId');
    const seguroId = searchParams.get('seguroId');
    const page = searchParams.get('page') || '1';
    const pageSize = searchParams.get('pageSize') || '10';

    if (!ubigeoId || !especialidadId) {
      return NextResponse.json(
        { error: 'ubigeoId and especialidadId are required' },
        { status: 400 }
      );
    }

    const params = new URLSearchParams({
      ubigeoId,
      especialidadId,
      page,
      pageSize,
    });

    if (seguroId) {
      params.append('seguroId', seguroId);
    }

    const url = `${AWS_BASE_URL}/search/doctors?${params.toString()}`;
    
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
    console.error('Search doctors error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

