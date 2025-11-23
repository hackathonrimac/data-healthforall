'use client';

import { useState, useEffect, useRef } from 'react';
import { experimental_useObject as useObject } from '@ai-sdk/react';
import { Send, AlertCircle, Stethoscope, Info, Loader2, CheckCircle2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';
import { Textarea } from '@/app/components/ui/textarea';
import { Button } from '@/app/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/app/components/ui/dialog';
import { symptomsSchema } from '@/lib/types/symptoms-object';

interface SearchSymptomsProps {
  onSpecialtySelected: (specialtyId: string, specialtyName: string) => void;
}

const TIMEOUT_DURATION = 30000; // 30 seconds

export function SearchSymptoms({ onSpecialtySelected }: SearchSymptomsProps) {
  const [input, setInput] = useState('');
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  const [isTimedOut, setIsTimedOut] = useState(false);
  
  const { object, submit, isLoading, error, stop } = useObject({
    api: '/api/symptoms',
    schema: symptomsSchema,
  });

  const handleSubmit = () => {
    if (!input.trim() || isLoading) return;

    setIsTimedOut(false);
    
    // Set timeout for the request
    timeoutRef.current = setTimeout(() => {
      if (isLoading) {
        setIsTimedOut(true);
        stop?.();
        toast.error('Servicio no disponible', {
          description: 'El análisis de síntomas no está disponible en este momento. Por favor, intenta más tarde o busca directamente por especialidad.',
          duration: 6000,
        });
      }
    }, TIMEOUT_DURATION);

    submit({ symptoms: input.trim() });
  };

  // Clear timeout when loading completes
  useEffect(() => {
    if (!isLoading && timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
  }, [isLoading]);

  // Cleanup timeout on unmount
  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  // Handle errors with toast notification
  useEffect(() => {
    if (error && !isTimedOut) {
      toast.error('Servicio no disponible', {
        description: 'El servicio de análisis de síntomas no está disponible. Por favor, intenta más tarde o busca directamente por especialidad.',
        duration: 6000,
      });
    }
  }, [error, isTimedOut]);

  // Only open dialog when object is fully loaded
  useEffect(() => {
    if (!isLoading && object?.especialidadId && object?.especialidadNombre && object?.explicacion && !isTimedOut) {
      setIsDialogOpen(true);
    }
  }, [isLoading, object, isTimedOut]);

  const handleAcceptDialog = () => {
    setIsDialogOpen(false);
    
    // Directly transition to search view with specialty pre-filled
    if (object?.especialidadId && object?.especialidadNombre) {
      onSpecialtySelected(object.especialidadId, object.especialidadNombre);
    }
  };

  const getUrgencyColor = (urgency: string) => {
    switch (urgency) {
      case 'alta':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'media':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'baja':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getUrgencyLabel = (urgency: string) => {
    switch (urgency) {
      case 'alta':
        return 'Urgencia Alta - Busca atención inmediata';
      case 'media':
        return 'Urgencia Media - Consulta en los próximos días';
      case 'baja':
        return 'Urgencia Baja - Puedes programar una cita';
      default:
        return urgency;
    }
  };

  return (
    <div className="w-full max-w-3xl mx-auto space-y-6">
      {/* Unified Input - Single Component */}
      <div className="relative flex items-center bg-white/50 rounded-xl shadow-sm overflow-hidden">
        <Textarea
          id="symptoms"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ej: Tengo dolor en el pecho al hacer ejercicio, me siento cansado y tengo palpitaciones..."
          className="flex-1 h-[60px] max-h-[60px] resize-none text-gray-900 placeholder:text-gray-400 bg-transparent border-none focus:border-none focus:ring-0 text-base py-3 px-5 pr-16"
          disabled={isLoading}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey && !isLoading && input.trim()) {
              e.preventDefault();
              handleSubmit();
            }
          }}
        />
        
        <Button
          type="button"
          onClick={handleSubmit}
          disabled={isLoading || !input.trim()}
          className="absolute right-2 top-1/2 -translate-y-1/2 h-10 w-auto rounded-lg"
        >
          {isLoading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              <span>Analizando...</span>
            </>
          ) : (
            <>
              <Send className="h-4 w-4" />
              <span>Preguntar</span>
            </>
          )}
        </Button>
      </div>

      {/* Info Display - Removed error display as we're using toast */}

      {/* Results Dialog with Animations */}
      <AnimatePresence>
        {isDialogOpen && object && (
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.4 }}
            >
              <DialogContent className="max-w-2xl overflow-hidden">
                <DialogHeader>
                  <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2, duration: 0.6 }}
                  >
                    <DialogTitle className="flex items-center gap-2 text-xl py-2">
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: 0.4, type: "spring", stiffness: 150 }}
                      >
                        <CheckCircle2 className="w-6 h-6 text-green-600" />
                      </motion.div>
                      Especialidad Recomendada
                    </DialogTitle>
                  </motion.div>
                </DialogHeader>
                
                <div className="space-y-5 px-6 pb-6">
                  {/* Specialty Name - Animated */}
                  {object.especialidadNombre && (
                    <motion.div
                      initial={{ opacity: 0, scale: 0.9, y: 20 }}
                      animate={{ opacity: 1, scale: 1, y: 0 }}
                      transition={{ delay: 0.5, duration: 0.8, type: "spring" }}
                      className="relative overflow-hidden py-2"
                    >
                      <motion.div
                        className="absolute inset-0 bg-gradient-to-r from-blue-400/20 via-blue-500/20 to-blue-400/20"
                        animate={{
                          x: ['-100%', '100%'],
                        }}
                        transition={{
                          duration: 3,
                          ease: "easeInOut",
                          times: [0, 1],
                        }}
                      />
                      <div className="relative p-6 bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl border-2 border-blue-200 shadow-sm">
                        <div className="flex items-center gap-3">
                          <Stethoscope className="w-8 h-8 text-blue-600" />
                          <p className="text-2xl font-bold text-blue-900">
                            {object.especialidadNombre}
                          </p>
                        </div>
                      </div>
                    </motion.div>
                  )}

                  {/* Urgency Level - Animated */}
                  {object.urgencia && (
                    <motion.div
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.8, duration: 0.6 }}
                      className={`p-4 rounded-xl border-2 ${getUrgencyColor(object.urgencia)} flex items-center gap-3 shadow-sm`}
                    >
                      <motion.div
                        animate={{ 
                          scale: [1, 1.2, 1],
                        }}
                        transition={{ 
                          duration: 3,
                          repeat: Infinity,
                          repeatType: "reverse"
                        }}
                      >
                        <Info className="w-5 h-5 flex-shrink-0" />
                      </motion.div>
                      <span className="text-sm font-semibold">
                        {getUrgencyLabel(object.urgencia)}
                      </span>
                    </motion.div>
                  )}

                  {/* Explanation - Animated */}
                  {object.explicacion && (
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 1.0, duration: 0.6 }}
                      className="space-y-3 p-4 bg-gray-50 rounded-xl"
                    >
                      <h4 className="text-sm font-bold text-gray-700 flex items-center gap-2">
                        <motion.div
                          animate={{ rotate: [0, 10, -10, 0] }}
                          transition={{ delay: 1.3, duration: 0.8 }}
                        >
                          💡
                        </motion.div>
                        ¿Por qué esta especialidad?
                      </h4>
                      <p className="text-gray-900 leading-relaxed">
                        {object.explicacion}
                      </p>
                    </motion.div>
                  )}

                  {/* Disclaimer */}
                  <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 1.3, duration: 0.6 }}
                    className="pt-3 border-t border-gray-200"
                  >
                    <p className="text-xs text-gray-500 italic">
                      * Esta es una recomendación orientativa basada en tus síntomas. No reemplaza una evaluación médica profesional. 
                      Si tienes síntomas graves, busca atención médica inmediata.
                    </p>
                  </motion.div>

                  {/* Accept Button - Animated */}
                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 1.5, duration: 0.6 }}
                    className="pt-4"
                  >
                    <Button 
                      onClick={handleAcceptDialog} 
                      className="w-full group" 
                      size="lg"
                    >
                      <span>Continuar</span>
                      <motion.span
                        className="ml-2"
                        animate={{ x: [0, 5, 0] }}
                        transition={{ 
                          duration: 2,
                          repeat: Infinity,
                          repeatType: "reverse"
                        }}
                      >
                        →
                      </motion.span>
                    </Button>
                  </motion.div>
                </div>
              </DialogContent>
            </motion.div>
          </Dialog>
        )}
      </AnimatePresence>

    </div>
  );
}

