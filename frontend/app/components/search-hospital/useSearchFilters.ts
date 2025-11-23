import { useState } from 'react';
import type { UbigeoDistrict } from '@/lib/constants/ubigeo';

export interface SearchFilters {
  selectedLocation: UbigeoDistrict | null;
  selectedInsurances: string[];
  selectedSpecialties: string[];
}

export interface UseSearchFiltersReturn {
  filters: SearchFilters;
  setSelectedLocation: (location: UbigeoDistrict | null) => void;
  setSelectedInsurances: (insurances: string[]) => void;
  setSelectedSpecialties: (specialties: string[]) => void;
  resetFilters: () => void;
}

export function useSearchFilters(): UseSearchFiltersReturn {
  const [selectedLocation, setSelectedLocation] = useState<UbigeoDistrict | null>(null);
  const [selectedInsurances, setSelectedInsurances] = useState<string[]>([]);
  const [selectedSpecialties, setSelectedSpecialties] = useState<string[]>([]);

  const resetFilters = () => {
    setSelectedLocation(null);
    setSelectedInsurances([]);
    setSelectedSpecialties([]);
  };

  return {
    filters: {
      selectedLocation,
      selectedInsurances,
      selectedSpecialties,
    },
    setSelectedLocation,
    setSelectedInsurances,
    setSelectedSpecialties,
    resetFilters,
  };
}

