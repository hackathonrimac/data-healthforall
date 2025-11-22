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
    <div className={`flex items-center gap-3 ${className}`}>
      <Stethoscope className="w-4 h-4 text-gray-400" />
      <div className="relative flex-1" ref={dropdownRef}>
        {/* Input with Selected Chips */}
        <div className="relative">
          <div className="w-full min-h-[42px] px-3 py-2 bg-white/50 hover:bg-white/70 focus-within:bg-white rounded-lg border border-gray-200/50 transition-colors focus-within:ring-2 focus-within:ring-black/10">
            <div className="flex items-center gap-2 flex-wrap">
              {/* Search Icon */}
              <Search className="w-4 h-4 text-gray-400 flex-shrink-0" />
              
              {/* Selected Specialty Chips */}
              {selectedSpecialties.map((specialtyId) => {
                const specialty = specialties.find(s => s.EspecialidadId === specialtyId);
                if (!specialty) return null;
                return (
                  <span
                    key={specialtyId}
                    className="inline-flex items-center gap-1.5 px-2 py-1 text-xs font-medium text-white bg-black rounded"
                  >
                    <span>{specialty.Nombre}</span>
                    <button
                      type="button"
                      onClick={(e) => {
                        e.stopPropagation();
                        toggleSpecialty(specialtyId);
                      }}
                      className="ml-1 hover:bg-gray-700 rounded-full transition-colors"
                    >
                      <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </span>
                );
              })}
              
              {/* Input Field */}
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                onFocus={() => setIsOpen(true)}
                placeholder={selectedSpecialties.length === 0 ? "Buscar especialidad..." : ""}
                disabled={loading}
                className="flex-1 min-w-[120px] bg-transparent border-none outline-none text-xs text-gray-900 placeholder:text-gray-400"
              />
              
              {/* Loading/Chevron Icon */}
              <div className="flex items-center gap-2 flex-shrink-0">
                {selectedSpecialties.length > 0 && (
                  <button
                    type="button"
                    onClick={clearAll}
                    className="text-gray-400 hover:text-black transition-colors"
                    title="Limpiar todo"
                  >
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                )}
                <ChevronDown className={`w-4 h-4 text-gray-400 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
              </div>
            </div>
          </div>
        </div>

        {/* Dropdown Menu */}
        {isOpen && !loading && (
          <div className="absolute z-50 w-full mt-1 bg-white rounded-lg shadow-lg border border-gray-200 max-h-80 overflow-hidden">
            {/* Selection Counter */}
            {selectedSpecialties.length > 0 && (
              <div className="bg-gray-100 border-b border-gray-200 px-4 py-2 flex justify-between items-center">
                <span className="text-xs text-black font-medium">
                  {selectedSpecialties.length} seleccionada{selectedSpecialties.length !== 1 ? 's' : ''}
                  {maxSelections && <span className="text-gray-600"> / {maxSelections} máx.</span>}
                </span>
              </div>
            )}

            {/* Specialty Options */}
            <div className="max-h-64 overflow-y-auto p-2 space-y-1">
              {filteredSpecialties.length === 0 && (
                <div className="text-center py-8 text-gray-500 text-xs">
                  {searchTerm ? (
                    <>No se encontraron especialidades que coincidan con &quot;{searchTerm}&quot;</>
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
                      w-full flex items-center gap-3 p-3 rounded-lg transition-all
                      ${
                        isSelected
                          ? 'bg-black text-white hover:bg-gray-800 border-2 border-black'
                          : isMaxReached
                          ? 'opacity-40 cursor-not-allowed'
                          : 'hover:bg-gray-50 border-2 border-transparent'
                      }
                    `}
                    title={specialty.Descripcion || specialty.Nombre || 'Especialidad'}
                  >
                    {/* Specialty Name */}
                    <div className="flex-1 text-left min-w-0">
                      <span className={`text-xs font-medium block ${isSelected ? 'text-white' : 'text-gray-700'}`}>
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
                      {isSelected && <Check className="w-3 h-3 text-black" />}
                    </div>
                  </button>
                );
              })}
            </div>

            {/* Error message */}
            {error && (
              <div className="bg-gray-100 border-t border-gray-200 px-4 py-2">
                <p className="text-xs text-gray-800">
                  {error}
                </p>
              </div>
            )}
          </div>
        )}
        
        {/* Loading State Overlay */}
        {loading && (
          <div className="absolute inset-0 bg-white/80 rounded-lg flex items-center justify-center">
            <div className="flex items-center gap-2 text-xs text-gray-600">
              <div className="w-4 h-4 border-2 border-black border-t-transparent rounded-full animate-spin"></div>
              Cargando...
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

