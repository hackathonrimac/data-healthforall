import { bedrock } from '@ai-sdk/amazon-bedrock';
import { streamText } from 'ai';

export const runtime = 'edge';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: bedrock('us.anthropic.claude-sonnet-4-20250514-v1:0'),
    messages,
    system: `Eres un asistente médico especializado en ayudar a pacientes a encontrar información sobre doctores, clínicas, especialidades y seguros médicos en Perú.

Tu rol es:
- Ayudar a los usuarios a buscar doctores por especialidad, clínica o seguro
- Proporcionar información sobre clínicas y sus ubicaciones
- Explicar diferentes especialidades médicas
- Orientar sobre seguros médicos y cobertura

Sé amable, profesional y conciso en tus respuestas.`,
  });

  return result.toTextStreamResponse();
}

