"use client";

import React from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/app/components/ui/card";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/app/components/ui/accordion";
import { MapPin, User, Stethoscope, Shield } from "lucide-react";

interface DoctorCard {
  doctorId: string;
  doctorName: string;
  photoUrl?: string;
  mainSpecialty: string;
  subSpecialties: string[];
  clinicId: string;
  clinicName: string;
  clinicAddress: string;
  seguros: Array<{
    seguroId: string;
    nombre: string;
  }>;
}

interface SearchResponse {
  items: DoctorCard[];
  page: number;
  pageSize: number;
  total: number;
}

interface CardInformationProps {
  data: SearchResponse;
  isLoading?: boolean;
}

interface GroupedClinic {
  clinicId: string;
  clinicName: string;
  clinicAddress: string;
  seguros: Array<{ seguroId: string; nombre: string }>;
  doctors: DoctorCard[];
}

export function CardInformation({ data, isLoading = false }: CardInformationProps) {
  // Group doctors by clinic
  const groupedByClinic = React.useMemo(() => {
    const clinicMap = new Map<string, GroupedClinic>();

    data.items.forEach((doctor) => {
      if (!clinicMap.has(doctor.clinicId)) {
        clinicMap.set(doctor.clinicId, {
          clinicId: doctor.clinicId,
          clinicName: doctor.clinicName,
          clinicAddress: doctor.clinicAddress,
          seguros: doctor.seguros,
          doctors: [],
        });
      }
      clinicMap.get(doctor.clinicId)?.doctors.push(doctor);
    });

    return Array.from(clinicMap.values());
  }, [data.items]);

  if (isLoading) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <Card key={i} className="animate-pulse">
            <CardHeader>
              <div className="h-6 bg-gray-200 rounded w-3/4"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2 mt-2"></div>
            </CardHeader>
            <CardContent>
              <div className="h-20 bg-gray-200 rounded"></div>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  if (!data.items || data.items.length === 0) {
    return (
      <Card className="w-full">
        <CardContent className="flex flex-col items-center justify-center py-12">
          <Stethoscope className="h-16 w-16 text-gray-300 mb-4" />
          <p className="text-lg text-gray-600 text-center">
            No se encontraron doctores para tu búsqueda
          </p>
          <p className="text-sm text-gray-500 text-center mt-2">
            Intenta ajustar los filtros de búsqueda
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      {/* Results Summary */}
      <div className="flex justify-between items-center">
        <p className="text-sm text-gray-600">
          Mostrando{" "}
          <span className="font-semibold">
            {(data.page - 1) * data.pageSize + 1} -{" "}
            {Math.min(data.page * data.pageSize, data.total)}
          </span>{" "}
          de <span className="font-semibold">{data.total}</span> resultados
        </p>
        <p className="text-sm text-gray-600">
          {groupedByClinic.length} {groupedByClinic.length === 1 ? "clínica" : "clínicas"}
        </p>
      </div>

      {/* Grouped Results */}
      <div className="space-y-4">
        {groupedByClinic.map((clinic) => (
          <Card key={clinic.clinicId} className="overflow-hidden">
            <CardHeader className="bg-gradient-to-r from-blue-50 to-indigo-50 border-b">
              <CardTitle className="text-xl flex items-start gap-3">
                <MapPin className="h-5 w-5 text-blue-600 mt-1 flex-shrink-0" />
                <div className="flex-1">
                  <div className="font-bold text-gray-900">{clinic.clinicName}</div>
                  <CardDescription className="text-sm text-gray-600 mt-1 flex items-start gap-1">
                    <span>{clinic.clinicAddress}</span>
                  </CardDescription>
                </div>
              </CardTitle>

              {/* Insurance badges */}
              {clinic.seguros && clinic.seguros.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-3">
                  {clinic.seguros.map((seguro) => (
                    <span
                      key={seguro.seguroId}
                      className="inline-flex items-center gap-1 px-3 py-1 bg-white rounded-full text-xs font-medium text-blue-700 border border-blue-200"
                    >
                      <Shield className="h-3 w-3" />
                      {seguro.nombre}
                    </span>
                  ))}
                </div>
              )}
            </CardHeader>

            <CardContent className="p-6">
              <div className="mb-3">
                <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide">
                  Doctores Disponibles ({clinic.doctors.length})
                </h3>
              </div>

              <Accordion type="single" collapsible className="w-full">
                {clinic.doctors.map((doctor, index) => (
                  <AccordionItem key={doctor.doctorId} value={`doctor-${doctor.doctorId}`}>
                    <AccordionTrigger className="hover:no-underline">
                      <div className="flex items-center gap-4 text-left w-full">
                        {/* Doctor Photo */}
                        <div className="flex-shrink-0">
                          {doctor.photoUrl ? (
                            <img
                              src={doctor.photoUrl}
                              alt={doctor.doctorName}
                              className="h-12 w-12 rounded-full object-cover border-2 border-gray-200"
                            />
                          ) : (
                            <div className="h-12 w-12 rounded-full bg-gradient-to-br from-blue-100 to-indigo-100 flex items-center justify-center border-2 border-gray-200">
                              <User className="h-6 w-6 text-blue-600" />
                            </div>
                          )}
                        </div>

                        {/* Doctor Info */}
                        <div className="flex-1 min-w-0">
                          <p className="font-semibold text-gray-900 truncate">
                            {doctor.doctorName}
                          </p>
                          <p className="text-sm text-gray-600 truncate">
                            {doctor.mainSpecialty}
                          </p>
                        </div>
                      </div>
                    </AccordionTrigger>

                    <AccordionContent>
                      <div className="pt-4 pl-16 pr-4 space-y-3">
                        {/* Main Specialty */}
                        <div>
                          <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">
                            Especialidad Principal
                          </p>
                          <p className="text-sm text-gray-900">{doctor.mainSpecialty}</p>
                        </div>

                        {/* Sub-specialties */}
                        {doctor.subSpecialties && doctor.subSpecialties.length > 0 && (
                          <div>
                            <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                              Sub-especialidades
                            </p>
                            <div className="flex flex-wrap gap-2">
                              {doctor.subSpecialties.map((subSpec, idx) => (
                                <span
                                  key={idx}
                                  className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-xs font-medium border border-blue-100"
                                >
                                  {subSpec}
                                </span>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* Action Button */}
                        <div className="pt-2">
                          <button
                            className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium text-sm transition-colors duration-200"
                            onClick={() => {
                              // TODO: Implement booking or doctor profile view
                              console.log("Ver perfil del doctor:", doctor.doctorId);
                            }}
                          >
                            Ver Perfil y Agendar Cita
                          </button>
                        </div>
                      </div>
                    </AccordionContent>
                  </AccordionItem>
                ))}
              </Accordion>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Pagination Info */}
      {data.total > data.pageSize && (
        <div className="flex justify-center items-center gap-4 pt-4">
          <p className="text-sm text-gray-600">
            Página {data.page} de {Math.ceil(data.total / data.pageSize)}
          </p>
        </div>
      )}
    </div>
  );
}

