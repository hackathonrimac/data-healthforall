import { useState, useEffect } from 'react';

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

interface ApiResponse {
  items: DoctorCard[];
  total: number;
  page: number;
  pageSize: number;
}

export interface SearchResponse {
  items: DoctorCard[];
  page: number;
  pageSize: number;
  total: number;
}

export interface UseDoctorSearchParams {
  ubigeoId?: string | null;
  especialidadId?: string | null;
  seguroId?: string | null;
  rimacEnsured?: boolean | null;
  page?: number;
  pageSize?: number;
  enabled?: boolean; // Only fetch when this is true
}

export interface UseDoctorSearchReturn {
  data: SearchResponse | null;
  isLoading: boolean;
  error: string | null;
  refetch: () => void;
}

export function useDoctorSearch({
  ubigeoId,
  especialidadId,
  seguroId = null,
  rimacEnsured = null,
  page = 1,
  pageSize = 10,
  enabled = true,
}: UseDoctorSearchParams): UseDoctorSearchReturn {
  const [data, setData] = useState<SearchResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [refetchTrigger, setRefetchTrigger] = useState(0);

  const refetch = () => {
    setRefetchTrigger((prev) => prev + 1);
  };

  useEffect(() => {
    // Don't fetch if not enabled or missing ALL params
    // At least ONE parameter must be provided
    const hasAtLeastOneParam = ubigeoId || especialidadId || seguroId || rimacEnsured !== null;
    
    if (!enabled || !hasAtLeastOneParam) {
      setData(null);
      setIsLoading(false);
      setError(null);
      return;
    }

    const fetchDoctors = async () => {
      setIsLoading(true);
      setError(null);

      try {
        const params = new URLSearchParams({
          page: page.toString(),
          pageSize: pageSize.toString(),
        });

        if (ubigeoId) {
          params.append('ubigeoId', ubigeoId);
        }

        if (especialidadId) {
          params.append('especialidadId', especialidadId);
        }

        if (seguroId) {
          params.append('seguroId', seguroId);
        }

        if (rimacEnsured !== null) {
          params.append('rimacEnsured', rimacEnsured.toString());
        }

        const url = `/api/search/doctors?${params.toString()}`;
        const response = await fetch(url);

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Error al buscar doctores');
        }

        const apiData: ApiResponse = await response.json();

        // Transform API response to match CardInformation expected format
        const transformedData: SearchResponse = {
          items: apiData.items,
          page: apiData.page,
          pageSize: apiData.pageSize,
          total: apiData.total,
        };

        setData(transformedData);
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Error desconocido';
        setError(errorMessage);
        console.error('Doctor search error:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchDoctors();
  }, [ubigeoId, especialidadId, seguroId, rimacEnsured, page, pageSize, enabled, refetchTrigger]);

  return {
    data,
    isLoading,
    error,
    refetch,
  };
}
