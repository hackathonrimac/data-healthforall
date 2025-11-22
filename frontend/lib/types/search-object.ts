import { z } from 'zod';

export const searchSchema = z.object({
    especialidad: z.string().describe('La especialidad médica extraída de la consulta').nullable(),
    distrito: z.string().describe('El distrito de Lima Metropolitana o Callao extraído de la consulta').nullable(),
    texto: z.string().describe('El texto de respuesta al usuario con la información encontrada'),
  });