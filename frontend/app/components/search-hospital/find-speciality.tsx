'use client';

import { useState, useEffect, useRef } from 'react';
import { Stethoscope, Check, ChevronDown, Search } from 'lucide-react';

interface Specialty {
  EspecialidadId: string;
  Nombre: string;
  Descripcion?: string;
}

interface FindSpecialityProps {
  onSpecialtySelect?: (selectedSpecialties: string[]) => void;
  className?: string;
  maxSelections?: number;
}

export function FindSpeciality({ 
  onSpecialtySelect, 
  className,
  maxSelections = 3
}: FindSpecialityProps) {
  const [selectedSpecialties, setSelectedSpecialties] = useState<string[]>([]);
  const [specialties, setSpecialties] = useState<Specialty[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchSpecialties();
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
    if (onSpecialtySelect) {
      onSpecialtySelect(selectedSpecialties);
    }
  }, [selectedSpecialties, onSpecialtySelect]);

  const fetchSpecialties = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/especialidades');
      
      if (!response.ok) {
        throw new Error('Error al cargar las especialidades');
      }

      const data = await response.json();
      
      // Ensure we have valid data
      const items = data.items || data || [];
      
      // Normalize field names - handle both uppercase and lowercase
      const normalizedItems = items.map((item: any) => ({
        EspecialidadId: item.EspecialidadId || item.especialidadId,
        Nombre: item.Nombre || item.nombre,
        Descripcion: item.Descripcion || item.descripcion
      }));
      
      const validItems = normalizedItems.filter((item: any) => item && item.EspecialidadId && item.Nombre);
      
      setSpecialties(validItems);
      setError(null);
    } catch (err) {
      console.error('Error fetching specialties:', err);
      setError('No se pudieron cargar las especialidades');
      // Fallback con especialidades básicas
      setSpecialties([
        { EspecialidadId: 'MEDGEN', Nombre: 'Medicina General', Descripcion: 'Atención médica general' },
        { EspecialidadId: 'CARD', Nombre: 'Cardiología', Descripcion: 'Enfermedades del corazón' },
        { EspecialidadId: 'DERM', Nombre: 'Dermatología', Descripcion: 'Enfermedades de la piel' },
        { EspecialidadId: 'NEURO', Nombre: 'Neurología', Descripcion: 'Sistema nervioso' },
        { EspecialidadId: 'GINEC', Nombre: 'Ginecología', Descripcion: 'Salud femenina' },
        { EspecialidadId: 'TRAUM', Nombre: 'Traumatología', Descripcion: 'Lesiones del aparato locomotor' },
        { EspecialidadId: 'PEDIA', Nombre: 'Pediatría', Descripcion: 'Salud infantil' },
        { EspecialidadId: 'OFTAL', Nombre: 'Oftalmología', Descripcion: 'Salud visual' },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const toggleSpecialty = (specialtyId: string) => {
    setSelectedSpecialties((prev) => {
      let newSelection: string[];
      
      if (prev.includes(specialtyId)) {
        // Deseleccionar
        newSelection = prev.filter((id) => id !== specialtyId);
      } else {
        // Seleccionar (respetar límite máximo)
        if (prev.length >= maxSelections) {
          // Si ya alcanzó el máximo, reemplazar el más antiguo
          newSelection = [...prev.slice(1), specialtyId];
        } else {
          newSelection = [...prev, specialtyId];
        }
      }
      
      return newSelection;
    });
  };

  const clearAll = () => {
    setSelectedSpecialties([]);
  };

  // Filtrar especialidades por término de búsqueda
  const filteredSpecialties = specialties.filter(specialty => {
    if (!specialty || !specialty.Nombre) return false;
    
    const lowerSearchTerm = searchTerm.toLowerCase();
    const nameMatch = specialty.Nombre.toLowerCase().includes(lowerSearchTerm);
    const descriptionMatch = specialty.Descripcion?.toLowerCase().includes(lowerSearchTerm) || false;
    
    return nameMatch || descriptionMatch;
  });

  return (
    <div className={`relative ${className}`} ref={dropdownRef}>
      <div className="relative">
        <Stethoscope className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none z-10" />
        <div 
          className="w-full h-12 pl-11 pr-10 bg-white/50 hover:bg-white/70 focus-within:bg-white rounded-lg border border-gray-200/50 transition-colors focus-within:ring-2 focus-within:ring-gray-900/10 flex items-center cursor-text"
          onClick={() => !loading && setIsOpen(true)}
        >
          <div className="flex-1 overflow-hidden">
            {loading ? (
              <span className="text-gray-400 text-sm">Cargando...</span>
            ) : selectedSpecialties.length === 0 ? (
              <span className="text-gray-400 text-sm">Especialidad</span>
            ) : selectedSpecialties.length === 1 ? (
              <span className="text-gray-900 font-medium text-sm truncate">
                {specialties.find(s => s.EspecialidadId === selectedSpecialties[0])?.Nombre}
              </span>
            ) : (
              <span className="text-gray-900 font-medium text-sm">
                {selectedSpecialties.length} especialidades
              </span>
            )}
          </div>
          {selectedSpecialties.length > 0 && !loading && (
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                clearAll();
              }}
              className="absolute right-10 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-900 transition-colors z-10"
              title="Limpiar"
            >
              <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>
        <ChevronDown className={`absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400 transition-transform pointer-events-none ${isOpen ? 'rotate-180' : ''}`} />
      </div>

      {/* Dropdown Menu */}
      {isOpen && !loading && (
        <div className="absolute z-50 w-full mt-2 bg-white rounded-lg shadow-xl border border-gray-200/50 overflow-hidden backdrop-blur-md">
          {/* Search Input */}
          <div className="p-3 border-b border-gray-200">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Buscar especialidad..."
                className="w-full pl-10 pr-4 py-2 bg-gray-50 rounded-lg border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900/10 text-gray-900 placeholder:text-gray-400"
                autoFocus
              />
            </div>
          </div>

          {/* Selection Counter */}
          {selectedSpecialties.length > 0 && (
            <div className="bg-gray-50 border-b border-gray-200 px-4 py-2 flex justify-between items-center">
              <span className="text-sm text-gray-600 font-medium">
                {selectedSpecialties.length} seleccionada{selectedSpecialties.length !== 1 ? 's' : ''}
                {maxSelections && <span className="text-gray-500"> / {maxSelections} máx.</span>}
              </span>
              <button
                onClick={clearAll}
                className="text-sm text-gray-900 hover:text-gray-700 transition-colors font-medium"
              >
                Limpiar
              </button>
            </div>
          )}

          {/* Specialty Options */}
          <div className="max-h-80 overflow-y-auto p-2">
            {filteredSpecialties.length === 0 && (
              <div className="text-center py-8 text-gray-500 text-sm">
                {searchTerm ? (
                  <>No se encontraron especialidades</>
                ) : (
                  <>No hay especialidades disponibles</>
                )}
              </div>
            )}
            
            {filteredSpecialties.map((specialty) => {
              if (!specialty || !specialty.EspecialidadId) return null;
              
              const isSelected = selectedSpecialties.includes(specialty.EspecialidadId);
              const isMaxReached = selectedSpecialties.length >= maxSelections && !isSelected;
              
              return (
                <button
                  key={specialty.EspecialidadId}
                  type="button"
                  onClick={() => toggleSpecialty(specialty.EspecialidadId)}
                  disabled={isMaxReached}
                  className={`
                    w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all
                    ${
                      isSelected
                        ? 'bg-gray-900 text-white hover:bg-gray-800'
                        : isMaxReached
                        ? 'opacity-40 cursor-not-allowed'
                        : 'text-gray-700 hover:bg-gray-50'
                    }
                  `}
                  title={specialty.Descripcion || specialty.Nombre || 'Especialidad'}
                >
                  {/* Specialty Name */}
                  <div className="flex-1 text-left min-w-0">
                    <span className={`text-sm font-medium block ${isSelected ? 'text-white' : 'text-gray-700'}`}>
                      {specialty.Nombre || 'Sin nombre'}
                    </span>
                    {specialty.Descripcion && (
                      <span className={`text-xs block mt-0.5 line-clamp-1 ${isSelected ? 'text-gray-300' : 'text-gray-500'}`}>
                        {specialty.Descripcion}
                      </span>
                    )}
                  </div>

                  {/* Checkbox Indicator */}
                  <div
                    className={`
                      flex items-center justify-center w-5 h-5 rounded border-2 flex-shrink-0 transition-colors
                      ${
                        isSelected
                          ? 'bg-white border-white'
                          : 'bg-white border-gray-300'
                      }
                    `}
                  >
                    {isSelected && <Check className="w-3 h-3 text-gray-900" />}
                  </div>
                </button>
              );
            })}
          </div>

          {/* Error message */}
          {error && (
            <div className="bg-gray-50 border-t border-gray-200 px-4 py-2">
              <p className="text-sm text-gray-600">
                {error}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

