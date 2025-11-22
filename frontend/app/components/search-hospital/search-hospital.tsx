'use client';

import { Card, CardContent } from '@/app/components/ui/card';
import { FindUbication } from '@/app/components/search-hospital/find-ubication';
import { FindInsurance } from '@/app/components/search-hospital/find-insurance';
import { FindSpeciality } from '@/app/components/search-hospital/find-speciality';
import type { SearchFilters } from '@/app/components/search-hospital/useSearchFilters';
import type { UbigeoDistrict } from '@/lib/constants/ubigeo';

interface SearchHospitalProps {
  filters: SearchFilters;
  setSelectedLocation: (location: UbigeoDistrict | null) => void;
  setSelectedInsurances: (insurances: string[]) => void;
  setSelectedSpecialties: (specialties: string[]) => void;
}

export function SearchHospital({
  filters,
  setSelectedLocation,
  setSelectedInsurances,
  setSelectedSpecialties,
}: SearchHospitalProps) {
  return (
    <div className="w-full max-w-7xl space-y-6">
      <Card className="bg-white/70 backdrop-blur-md border border-white/20 shadow-xl rounded-2xl">
        <CardContent className="pt-6">
          <div className="flex items-center gap-4">
            <FindUbication 
              onLocationSelect={(ubigeo) => setSelectedLocation(ubigeo)}
              className="flex-1"
            />

            <FindInsurance 
              onInsuranceSelect={(insurances) => setSelectedInsurances(insurances)}
              className="flex-1"
            />

            <FindSpeciality 
              onSpecialtySelect={(specialties) => setSelectedSpecialties(specialties)}
              className="flex-1"
            />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

