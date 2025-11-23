'use client';

import { useState } from 'react';
import { Card, CardContent } from '@/app/components/ui/card';
import { FindUbication } from '@/app/components/search-hospital/find-ubication';
import { FindInsurance } from '@/app/components/search-hospital/find-insurance';
import { FindSpeciality } from '@/app/components/search-hospital/find-speciality';
import { Plus, X } from 'lucide-react';
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
  const [showMoreFilters, setShowMoreFilters] = useState(false);

  return (
    <div className="w-full max-w-7xl space-y-4">
      {/* Main Filters Card */}
      <Card className="bg-white/70 backdrop-blur-md border border-white/20 shadow-sm rounded-2xl">
        <CardContent className="pt-6">
          <div className="flex items-center gap-4">
            <FindUbication 
              onLocationSelect={(ubigeo) => setSelectedLocation(ubigeo)}
              className="flex-1"
            />

            <FindSpeciality 
              onSpecialtySelect={(specialties) => setSelectedSpecialties(specialties)}
              className="flex-1"
            />

            {/* More Filters Button */}
            <button
              type="button"
              onClick={() => setShowMoreFilters(!showMoreFilters)}
              className="flex items-center justify-center gap-2 w-44 h-12 bg-gray-900 hover:bg-gray-800 text-white rounded-lg transition-all font-medium text-sm shadow-lg hover:shadow-xl whitespace-nowrap"
            >
              {showMoreFilters ? (
                <>
                  <X className="w-4 h-4" />
                  <span>Hide Filters</span>
                </>
              ) : (
                <>
                  <Plus className="w-4 h-4" />
                  <span>More Filters</span>
                </>
              )}
            </button>
          </div>
        </CardContent>
      </Card>

      {/* Additional Filters Card - Slides in and pushes content */}
      <div
        className={`
          grid transition-all duration-500 ease-out
          ${showMoreFilters 
            ? 'grid-rows-[1fr] opacity-100' 
            : 'grid-rows-[0fr] opacity-0'}
        `}
      >
        <div className="overflow-hidden">
          <div className="pb-0">
            <Card className="bg-white/70 backdrop-blur-md border border-white/20 shadow-sm rounded-2xl">
              <CardContent className="pt-6">
                <div className="space-y-4">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-sm font-semibold text-gray-900">Additional Filters</h3>
                    <button
                      type="button"
                      onClick={() => setShowMoreFilters(false)}
                      className="text-gray-400 hover:text-gray-600 transition-colors"
                      title="Close"
                    >
                      <X className="w-5 h-5" />
                    </button>
                  </div>
                  
                  <div className="flex items-center gap-4 pb-4">
                    <FindInsurance 
                      onInsuranceSelect={(insurances) => setSelectedInsurances(insurances)}
                      className="flex-1"
                    />
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}

