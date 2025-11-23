import { bedrock } from '@ai-sdk/amazon-bedrock';
import { streamObject } from 'ai';
import { symptomsSchema } from '@/lib/types/symptoms-object';

// Use nodejs runtime for better AWS SDK support
export const runtime = 'nodejs';
export const maxDuration = 30; // 30 seconds timeout

const AWS_BASE_URL = process.env.AWS_API_URL || process.env.NEXT_PUBLIC_API_URL || '';

async function fetchAvailableSpecialties() {
  if (!AWS_BASE_URL) {
    console.error('[Symptoms API] AWS_BASE_URL not configured');
    throw new Error('API endpoint not configured. Please contact support.');
  }

  try {
    const response = await fetch(`${AWS_BASE_URL}/especialidades`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      signal: AbortSignal.timeout(10000), // 10 second timeout for this call
    });

    if (!response.ok) {
      const error = await response.text();
      console.error('[Symptoms API] Failed to fetch specialties:', response.status, error);
      throw new Error(`Failed to fetch specialties: ${error}`);
    }

    const data = await response.json();
    const items = data.items || data || [];
    
    // Normalize field names - handle both uppercase and lowercase
    const normalizedItems = items.map((item: any) => ({
      id: item.EspecialidadId || item.especialidadId,
      nombre: item.Nombre || item.nombre,
      descripcion: item.Descripcion || item.descripcion
    }));
    
    // Filter valid items
    const validItems = normalizedItems.filter((item: any) => item.id && item.nombre);
    
    if (validItems.length === 0) {
      console.error('[Symptoms API] No valid specialties found');
      throw new Error('No specialties available');
    }
    
    return validItems;
  } catch (err) {
    console.error('[Symptoms API] Error fetching specialties:', err);
    throw err;
  }
}

function buildSystemPrompt(specialties: any[]) {
  const specialtyList = specialties
    .map(s => `- ID: ${s.id}, Nombre: "${s.nombre}"${s.descripcion ? `, Descripción: ${s.descripcion}` : ''}`)
    .join('\n');

  return `Eres un asistente médico virtual que ayuda a pacientes a identificar qué especialidad médica deben consultar según sus síntomas.

Tu tarea es analizar los síntomas del paciente y recomendar la especialidad médica más apropiada de la siguiente lista:

ESPECIALIDADES DISPONIBLES:
${specialtyList}

INSTRUCCIONES IMPORTANTES:
1. Analiza cuidadosamente los síntomas descritos por el paciente
2. Identifica la especialidad médica más apropiada de la lista anterior
3. DEBES usar EXACTAMENTE el ID numérico de la especialidad (por ejemplo: "8", "36", "44")
4. DEBES usar EXACTAMENTE el nombre de la especialidad como aparece en la lista
5. Proporciona una explicación clara y comprensible de por qué recomiendas esa especialidad
6. Evalúa el nivel de urgencia:
   - "baja": Síntomas leves que pueden esperar consulta programada (semanas)
   - "media": Síntomas que requieren atención en los próximos días
   - "alta": Síntomas que sugieren necesidad de atención inmediata o urgencia (horas)

CRITERIOS DE URGENCIA ALTA:
- Dolor de pecho intenso o dificultad para respirar
- Pérdida súbita de conciencia o convulsiones
- Sangrado abundante o incontrolable
- Traumatismo severo
- Síntomas de accidente cerebrovascular (confusión, parálisis, dificultad para hablar)
- Dolor abdominal agudo intenso
- Fiebre muy alta con síntomas graves

REGLAS CRÍTICAS:
- SOLO puedes recomendar especialidades de la lista proporcionada
- Usa el ID numérico EXACTO (como "8" para Cardiología, no "CARD")
- Escribe en español con tono profesional pero amable
- No uses emojis
- Sé conciso pero informativo en tu explicación (máximo 2-3 oraciones)
- Si los síntomas son muy generales o ambiguos, recomienda "Medicina Interna" (ID: "29") o "Medicina General Integral" (ID: "56")
- Si hay múltiples especialidades posibles, elige la más específica para los síntomas principales

FORMATO DE RESPUESTA:
{
  "especialidadId": "[ID numérico exacto de la lista]",
  "especialidadNombre": "[Nombre exacto de la especialidad]",
  "explicacion": "[Razón clara y concisa]",
  "urgencia": "[baja|media|alta]"
}

IMPORTANTE: Este es un sistema de orientación inicial. El resultado ayudará al paciente a encontrar el especialista adecuado, pero no reemplaza una evaluación médica profesional.`;
}

export async function POST(req: Request) {
  try {
    const { symptoms } = await req.json();

    if (!symptoms || typeof symptoms !== 'string' || symptoms.trim().length === 0) {
      console.warn('[Symptoms API] Empty symptoms received');
      return new Response(
        JSON.stringify({ error: 'Síntomas requeridos' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    console.log('[Symptoms API] Processing symptoms request');

    // Fetch available specialties from AWS
    const specialties = await fetchAvailableSpecialties();
    
    if (!specialties || specialties.length === 0) {
      console.error('[Symptoms API] No specialties available');
      return new Response(
        JSON.stringify({ error: 'No se pudieron cargar las especialidades disponibles' }),
        { status: 503, headers: { 'Content-Type': 'application/json' } }
      );
    }
    
    console.log('[Symptoms API] Loaded', specialties.length, 'specialties');

    // Verify AWS credentials are available for Bedrock
    if (!process.env.AWS_ACCESS_KEY_ID || !process.env.AWS_SECRET_ACCESS_KEY) {
      console.error('[Symptoms API] AWS credentials not configured');
      return new Response(
        JSON.stringify({ error: 'Servicio de IA no configurado' }),
        { status: 503, headers: { 'Content-Type': 'application/json' } }
      );
    }
    
    // Build dynamic system prompt with available specialties
    const systemPrompt = buildSystemPrompt(specialties);

    console.log('[Symptoms API] Calling Bedrock AI');
    const result = streamObject({
      model: bedrock('us.anthropic.claude-sonnet-4-20250514-v1:0'),
      schema: symptomsSchema,
      system: systemPrompt,
      prompt: `El paciente describe los siguientes síntomas:\n\n"${symptoms}"\n\nAnaliza estos síntomas y recomienda la especialidad médica más apropiada. Recuerda usar el ID numérico exacto y el nombre exacto de la especialidad.`,
    });

    return result.toTextStreamResponse();
  } catch (error) {
    console.error('[Symptoms API] Error processing symptoms:', error);
    
    // Check if it's a Bedrock-specific error
    const errorMessage = error instanceof Error ? error.message : 'Error procesando síntomas';
    const isBedrockError = errorMessage.toLowerCase().includes('bedrock') || 
                           errorMessage.toLowerCase().includes('credential') ||
                           errorMessage.toLowerCase().includes('access');
    
    return new Response(
      JSON.stringify({ 
        error: isBedrockError ? 'Servicio de análisis no disponible' : errorMessage
      }),
      { status: 503, headers: { 'Content-Type': 'application/json' } }
    );
  }
}
