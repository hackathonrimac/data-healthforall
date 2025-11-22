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
  className?: string;
}

export function FindInsurance({ onInsuranceSelect, className }: FindInsuranceProps) {
  const [selectedInsurances, setSelectedInsurances] = useState<string[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [insuranceCompanies, setInsuranceCompanies] = useState<InsuranceCompany[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);

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
    <div className={`flex items-center gap-3 ${className}`}>
      <Shield className="w-4 h-4 text-gray-400" />
      <div className="relative flex-1" ref={dropdownRef}>
        {/* Dropdown Button */}
        <button
          type="button"
          onClick={() => setIsOpen(!isOpen)}
          disabled={isLoading}
          className="w-full px-4 py-2 bg-white/50 hover:bg-white/70 focus:bg-white rounded-lg border border-gray-200/50 text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500/20 text-left flex items-center justify-between gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <div className="flex-1 flex items-center gap-2 overflow-hidden">
            {isLoading && (
              <span className="text-gray-400">Cargando seguros...</span>
            )}
            {!isLoading && error && (
              <span className="text-red-500 text-xs">{error}</span>
            )}
            {!isLoading && !error && selectedInsurances.length === 0 && (
              <span className="text-gray-400">Selecciona tus seguros</span>
            )}
            {!isLoading && !error && selectedInsurances.length > 0 && selectedInsurances.length <= 2 && (
              <div className="flex items-center gap-2 flex-wrap">
                {selectedInsurances.map((insuranceId) => {
                  const insurance = insuranceCompanies.find(i => i.id === insuranceId);
                  if (!insurance) return null;
                  return (
                    <span
                      key={insuranceId}
                      className="inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium text-gray-700"
                    >
                      <span>{insurance.name}</span>
                    </span>
                  );
                })}
              </div>
            )}
            {!isLoading && !error && selectedInsurances.length > 2 && (
              <span className="text-gray-900">
                {selectedInsurances.length} seguros seleccionados
              </span>
            )}
          </div>
          <ChevronDown className={`w-4 h-4 text-gray-400 transition-transform flex-shrink-0 ${isOpen ? 'rotate-180' : ''}`} />
        </button>

        {/* Dropdown Menu */}
        {isOpen && !isLoading && !error && (
          <div className="absolute z-50 w-full mt-1 bg-white rounded-lg shadow-lg border border-gray-200 max-h-96 overflow-y-auto">
            {/* Clear All Button */}
            {selectedInsurances.length > 0 && (
              <div className="sticky top-0 bg-white border-b border-gray-200 px-4 py-2 flex justify-between items-center">
                <span className="text-xs text-gray-600">
                  {selectedInsurances.length} seleccionado{selectedInsurances.length !== 1 ? 's' : ''}
                </span>
                <button
                  onClick={clearAll}
                  className="text-xs text-blue-600 hover:text-blue-700 transition-colors font-medium"
                >
                  Limpiar todo
                </button>
              </div>
            )}

            {/* Insurance Options */}
            <div className="p-2 space-y-1">
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
                        w-full flex items-center gap-3 p-3 rounded-lg transition-all
                        ${
                          isSelected
                            ? 'bg-blue-50 hover:bg-blue-100'
                            : 'hover:bg-gray-50'
                        }
                      `}
                    >
                      {/* Insurance Name */}
                      <div className="flex-1 text-left">
                        <span className={`text-sm font-medium ${isSelected ? 'text-blue-900' : 'text-gray-700'}`}>
                          {insurance.name}
                        </span>
                      </div>

                      {/* Checkbox Indicator */}
                      <div
                        className={`
                          flex items-center justify-center w-5 h-5 rounded border-2 flex-shrink-0
                          ${
                            isSelected
                              ? 'bg-blue-500 border-blue-500'
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
    </div>
  );
}

