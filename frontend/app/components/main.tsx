'use client';

import { SearchHospital } from '@/app/components/search-hospital/search-hospital';

export default function Main() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-br from-blue-100 via-white to-green-100 px-4 py-8">
      <div className="w-full max-w-3xl mx-auto">
        <h1 className="text-3xl md:text-4xl font-bold mb-8 text-center text-gray-800 font-nunito">
          Busca tu médico
        </h1>
        <SearchHospital />
      </div>
    </main>
  );
}
