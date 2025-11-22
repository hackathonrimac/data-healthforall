import { ChatInterface } from './components/chat_interface';

export default function Home() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-white px-4">
      <main className="flex flex-col items-center justify-center gap-8 w-full">
        <div className="text-center space-y-3">
          <h1 className="text-4xl font-bold text-gray-900">
            HealthForAll
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl">
            Encuentra doctores, clínicas y especialidades médicas en Perú. 
            Pregúntame lo que necesites.
          </p>
        </div>
        
        <ChatInterface />
      </main>
    </div>
  );
}
