'use client';

import { SearchHospital } from '@/app/components/search-hospital/search-hospital';
import { CardInformation } from './card-information/card-information';
import { useSearchFilters } from './search-hospital/useSearchFilters';
import { useDoctorSearch } from '../hooks/useDoctorSearch';

export default function Main() {
  const {
    filters,
    setSelectedLocation,
    setSelectedInsurances,
    setSelectedSpecialties,
  } = useSearchFilters();

  // Fetch doctors based on selected filters
  const { data, isLoading, error } = useDoctorSearch({
    ubigeoId: filters.selectedLocation?.code || null,
    especialidadId: filters.selectedSpecialties[0] || null, // Using first specialty
    seguroId: filters.selectedInsurances[0] || null, // Using first insurance
    page: 1,
    pageSize: 20,
    enabled: !!(filters.selectedLocation && filters.selectedSpecialties.length > 0),
  });

  return (
    <main className="flex min-h-screen flex-col items-center bg-white px-4 py-8">
      <div className="w-full max-w-7xl mx-auto space-y-8">
        <div className="w-full max-w-3xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-bold mb-8 text-center text-gray-800 font-nunito">
            Busca tu médico
          </h1>
          <SearchHospital 
            filters={filters}
            setSelectedLocation={setSelectedLocation}
            setSelectedInsurances={setSelectedInsurances}
            setSelectedSpecialties={setSelectedSpecialties}
          />
        </div>

        {/* Error Message */}
        {error && (
          <div className="w-full max-w-5xl mx-auto">
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-800 text-sm">{error}</p>
            </div>
          </div>
        )}

        {/* Results */}
        {data && (
          <div className="w-full max-w-5xl mx-auto">
            <CardInformation data={data} isLoading={isLoading} />
          </div>
        )}

        {/* Empty state when no filters selected */}
        {!data && !isLoading && !error && (
          <div className="w-full max-w-5xl mx-auto text-center py-12">
            <p className="text-gray-600">
              Selecciona una ubicación y especialidad para buscar doctores
            </p>
          </div>
        )}
      </div>
    </main>
  );
}
