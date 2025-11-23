'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { useState, useEffect } from 'react';

const callToActions = [
  "Salud digital sin complicaciones",
  "Encuentra tu especialista en segundos",
  "Información confiable, pacientes felices"
];

export function Title() {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % callToActions.length);
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative w-full overflow-hidden py-4">
      <div className="max-w-5xl mx-auto px-4">
        {/* Main animated title */}
        <div className="text-center space-y-3">
          {/* Static top text */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
          >
            <span className="inline-block text-xs md:text-sm font-bold text-blue-600 tracking-widest uppercase bg-blue-50 px-3 py-1 rounded-full">
              HealthForAll Beta
            </span>
          </motion.div>

          {/* Animated rotating text */}
          <div className="relative h-[60px] md:h-[70px] flex items-center justify-center">
            <AnimatePresence mode="wait">
              <motion.h1
                key={currentIndex}
                initial={{ opacity: 0, y: 20, scale: 0.98 }}
                animate={{ 
                  opacity: 1, 
                  y: 0, 
                  scale: 1,
                }}
                exit={{ 
                  opacity: 0, 
                  y: -20, 
                  scale: 0.98,
                }}
                transition={{ 
                  duration: 0.6,
                  ease: "easeOut"
                }}
                className="absolute inset-0 flex items-center justify-center text-2xl md:text-4xl lg:text-5xl font-extrabold text-gray-900 px-4 tracking-tight"
              >
                <span className="bg-gradient-to-r from-slate-900 via-blue-900 to-slate-900 bg-clip-text text-transparent text-center leading-tight">
                  {callToActions[currentIndex]}
                </span>
              </motion.h1>
            </AnimatePresence>
          </div>

          {/* Supporting text */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="text-sm md:text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed pt-2"
          >
            Facilitamos el viaje del paciente con datos precisos, mejorando la accesibilidad y{' '}
            <span className="font-semibold text-gray-900">reduciendo la carga operativa</span> del sistema de salud.
          </motion.p>

          {/* Animated dots indicator */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="flex justify-center gap-2 pt-1"
          >
            {callToActions.map((_, index) => (
              <motion.div
                key={index}
                className={`h-1.5 rounded-full transition-all duration-500 ${
                  index === currentIndex 
                    ? 'w-8 bg-gray-900' 
                    : 'w-1.5 bg-gray-300'
                }`}
                animate={{
                  scale: index === currentIndex ? 1 : 0.8,
                }}
              />
            ))}
          </motion.div>
        </div>
      </div>
    </div>
  );
}

