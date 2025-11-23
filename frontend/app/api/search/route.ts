import { bedrock } from '@ai-sdk/amazon-bedrock';
import { streamObject } from 'ai';
import { z } from 'zod';

export const runtime = 'edge';


export const SEARCH_PROMPT = `
Eres un asistente de búsqueda médica que extrae información estructurada de consultas de usuarios en español.

Tu tarea es extraer la especialidad médica y la ubicación (distrito de Lima Metropolitana o Callao) mencionadas en la consulta.

Responde SIEMPRE en español y con un tono conciso y útil.

Requisitos para extraer la información:
- La especialidad médica debe ser una especialidad médica válida y debe ser estar bien escrita. EJ. "Cardiología", "Pediatría", "Neurología", etc.
- La ubicación debe ser un distrito de Lima Metropolitana o Callao y debe ser estar bien escrita. EJ. "Lima", "Lince", "Miraflores", "San Isidro", etc.
- El texto debe ser una respuesta al usuario con la información encontrada.

INDICACIONES PARA RESPONDER AL USUARIO: 
- No uses emojis.
- Utiliza un tono amable y profesional.
- No uses comillas dobles en el texto de respuesta.

Devuelve la información en el siguiente formato JSON:
{
  "especialidad": "string",
  "distrito": "string",
  "texto": "string"
}

Si la información no se menciona explícitamente, infiere según el contexto o deja el campo vacío.
`;



const searchSchema = z.object({
  especialidad: z.string().describe('La especialidad médica extraída de la consulta'),
  distrito: z.string().describe('El distrito de Lima Metropolitana o Callao extraído de la consulta'),
  texto: z.string().describe('El texto de respuesta al usuario con la información encontrada'),
});

export async function POST(req: Request) {
  const context = await req.json();

  const result = streamObject({
    model: bedrock('us.anthropic.claude-sonnet-4-20250514-v1:0'),
    schema: searchSchema,
    system: SEARCH_PROMPT,
    prompt: context,
  });

  return result.toTextStreamResponse();
}

