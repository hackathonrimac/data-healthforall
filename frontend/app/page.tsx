import { SearchHospital } from './components/search-hospital';

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-white px-4">
      <main className="flex flex-col items-center justify-center gap-8 w-full">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900">
            HealthForAll
          </h1>
        </div>
        
        <SearchHospital />
      </main>
    </div>
  );
}
