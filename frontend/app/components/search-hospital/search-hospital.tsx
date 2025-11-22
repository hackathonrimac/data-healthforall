'use client';

import { Card, CardContent } from '@/app/components/ui/card';
import { FindUbication } from '@/app/components/search-hospital/find-ubication';
import { FindInsurance } from '@/app/components/search-hospital/find-insurance';
import { FindSpeciality } from '@/app/components/search-hospital/find-speciality';
import { useSearchFilters } from '@/app/components/search-hospital/useSearchFilters';

export function SearchHospital() {
  const {
    filters,
    setSelectedLocation,
    setSelectedInsurances,
    setSelectedSpecialties,
  } = useSearchFilters();
  


  return (
    <div className="w-full max-w-2xl space-y-6">
      <Card className="bg-white/70 backdrop-blur-md border-white/20 shadow-xl">
        <CardContent className="pt-6 space-y-4">
          <FindUbication 
            onLocationSelect={(ubigeo) => setSelectedLocation(ubigeo)}
          />

          <FindInsurance 
            onInsuranceSelect={(insurances) => setSelectedInsurances(insurances)}
          />

          <FindSpeciality 
            onSpecialtySelect={(specialties) => setSelectedSpecialties(specialties)}
          />

        </CardContent>
      </Card>

    </div>
  );
}

