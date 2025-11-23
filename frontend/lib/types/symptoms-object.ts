import { z } from 'zod';

export const symptomsSchema = z.object({
  especialidadId: z.string().describe('El ID numérico de la especialidad médica recomendada según los síntomas'),
  especialidadNombre: z.string().describe('El nombre de la especialidad médica recomendada'),
  explicacion: z.string().describe('Explicación clara y concisa de por qué se recomienda esta especialidad'),
  urgencia: z.enum(['baja', 'media', 'alta']).describe('Nivel de urgencia recomendado: baja (consulta programada), media (días), alta (inmediato)'),
});

export type SymptomsResponse = z.infer<typeof symptomsSchema>;
