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
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogClose,
} from "@/app/components/ui/dialog";
import { MapPin, User, Stethoscope, Shield } from "lucide-react";

interface DoctorCard {
  doctorId: string;
  doctorName: string;
  photoUrl?: string;
  mainSpecialty: string;
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
  data: SearchResponse | null;
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
  const [selectedClinic, setSelectedClinic] = React.useState<GroupedClinic | null>(null);
  
  // Group doctors by clinic
  const groupedByClinic = React.useMemo(() => {
    if (!data || !data.items) {
      return [];
    }

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
  }, [data]);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center w-full h-64">
        <svg className="animate-spin h-10 w-10 text-gray-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4z" />
        </svg>
      </div>
    );
  }

  if (!data || !data.items || data.items.length === 0) {
    return (
      <Card className="w-full border-none shadow-none bg-transparent" style={{ backgroundColor: '#FFFFFF', border: '1px solid #E5E7EB' }}>
        <CardContent className="flex flex-col items-center justify-center py-12 border-none shadow-none">
          <Stethoscope style={{ color: '#D1D5DB', width: '64px', height: '64px', marginBottom: '16px' }} />
          <p style={{ fontSize: '18px', color: '#4B5563', textAlign: 'center' }}>
            No se encontraron doctores para tu búsqueda
          </p>
          <p style={{ fontSize: '14px', color: '#6B7280', textAlign: 'center', marginTop: '8px' }}>
            Intenta ajustar los filtros de búsqueda
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="w-full max-w-7xl space-y-6">
      {/* Results Summary */}
      <div className="flex justify-between items-center">
        <p style={{ fontSize: '14px', color: '#4B5563' }}>
          Mostrando{" "}
          <span style={{ fontWeight: 600 }}>
            {(data.page - 1) * data.pageSize + 1} -{" "}
            {Math.min(data.page * data.pageSize, data.total)}
          </span>{" "}
          de <span style={{ fontWeight: 600 }}>{data.total}</span> resultados
        </p>
        <p style={{ fontSize: '14px', color: '#4B5563' }}>
          {groupedByClinic.length} {groupedByClinic.length === 1 ? "clínica" : "clínicas"}
        </p>
      </div>

      {/* Grouped Results - 2 columns grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {groupedByClinic.map((clinic) => (
          <Card key={clinic.clinicId} className="overflow-hidden flex flex-col">
            <CardHeader style={{ background: 'linear-gradient(to right, #F9FAFB, #F3F4F6)', borderBottom: '1px solid #E5E7EB' }}>
              <CardTitle className="text-lg flex items-start gap-3">
                <MapPin style={{ height: '20px', width: '20px', color: '#4B5563', marginTop: '4px' }} className="flex-shrink-0" />
                <div className="flex-1 min-w-0">
                  <div style={{ fontWeight: 700, color: '#111827' }} className="truncate">{clinic.clinicName}</div>
                  <CardDescription style={{ fontSize: '14px', color: '#4B5563', marginTop: '4px' }}>
                    <span className="line-clamp-1">{clinic.clinicAddress}</span>
                  </CardDescription>
                </div>
              </CardTitle>

              {/* Insurance badges */}
              {clinic.seguros && clinic.seguros.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-3">
                  {clinic.seguros.map((seguro) => (
                    <span
                      key={seguro.seguroId}
                      style={{ 
                        display: 'inline-flex', 
                        alignItems: 'center', 
                        gap: '4px', 
                        padding: '4px 12px', 
                        backgroundColor: '#FFFFFF', 
                        borderRadius: '9999px', 
                        fontSize: '12px', 
                        fontWeight: 500, 
                        color: '#374151', 
                        border: '1px solid #D1D5DB' 
                      }}
                    >
                      <Shield style={{ height: '12px', width: '12px' }} />
                      {seguro.nombre}
                    </span>
                  ))}
                </div>
              )}
            </CardHeader>

            <CardContent style={{ padding: '24px', backgroundColor: '#FFFFFF' }} className="flex-1">
              <div style={{ marginBottom: '12px' }}>
                <h3 style={{ fontSize: '14px', fontWeight: 600, color: '#374151', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  Doctores Disponibles ({clinic.doctors.length})
                </h3>
              </div>

              {/* Show only first doctor */}
              <div className="space-y-4">
                {clinic.doctors.slice(0, 1).map((doctor) => (
                  <div key={doctor.doctorId} style={{ display: 'flex', alignItems: 'flex-start', gap: '16px', padding: '12px', borderRadius: '8px', backgroundColor: '#F9FAFB', border: '1px solid #E5E7EB' }}>
                    {/* Doctor Photo */}
                    <div className="flex-shrink-0">
                      {doctor.photoUrl ? (
                        <img
                          src={doctor.photoUrl}
                          alt={doctor.doctorName}
                          style={{ height: '48px', width: '48px', borderRadius: '9999px', objectFit: 'cover', border: '2px solid #D1D5DB' }}
                        />
                      ) : (
                        <div style={{ height: '48px', width: '48px', borderRadius: '9999px', backgroundColor: '#E5E7EB', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '2px solid #D1D5DB' }}>
                          <User style={{ height: '24px', width: '24px', color: '#4B5563' }} />
                        </div>
                      )}
                    </div>

                    {/* Doctor Info */}
                    <div className="flex-1 min-w-0">
                      <p style={{ fontWeight: 600, color: '#111827' }} className="truncate">
                        {doctor.doctorName}
                      </p>
                      <p style={{ fontSize: '14px', color: '#4B5563' }} className="truncate">
                        {doctor.mainSpecialty}
                      </p>
                    </div>
                  </div>
                ))}

                {/* Show "y X doctores más" if there are more doctors */}
                {clinic.doctors.length > 1 && (
                  <button
                    onClick={() => setSelectedClinic(clinic)}
                    style={{
                      fontSize: '14px',
                      color: '#2563EB',
                      fontWeight: 500,
                      cursor: 'pointer',
                      background: 'none',
                      border: 'none',
                      padding: '8px 12px',
                      textAlign: 'left',
                      width: '100%',
                      borderRadius: '8px',
                      transition: 'background-color 0.2s',
                    }}
                    onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#F3F4F6'}
                    onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
                  >
                    y {clinic.doctors.length - 1} doctores más
                  </button>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Pagination Info */}
      {data.total > data.pageSize && (
        <div className="flex justify-center items-center gap-4 pt-4">
          <p style={{ fontSize: '14px', color: '#4B5563' }}>
            Página {data.page} de {Math.ceil(data.total / data.pageSize)}
          </p>
        </div>
      )}

      {/* Modal for all doctors */}
      <Dialog open={!!selectedClinic} onOpenChange={(open) => !open && setSelectedClinic(null)}>
        <DialogContent>
          <DialogClose onClose={() => setSelectedClinic(null)} />
          <DialogHeader>
            <DialogTitle>
              {selectedClinic?.clinicName}
            </DialogTitle>
            <p style={{ fontSize: '14px', color: '#6B7280', marginTop: '4px' }}>
              {selectedClinic?.clinicAddress}
            </p>
          </DialogHeader>
          
          <div style={{ padding: '24px' }}>
            {/* Insurance badges in modal */}
            {selectedClinic?.seguros && selectedClinic.seguros.length > 0 && (
              <div className="flex flex-wrap gap-2 mb-6">
                {selectedClinic.seguros.map((seguro) => (
                  <span
                    key={seguro.seguroId}
                    style={{ 
                      display: 'inline-flex', 
                      alignItems: 'center', 
                      gap: '4px', 
                      padding: '4px 12px', 
                      backgroundColor: '#F3F4F6', 
                      borderRadius: '9999px', 
                      fontSize: '12px', 
                      fontWeight: 500, 
                      color: '#374151', 
                      border: '1px solid #D1D5DB' 
                    }}
                  >
                    <Shield style={{ height: '12px', width: '12px' }} />
                    {seguro.nombre}
                  </span>
                ))}
              </div>
            )}

            <h3 style={{ fontSize: '16px', fontWeight: 600, color: '#111827', marginBottom: '16px' }}>
              Todos los doctores ({selectedClinic?.doctors.length || 0})
            </h3>

            {/* All doctors list */}
            <div className="space-y-3">
              {selectedClinic?.doctors.map((doctor) => (
                <div key={doctor.doctorId} style={{ display: 'flex', alignItems: 'flex-start', gap: '16px', padding: '12px', borderRadius: '8px', backgroundColor: '#F9FAFB', border: '1px solid #E5E7EB' }}>
                  {/* Doctor Photo */}
                  <div className="flex-shrink-0">
                    {doctor.photoUrl ? (
                      <img
                        src={doctor.photoUrl}
                        alt={doctor.doctorName}
                        style={{ height: '48px', width: '48px', borderRadius: '9999px', objectFit: 'cover', border: '2px solid #D1D5DB' }}
                      />
                    ) : (
                      <div style={{ height: '48px', width: '48px', borderRadius: '9999px', backgroundColor: '#E5E7EB', display: 'flex', alignItems: 'center', justifyContent: 'center', border: '2px solid #D1D5DB' }}>
                        <User style={{ height: '24px', width: '24px', color: '#4B5563' }} />
                      </div>
                    )}
                  </div>

                  {/* Doctor Info */}
                  <div className="flex-1 min-w-0">
                    <p style={{ fontWeight: 600, color: '#111827' }} className="truncate">
                      {doctor.doctorName}
                    </p>
                    <p style={{ fontSize: '14px', color: '#4B5563' }} className="truncate">
                      {doctor.mainSpecialty}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}

