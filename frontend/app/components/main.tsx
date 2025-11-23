'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';
import { SearchHospital } from '@/app/components/search-hospital/search-hospital';
import { CardInformation } from './card-information/card-information';
import { useSearchFilters } from './search-hospital/useSearchFilters';
import { useDoctorSearch } from '../hooks/useDoctorSearch';
import { Title } from './title';
import { Metrics } from './metrics';

export default function Main() {
  const {
    filters,
    setSelectedLocation,
    setSelectedInsurances,
    setSelectedSpecialties,
  } = useSearchFilters();

  const [isSearchTriggered, setIsSearchTriggered] = useState(false);

  // Fetch doctors based on selected filters
  const { data, isLoading, error } = useDoctorSearch({
    ubigeoId: filters.selectedLocation?.code || null,
    especialidadId: filters.selectedSpecialties[0] || null,
    seguroId: filters.selectedInsurances[0] || null,
    page: 1,
    pageSize: 20,
    enabled: isSearchTriggered, // Trigger search only when button is clicked
  });

  const handleSearch = () => {
    // Check if AT LEAST ONE filter is selected before triggering search
    // We do this to prevent invalid API calls if the user clicks search without selecting anything
    if (filters.selectedLocation || filters.selectedSpecialties.length > 0 || filters.selectedInsurances.length > 0) {
       setIsSearchTriggered(true);
    } else {
       toast.error("Por favor, selecciona una opción", {
         description: "Indícanos qué necesitas buscar para ayudarte.",
         duration: 3000,
       });
    }
  };

  // Reset search trigger if filters become empty (optional, but good for consistency)
  useEffect(() => {
     if (!filters.selectedLocation && filters.selectedSpecialties.length === 0 && filters.selectedInsurances.length === 0) {
        setIsSearchTriggered(false);
     }
  }, [filters]);

  return (
    <main className="relative h-screen flex flex-col bg-white overflow-hidden">
      {/* Subtle blue gradient at bottom */}
      <div className="absolute bottom-0 left-0 right-0 h-1/3 bg-gradient-to-t from-blue-50/30 to-transparent pointer-events-none" />
      
      <div className="relative z-10 w-full h-full flex flex-col">
        <AnimatePresence mode="wait">
          {!isSearchTriggered ? (
             // LANDING VIEW
             <motion.div 
               key="landing"
               exit={{ opacity: 0, y: -50 }}
               transition={{ duration: 0.5, ease: "easeInOut" }}
               className="flex-1 flex flex-col items-center justify-center px-4 overflow-y-auto"
             >
                <div className="w-full max-w-5xl space-y-12 py-10 flex flex-col items-center">
                   {/* 1. Title Section */}
                   <motion.div 
                     className="transform scale-110 w-full"
                     exit={{ opacity: 0, y: -20 }}
                     transition={{ duration: 0.3 }}
                   >
                     <Title />
                   </motion.div>

                   {/* 2. Search Section - Focal Point */}
                   <motion.div 
                     className="w-full max-w-4xl mx-auto transform transition-all hover:scale-[1.01] z-20"
                     layoutId="search-container"
                   >
                      <SearchHospital 
                        filters={filters}
                        setSelectedLocation={setSelectedLocation}
                        setSelectedInsurances={setSelectedInsurances}
                        setSelectedSpecialties={setSelectedSpecialties}
                        onSearch={handleSearch}
                      />
                   </motion.div>

                   {/* 3. Metrics Section - Social Proof */}
                   <motion.div 
                     className="pt-8 opacity-90 hover:opacity-100 transition-opacity w-full"
                     exit={{ opacity: 0, y: 20 }}
                     transition={{ duration: 0.3 }}
                   >
                     <Metrics />
                   </motion.div>
                </div>
             </motion.div>
          ) : (
             // RESULTS VIEW
             <motion.div 
               key="results"
               initial={{ opacity: 0 }}
               animate={{ opacity: 1 }}
               transition={{ duration: 0.5 }}
               className="flex flex-col h-full"
             >
                {/* Header Section */}
                <div className="flex-shrink-0 bg-white/80 backdrop-blur-sm border-b border-gray-100 z-30 shadow-sm">
                   <div className="max-w-7xl mx-auto w-full px-4 py-4">
                      <div className="flex flex-col md:flex-row md:items-center gap-4 justify-between">
                         <div className="flex items-center gap-3 cursor-pointer hover:opacity-80 transition-opacity" onClick={() => setIsSearchTriggered(false)}>
                            <h1 className="text-xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">
                              HealthForAll
                            </h1>
                            <span className="hidden md:inline-block h-4 w-px bg-gray-300 mx-2"></span>
                            <p className="hidden md:block text-sm text-gray-500">Encuentra tu especialista ideal</p>
                         </div>
                         
                         <div className="w-full md:max-w-2xl">
                            <SearchHospital 
                               filters={filters}
                               setSelectedLocation={setSelectedLocation}
                               setSelectedInsurances={setSelectedInsurances}
                               setSelectedSpecialties={setSelectedSpecialties}
                               onSearch={handleSearch}
                            />
                         </div>
                      </div>
                   </div>
                </div>

                {/* Error Message */}
                {error && (
                  <div className="flex-shrink-0 p-4 bg-red-50/50">
                    <div className="w-full max-w-5xl mx-auto bg-red-50 border border-red-200 rounded-lg p-3 shadow-sm">
                      <p className="text-red-800 text-sm font-medium">
                        {/* Customize error message for better UX */}
                        {error.includes("required") 
                          ? "Por favor selecciona una ubicación o especialidad para buscar." 
                          : error}
                      </p>
                    </div>
                  </div>
                )}

                {/* Results List */}
                <div className="flex-1 overflow-y-auto px-4 py-6 scroll-smooth">
                   <div className="w-full max-w-7xl mx-auto">
                      <CardInformation data={data} isLoading={isLoading} />
                   </div>
                </div>
             </motion.div>
          )}
        </AnimatePresence>
      </div>
    </main>
  );
}
