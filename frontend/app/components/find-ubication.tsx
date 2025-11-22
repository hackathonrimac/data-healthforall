'use client';

import { useState, useRef, useEffect } from 'react';
import { MapPin } from 'lucide-react';
import { SORTED_DISTRICTS, type UbigeoDistrict } from '@/lib/constants/ubigeo';

interface FindUbicationProps {
  onLocationSelect?: (ubigeo: UbigeoDistrict) => void;
  className?: string;
}

export function FindUbication({ onLocationSelect, className }: FindUbicationProps) {
  const [selectedDistrict, setSelectedDistrict] = useState<string>('');
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
        // Reset search term to selected district name when closing
        if (selectedDistrict) {
          const district = SORTED_DISTRICTS.find(d => d.code === selectedDistrict);
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
  }, [isOpen, selectedDistrict]);

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
    setIsOpen(true);
  };

  // Filter districts based on search term
  const filteredDistricts = SORTED_DISTRICTS.filter(district =>
    district.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const selectedDistrictData = SORTED_DISTRICTS.find(d => d.code === selectedDistrict);

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
          placeholder="Escribe o selecciona tu distrito"
          className="w-full px-4 py-2 bg-white/50 hover:bg-white/70 focus:bg-white rounded-lg border border-gray-200/50 text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500/20 text-gray-900 placeholder:text-gray-400"
        />

        {isOpen && filteredDistricts.length > 0 && (
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

        {isOpen && filteredDistricts.length === 0 && (
          <div className="absolute z-50 w-full mt-1 bg-white rounded-lg shadow-lg border border-gray-200 px-4 py-3 text-sm text-gray-500">
            No se encontraron distritos
          </div>
        )}
      </div>
    </div>
  );
}

