'use client';

import { useState, useRef, useEffect } from 'react';
import { Shield, Check, ChevronDown } from 'lucide-react';

interface InsuranceCompany {
  id: string;
  name: string;
  descripcion?: string;
}

interface FindInsuranceProps {
  onInsuranceSelect?: (selectedInsurances: string[]) => void;
  selectedInsurances?: string[];
  className?: string;
}

export function FindInsurance({ 
  onInsuranceSelect, 
  selectedInsurances: initialSelectedInsurances = [],
  className 
}: FindInsuranceProps) {
  const [selectedInsurances, setSelectedInsurances] = useState<string[]>(initialSelectedInsurances);
  const [isOpen, setIsOpen] = useState(false);
  const [insuranceCompanies, setInsuranceCompanies] = useState<InsuranceCompany[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Update internal state when selectedInsurances prop changes
  useEffect(() => {
    setSelectedInsurances(initialSelectedInsurances);
  }, [initialSelectedInsurances]);

  // Fetch insurance companies from API
  useEffect(() => {
    const fetchInsuranceCompanies = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        const response = await fetch('/api/seguros');
        
        if (!response.ok) {
          throw new Error('Failed to fetch insurance companies');
        }
        
        const data = await response.json();
        
        // Ensure we have valid data - handle different possible structures
        const items = data.seguros || data.items || data || [];
        
        // Normalize field names - handle both uppercase and lowercase
        const normalizedItems = Array.isArray(items) ? items.map((item: any) => ({
          id: item.seguroId || item.SeguroId || item.id,
          name: item.nombre || item.Nombre || item.name,
          descripcion: item.descripcion || item.Descripcion
        })) : [];
        
        // Filter out invalid entries
        const validItems = normalizedItems.filter((item: any) => item && item.id && item.name);
        
        setInsuranceCompanies(validItems);
        setError(null);
      } catch (err) {
        console.error('Error fetching insurance companies:', err);
        setError('No se pudieron cargar los seguros');
        // Fallback with basic insurance companies
        setInsuranceCompanies([
          { id: 'RIMAC', name: 'RIMAC Seguros' },
          { id: 'PACIFICO', name: 'Pacífico Seguros' },
          { id: 'MAPFRE', name: 'MAPFRE Seguros' },
          { id: 'SANITAS', name: 'Sanitas Perú' },
        ]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchInsuranceCompanies();
  }, []);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  // Notify parent component when selection changes
  useEffect(() => {
    if (onInsuranceSelect) {
      onInsuranceSelect(selectedInsurances);
    }
  }, [selectedInsurances, onInsuranceSelect]);

  const toggleInsurance = (insuranceId: string) => {
    setSelectedInsurances((prev) => {
      const newSelection = prev.includes(insuranceId)
        ? prev.filter((id) => id !== insuranceId)
        : [...prev, insuranceId];
      
      return newSelection;
    });
  };

  const clearAll = () => {
    setSelectedInsurances([]);
  };

  return (
    <div className={`relative ${className}`} ref={dropdownRef}>
      <div className="relative">
        <Shield className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none z-10" />
        <button
          type="button"
          onClick={() => setIsOpen(!isOpen)}
          disabled={isLoading}
          className="w-full h-12 pl-11 pr-10 bg-white/50 hover:bg-white/70 focus:bg-white rounded-lg border border-gray-200/50 text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-gray-900/10 text-left flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <div className="flex-1 overflow-hidden">
            {isLoading && (
              <span className="text-gray-400">Cargando seguros...</span>
            )}
            {!isLoading && error && (
              <span className="text-red-500 text-sm">{error}</span>
            )}
            {!isLoading && !error && selectedInsurances.length === 0 && (
              <span className="text-gray-400">Seguro</span>
            )}
            {!isLoading && !error && selectedInsurances.length === 1 && (
              <span className="text-gray-900 font-medium truncate">
                {insuranceCompanies.find(i => i.id === selectedInsurances[0])?.name}
              </span>
            )}
            {!isLoading && !error && selectedInsurances.length > 1 && (
              <span className="text-gray-900 font-medium">
                {selectedInsurances.length} seguros
              </span>
            )}
          </div>
        </button>
        <ChevronDown className={`absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 transition-transform pointer-events-none ${isOpen ? 'rotate-180' : ''}`} />
      </div>

      {/* Dropdown Menu */}
      {isOpen && !isLoading && !error && (
        <div className="absolute z-[100] w-full mt-2 bg-white rounded-lg shadow-xl border border-gray-200/50 max-h-96 overflow-hidden backdrop-blur-md">
          {/* Clear All Button */}
          {selectedInsurances.length > 0 && (
            <div className="sticky top-0 bg-gray-50 border-b border-gray-200 px-4 py-2 flex justify-between items-center">
              <span className="text-sm text-gray-600 font-medium">
                {selectedInsurances.length} seleccionado{selectedInsurances.length !== 1 ? 's' : ''}
              </span>
              <button
                onClick={clearAll}
                className="text-sm text-gray-700 hover:text-gray-500 transition-colors font-medium"
              >
                Limpiar
              </button>
            </div>
          )}

          {/* Insurance Options */}
          <div className="max-h-80 overflow-y-auto p-2">
            {insuranceCompanies.length === 0 ? (
              <div className="px-4 py-3 text-sm text-gray-500 text-center">
                No hay seguros disponibles
              </div>
            ) : (
              insuranceCompanies.map((insurance) => {
                const isSelected = selectedInsurances.includes(insurance.id);
                
                return (
                  <button
                    key={insurance.id}
                    type="button"
                    onClick={() => toggleInsurance(insurance.id)}
                    className={`
                      w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all
                      ${
                        isSelected
                          ? ''
                          : 'text-gray-700 hover:bg-gray-100'
                      }
                    `}
                  >
                    {/* Insurance Name */}
                    <div className="flex-1 text-left">
                      <span className={`text-sm font-medium ${isSelected ? 'text-gray-900' : 'text-gray-700'}`}>
                        {insurance.name}
                      </span>
                    </div>

                    {/* Checkbox Indicator */}
                    <div
                      className={`
                        flex items-center justify-center w-5 h-5 rounded border-2 flex-shrink-0
                        ${
                          isSelected
                            ? 'bg-gray-900 border-gray-900'
                            : 'bg-white border-gray-300'
                        }
                      `}
                    >
                      {isSelected && <Check className="w-3 h-3 text-white" />}
                    </div>
                  </button>
                );
              })
            )}
          </div>
        </div>
      )}
    </div>
  );
}

