'use client';

import { motion, useMotionValue, useTransform, animate } from 'framer-motion';
import { useEffect, useRef, useState } from 'react';

interface MetricCardProps {
  value: string;
  label: string;
  delay: number;
  suffix?: string;
}

function MetricCard({ value, label, delay, suffix = '' }: MetricCardProps) {
  const [isVisible, setIsVisible] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  const count = useMotionValue(0);
  
  // Check if value is numeric
  const isNumeric = !isNaN(parseInt(value));
  
  const rounded = useTransform(count, (latest) => {
    const num = Math.round(latest);
    return suffix ? `${num}${suffix}` : num.toString();
  });

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
        }
      },
      { threshold: 0.2 }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    if (isVisible && isNumeric) {
      const numericValue = parseInt(value.replace(/[^0-9]/g, ''));
      const controls = animate(count, numericValue, {
        duration: 2.5,
        ease: [0.43, 0.13, 0.23, 0.96],
        delay: delay,
      });

      return controls.stop;
    }
  }, [isVisible, count, value, delay, isNumeric]);

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 30, scale: 0.9 }}
      animate={isVisible ? { opacity: 1, y: 0, scale: 1 } : {}}
      transition={{
        duration: 0.8,
        delay: delay,
        ease: [0.43, 0.13, 0.23, 0.96]
      }}
      className="relative group"
    >
      {/* Glass card */}
      <div className="relative bg-white/70 backdrop-blur-md border border-white/20 shadow-xl rounded-2xl p-4 overflow-hidden transition-all duration-300 hover:shadow-2xl hover:scale-[1.02]">
        {/* Gradient overlay on hover - subtle blue */}
        <motion.div
          className="absolute inset-0 bg-gradient-to-br from-blue-50/30 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"
          initial={false}
        />

        {/* Content */}
        <div className="relative z-10 space-y-1">
          {/* Animated number or text */}
          <motion.div className="text-3xl md:text-4xl font-bold text-gray-900 tracking-tight">
            <motion.span className="bg-gradient-to-r from-gray-900 via-gray-700 to-gray-900 bg-clip-text text-transparent">
              {isNumeric ? rounded : value}
            </motion.span>
          </motion.div>

          {/* Label */}
          <div className="text-xs md:text-sm font-medium text-gray-600 leading-snug">
            {label}
          </div>
        </div>
      </div>

      {/* Subtle glow effect on hover - blue only */}
      <motion.div
        className="absolute inset-0 -z-10 bg-blue-100/40 rounded-2xl blur-xl opacity-0 group-hover:opacity-50 transition-opacity duration-500"
        initial={false}
      />
    </motion.div>
  );
}

export function Metrics() {
  return (
    <div className="w-full py-3">
      <div className="max-w-7xl mx-auto px-4">
        {/* Section header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-4"
        >
          <h2 className="text-lg md:text-xl font-bold text-gray-900 mb-1">
            Impacto Real en el Ecosistema
          </h2>
          <p className="text-xs md:text-sm text-gray-600 max-w-2xl mx-auto">
            Datos estructurados para una toma de decisiones más ágil y una red de salud más integrada
          </p>
        </motion.div>

        {/* Metrics grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 md:gap-4">
          <MetricCard
            value="30000"
            label="Especialistas Verificados"
            delay={0.1}
            suffix="+"
          />
          <MetricCard
            value="50"
            label="Centros de Salud Aliados"
            delay={0.3}
            suffix="+"
          />
          <MetricCard
            value="100"
            label="Transparencia y Acceso Libre"
            delay={0.5}
            suffix="%"
          />
        </div>
      </div>
    </div>
  );
}

