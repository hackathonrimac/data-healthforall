'use client';

import { useState, useRef, useEffect } from 'react';
import { MapPin } from 'lucide-react';
import type { UbigeoDistrict } from '@/lib/constants/ubigeo';

interface UbigeoApiResponse {
  ubigeoId: string;
  nombreDistrito: string;
  departamento: string;
  provincia: string;
}

interface FindUbicationProps {
  onLocationSelect?: (ubigeo: UbigeoDistrict) => void;
  className?: string;
}

export function FindUbication({ onLocationSelect, className }: FindUbicationProps) {
  const [selectedDistrict, setSelectedDistrict] = useState<string>('');
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [isOpen, setIsOpen] = useState(false);
  const [districts, setDistricts] = useState<UbigeoDistrict[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Fetch districts from API
  useEffect(() => {
    const fetchDistricts = async () => {
      try {
        setIsLoading(true);
        setError(null);
        
        const response = await fetch('/api/ubigeo');
        
        if (!response.ok) {
          throw new Error('Failed to fetch districts');
        }
        
        const data: UbigeoApiResponse[] = await response.json();
        
        // Transform API response to component format and sort alphabetically
        const transformed: UbigeoDistrict[] = data
          .map((item) => ({
            code: item.ubigeoId,
            name: item.nombreDistrito,
            department: item.departamento,
            province: item.provincia,
          }))
          .sort((a, b) => a.name.localeCompare(b.name));
        
        setDistricts(transformed);
      } catch (err) {
        console.error('Error fetching districts:', err);
        setError('No se pudieron cargar los distritos');
      } finally {
        setIsLoading(false);
      }
    };

    fetchDistricts();
  }, []);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
        // Reset search term to selected district name when closing
        if (selectedDistrict) {
          const district = districts.find(d => d.code === selectedDistrict);
          setSearchTerm(district?.name || '');
        } else {
          setSearchTerm('');
        }
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen, selectedDistrict, districts]);

  const handleDistrictSelect = (district: UbigeoDistrict) => {
    setSelectedDistrict(district.code);
    setSearchTerm(district.name);
    setIsOpen(false);
    if (onLocationSelect) {
      onLocationSelect(district);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
    setIsOpen(true);
  };

  const handleInputFocus = () => {
    if (!isLoading && !error) {
      setIsOpen(true);
    }
  };

  // Filter districts based on search term
  const filteredDistricts = districts.filter(district =>
    district.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const selectedDistrictData = districts.find(d => d.code === selectedDistrict);

  return (
    <div className={`flex items-center gap-3 ${className}`}>
      <MapPin className="w-4 h-4 text-gray-400" />
      <div className="relative flex-1" ref={dropdownRef}>
        <input
          ref={inputRef}
          type="text"
          value={searchTerm}
          onChange={handleInputChange}
          onFocus={handleInputFocus}
          placeholder={
            isLoading 
              ? "Cargando distritos..." 
              : error 
                ? error 
                : "Escribe o selecciona tu distrito"
          }
          disabled={isLoading || !!error}
          className="w-full px-4 py-2 bg-white/50 hover:bg-white/70 focus:bg-white rounded-lg border border-gray-200/50 text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500/20 text-gray-900 placeholder:text-gray-400 disabled:opacity-50 disabled:cursor-not-allowed"
        />

        {isOpen && !isLoading && !error && filteredDistricts.length > 0 && (
          <div className="absolute z-50 w-full mt-1 bg-white rounded-lg shadow-lg border border-gray-200 max-h-60 overflow-y-auto">
            {filteredDistricts.map((district) => (
              <button
                key={district.code}
                type="button"
                onClick={() => handleDistrictSelect(district)}
                className={`w-full text-left px-4 py-2 text-sm transition-colors hover:bg-blue-50 ${
                  selectedDistrict === district.code ? 'bg-blue-50 text-blue-900' : 'text-gray-700'
                }`}
              >
                {district.name}
              </button>
            ))}
          </div>
        )}

        {isOpen && !isLoading && !error && filteredDistricts.length === 0 && (
          <div className="absolute z-50 w-full mt-1 bg-white rounded-lg shadow-lg border border-gray-200 px-4 py-3 text-sm text-gray-500">
            No se encontraron distritos
          </div>
        )}
      </div>
    </div>
  );
}

