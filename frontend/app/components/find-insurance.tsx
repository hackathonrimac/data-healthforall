'use client';

import { useState, useRef, useEffect } from 'react';
import { Shield, Check, ChevronDown } from 'lucide-react';

interface InsuranceCompany {
  id: string;
  name: string;
  logo: string;
  color: string;
}

const INSURANCE_COMPANIES: InsuranceCompany[] = [
  {
    id: 'RIMAC',
    name: 'RIMAC Seguros',
    logo: '🛡️',
    color: 'bg-red-500',
  },
  {
    id: 'PACIFICO',
    name: 'Pacífico Seguros',
    logo: '🌊',
    color: 'bg-blue-600',
  },
  {
    id: 'SURA',
    name: 'SURA',
    logo: '🔷',
    color: 'bg-teal-600',
  },
  {
    id: 'LA_POSITIVA',
    name: 'La Positiva Seguros',
    logo: '✨',
    color: 'bg-orange-500',
  },
  {
    id: 'MAPFRE',
    name: 'MAPFRE',
    logo: '🏥',
    color: 'bg-red-700',
  },
  {
    id: 'ESSALUD',
    name: 'EsSalud',
    logo: '🏛️',
    color: 'bg-green-600',
  },
];

interface FindInsuranceProps {
  onInsuranceSelect?: (selectedInsurances: string[]) => void;
  className?: string;
}

export function FindInsurance({ onInsuranceSelect, className }: FindInsuranceProps) {
  const [selectedInsurances, setSelectedInsurances] = useState<string[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

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
          className="w-full px-4 py-2 bg-white/50 hover:bg-white/70 focus:bg-white rounded-lg border border-gray-200/50 text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500/20 text-left flex items-center justify-between gap-2"
        >
          <div className="flex-1 flex items-center gap-2 overflow-hidden">
            {selectedInsurances.length === 0 && (
              <span className="text-gray-400">Selecciona tus seguros</span>
            )}
            {selectedInsurances.length > 0 && selectedInsurances.length <= 2 && (
              <div className="flex items-center gap-2 flex-wrap">
                {selectedInsurances.map((insuranceId) => {
                  const insurance = INSURANCE_COMPANIES.find(i => i.id === insuranceId);
                  if (!insurance) return null;
                  return (
                    <span
                      key={insuranceId}
                      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium text-white ${insurance.color}`}
                    >
                      <span>{insurance.logo}</span>
                      <span>{insurance.name}</span>
                    </span>
                  );
                })}
              </div>
            )}
            {selectedInsurances.length > 2 && (
              <span className="text-gray-900">
                {selectedInsurances.length} seguros seleccionados
              </span>
            )}
          </div>
          <ChevronDown className={`w-4 h-4 text-gray-400 transition-transform flex-shrink-0 ${isOpen ? 'rotate-180' : ''}`} />
        </button>

        {/* Dropdown Menu */}
        {isOpen && (
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
              {INSURANCE_COMPANIES.map((insurance) => {
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
                    {/* Insurance Logo */}
                    <div
                      className={`
                        flex items-center justify-center w-10 h-10 rounded-lg
                        ${insurance.color} text-white text-xl flex-shrink-0
                      `}
                    >
                      {insurance.logo}
                    </div>

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
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

