'use client';

import { useState } from 'react';
import { Card, CardContent } from '@/app/components/ui/card';
import { FindUbication } from '@/app/components/find-ubication';
import { FindInsurance } from '@/app/components/find-insurance';
import { FindSpeciality } from '@/app/components/find-speciality';
import type { UbigeoDistrict } from '@/lib/constants/ubigeo';

export function SearchHospital() {
  const [input, setInput] = useState('');
  const [selectedLocation, setSelectedLocation] = useState<UbigeoDistrict | null>(null);
  const [selectedInsurances, setSelectedInsurances] = useState<string[]>([]);
  const [selectedSpecialties, setSelectedSpecialties] = useState<string[]>([]);
  


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

