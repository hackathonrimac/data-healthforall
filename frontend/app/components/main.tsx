'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'sonner';
import Link from 'next/link';
import { FileText, Stethoscope, MapPin, ChevronRight, ChevronLeft } from 'lucide-react';
import { SearchHospital } from '@/app/components/search-hospital/search-hospital';
import { SearchSymptoms } from '@/app/components/search-hospital/search-symptoms';
import { CardInformation } from './card-information/card-information';
import { useSearchFilters } from './search-hospital/useSearchFilters';
import { useDoctorSearch } from '../hooks/useDoctorSearch';
import { Title } from './title';
import { Metrics } from './metrics';
import type { UbigeoDistrict } from '@/lib/constants/ubigeo';

type ViewMode = 'options' | 'symptoms' | 'search';

export default function Main() {
  const {
    filters,
    setSelectedLocation,
    setSelectedInsurances,
    setSelectedSpecialties,
  } = useSearchFilters();

  const [viewMode, setViewMode] = useState<ViewMode>('options');
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

  const handleSpecialtyFromSymptoms = (specialtyId: string, specialtyName: string) => {
    // Set specialty filter from symptoms flow
    setSelectedSpecialties([specialtyId]);
    
    // Transition to search view with pre-filled specialty
    setViewMode('search');
    
    // Show success message
    toast.success("Especialidad identificada", {
      description: `${specialtyName} - Ahora selecciona tu ubicación`,
      duration: 3000,
    });
  };

  const handleBackToOptions = () => {
    // Reset everything when going back to options
    setViewMode('options');
    setIsSearchTriggered(false);
    setSelectedLocation(null);
    setSelectedSpecialties([]);
    setSelectedInsurances([]);
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
             // LANDING VIEW (Options, Symptoms, or Search)
             <motion.div 
               key="landing"
               exit={{ opacity: 0, y: -50 }}
               transition={{ duration: 0.5, ease: "easeInOut" }}
               className="flex-1 flex flex-col items-center justify-center px-4 overflow-y-auto relative"
             >
                {/* Back Button - Only show when not on options */}
                {viewMode !== 'options' && (
                  <button
                    onClick={handleBackToOptions}
                    className="absolute top-6 left-6 flex items-center gap-2 px-4 py-2 rounded-lg bg-white border border-gray-200 hover:border-gray-300 hover:shadow-md transition-all duration-200 text-gray-700 hover:text-gray-900 z-50"
                  >
                    <ChevronLeft className="w-4 h-4" />
                    <span className="font-medium text-sm">Volver</span>
                  </button>
                )}

                {/* Docs Button - Top Right */}
                <Link 
                  href="/docs"
                  className="absolute top-6 right-6 flex items-center gap-2 px-4 py-2 rounded-lg bg-white border border-gray-200 hover:border-gray-300 hover:shadow-md transition-all duration-200 text-gray-700 hover:text-gray-900 group z-50"
                >
                  <FileText className="w-4 h-4 group-hover:scale-110 transition-transform" />
                  <span className="font-medium text-sm">Docs</span>
                </Link>

                <div className="w-full max-w-5xl space-y-12 py-10 flex flex-col items-center">
                   {/* 1. Title Section - Always visible */}
                   <motion.div 
                     className="transform scale-110 w-full"
                     transition={{ duration: 0.3 }}
                   >
                     <Title />
                   </motion.div>

                   {/* 2. Dynamic Content Section */}
                   <div className="w-full max-w-4xl mx-auto">
                     <AnimatePresence mode="wait">
                       {viewMode === 'options' && (
                         <motion.div
                           key="options-content"
                           initial={{ opacity: 0, y: 20 }}
                           animate={{ opacity: 1, y: 0 }}
                           exit={{ opacity: 0, y: -20 }}
                           transition={{ duration: 0.3 }}
                           className="grid md:grid-cols-2 gap-4"
                         >
                           {/* Option 1: Symptoms */}
                           <motion.button
                             onClick={() => setViewMode('symptoms')}
                             className="group w-full flex items-center gap-4 p-5 bg-white/70 hover:bg-white backdrop-blur-md border border-white/20 hover:border-gray-300 rounded-xl shadow-sm hover:shadow-md transition-all duration-200 text-left"
                             whileHover={{ x: 5 }}
                             whileTap={{ scale: 0.98 }}
                           >
                             <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:bg-blue-200 transition-colors">
                               <Stethoscope className="w-5 h-5 text-blue-600" />
                             </div>
                             <div className="flex-1 min-w-0">
                               <h3 className="text-base font-semibold text-gray-900">
                                 Tengo síntomas, ¿con qué especialista debo ir?
                               </h3>
                             </div>
                             <ChevronRight className="w-5 h-5 text-gray-400 group-hover:text-gray-900 transition-colors flex-shrink-0" />
                           </motion.button>

                           {/* Option 2: Location Search */}
                           <motion.button
                             onClick={() => setViewMode('search')}
                             className="group w-full flex items-center gap-4 p-5 bg-white/70 hover:bg-white backdrop-blur-md border border-white/20 hover:border-gray-300 rounded-xl shadow-sm hover:shadow-md transition-all duration-200 text-left"
                             whileHover={{ x: 5 }}
                             whileTap={{ scale: 0.98 }}
                           >
                             <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:bg-green-200 transition-colors">
                               <MapPin className="w-5 h-5 text-green-600" />
                             </div>
                             <div className="flex-1 min-w-0">
                               <h3 className="text-base font-semibold text-gray-900">
                                 Quiero ubicar mis centros más cercanos
                               </h3>
                             </div>
                             <ChevronRight className="w-5 h-5 text-gray-400 group-hover:text-gray-900 transition-colors flex-shrink-0" />
                           </motion.button>
                         </motion.div>
                       )}

                       {viewMode === 'symptoms' && (
                         <motion.div
                           key="symptoms-content"
                           initial={{ opacity: 0, y: 20 }}
                           animate={{ opacity: 1, y: 0 }}
                           exit={{ opacity: 0, y: -20 }}
                           transition={{ duration: 0.3 }}
                         >
                           <SearchSymptoms onSpecialtySelected={handleSpecialtyFromSymptoms} />
                         </motion.div>
                       )}

                       {viewMode === 'search' && (
                         <motion.div
                           key="search-content"
                           initial={{ opacity: 0, y: 20 }}
                           animate={{ opacity: 1, y: 0 }}
                           exit={{ opacity: 0, y: -20 }}
                           transition={{ duration: 0.3 }}
                         >
                           <SearchHospital 
                             filters={filters}
                             setSelectedLocation={setSelectedLocation}
                             setSelectedInsurances={setSelectedInsurances}
                             setSelectedSpecialties={setSelectedSpecialties}
                             onSearch={handleSearch}
                           />
                         </motion.div>
                       )}
                     </AnimatePresence>
                   </div>

                   {/* 3. Metrics Section - Always visible */}
                   <motion.div 
                     className="pt-8 opacity-90 hover:opacity-100 transition-opacity w-full"
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
                         <div className="flex items-center gap-3 cursor-pointer hover:opacity-80 transition-opacity" onClick={handleBackToOptions}>
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
