'use client';

import { useState } from 'react';

type EndpointMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';

interface Parameter {
  name: string;
  type: string;
  required: boolean;
  description: string;
  default?: string;
}

interface Endpoint {
  method: EndpointMethod;
  path: string;
  description: string;
  parameters: Parameter[];
  responseExample: string;
  notes?: string[];
}

interface ApiSection {
  id: string;
  title: string;
  description: string;
  baseUrl: string;
  endpoints: Endpoint[];
}

const API_DOCS: ApiSection[] = [
  {
    id: 'search',
    title: 'Search API',
    description: 'Search for doctors near you with specialty and location filters.',
    baseUrl: '/search',
    endpoints: [
      {
        method: 'GET',
        path: '/doctors',
        description: 'Returns doctor cards with denormalized data ready for UI rendering.',
        parameters: [
          { name: 'ubigeoId', type: 'string', required: true, description: 'Geographic location ID (distrito)' },
          { name: 'especialidadId', type: 'string', required: true, description: 'Specialty ID to filter by' },
          { name: 'seguroId', type: 'string', required: false, description: 'Insurance provider ID' },
          { name: 'page', type: 'number', required: false, description: 'Page number for pagination', default: '1' },
          { name: 'pageSize', type: 'number', required: false, description: 'Items per page', default: '10' },
        ],
        responseExample: `{
  "doctors": [
    {
      "doctorId": "CMP-12345",
      "doctorName": "Dr. Juan Pérez",
      "photoUrl": "https://...",
      "mainSpecialty": "Cardiología",
      "subSpecialties": ["Electrofisiología"],
      "clinicId": "CLINIC-001",
      "clinicName": "Clínica San Felipe",
      "clinicAddress": "Av. Gregorio Escobedo 650, Jesús María",
      "seguros": ["RIMAC", "PACIFICO"]
    }
  ],
  "total": 25,
  "page": 1,
  "pageSize": 10
}`,
        notes: [
          'This endpoint returns denormalized data (doctor + clinic + specialties + insurance)',
          'Perfect for rendering doctor cards in carousels without additional API calls',
        ],
      },
    ],
  },
  {
    id: 'clinics',
    title: 'Clinics API',
    description: 'List and filter clinics by location, specialty, and insurance.',
    baseUrl: '/clinics',
    endpoints: [
      {
        method: 'GET',
        path: '',
        description: 'List clinics or get clinic details.',
        parameters: [
          { name: 'ubigeoId', type: 'string', required: false, description: 'Filter by geographic location' },
          { name: 'especialidadId', type: 'string', required: false, description: 'Filter by available specialty' },
          { name: 'seguroId', type: 'string', required: false, description: 'Filter by accepted insurance' },
          { name: 'clinicaId', type: 'string', required: false, description: 'Get specific clinic details' },
          { name: 'page', type: 'number', required: false, description: 'Page number', default: '1' },
          { name: 'pageSize', type: 'number', required: false, description: 'Items per page', default: '10' },
        ],
        responseExample: `{
  "clinics": [
    {
      "clinicaId": "CLINIC-001",
      "nombreClinica": "Clínica San Felipe",
      "ubicacion": "Av. Gregorio Escobedo 650, Jesús María",
      "ubigeoId": "150117",
      "especialidadIds": ["CARD", "NEUR", "ONCO"],
      "seguroIds": ["RIMAC", "PACIFICO"],
      "grupoClinicaId": "SANFELIPE",
      "url": "https://clinicasanfelipe.com",
      "urlStaffMedico": "https://clinicasanfelipe.com/staff"
    }
  ],
  "total": 15,
  "page": 1,
  "pageSize": 10
}`,
        notes: [
          'When clinicaId is provided, other filters are not allowed',
          'Returns paginated list of clinics or single clinic detail',
        ],
      },
    ],
  },
  {
    id: 'doctors',
    title: 'Doctors API',
    description: 'List and filter doctors by specialty and clinic.',
    baseUrl: '/doctors',
    endpoints: [
      {
        method: 'GET',
        path: '',
        description: 'List doctors or get doctor details.',
        parameters: [
          { name: 'especialidadId', type: 'string', required: false, description: 'Filter by main specialty' },
          { name: 'clinicaId', type: 'string', required: false, description: 'Filter by clinic' },
          { name: 'doctorId', type: 'string', required: false, description: 'Get specific doctor details' },
          { name: 'page', type: 'number', required: false, description: 'Page number', default: '1' },
          { name: 'pageSize', type: 'number', required: false, description: 'Items per page', default: '10' },
        ],
        responseExample: `{
  "doctors": [
    {
      "doctorId": "CMP-12345",
      "nombreCompleto": "Dr. Juan Pérez García",
      "especialidadPrincipalId": "CARD",
      "subEspecialidadIds": ["CARD-ELECTRO"],
      "clinicaId": "CLINIC-001",
      "photoUrl": "https://..."
    }
  ],
  "total": 8,
  "page": 1,
  "pageSize": 10
}`,
        notes: [
          'Returns paginated list of doctors or single doctor detail',
          'Use Search API for denormalized doctor cards with clinic info',
        ],
      },
    ],
  },
  {
    id: 'especialidades',
    title: 'Especialidades API',
    description: 'Get medical specialties and subspecialties.',
    baseUrl: '/especialidades',
    endpoints: [
      {
        method: 'GET',
        path: '',
        description: 'List all specialties or get specific specialty.',
        parameters: [
          { name: 'especialidadId', type: 'string', required: false, description: 'Get specific specialty by ID' },
        ],
        responseExample: `{
  "especialidades": [
    {
      "especialidadId": "CARD",
      "nombre": "Cardiología",
      "descripcion": "Especialidad médica que se encarga del estudio, diagnóstico y tratamiento de las enfermedades del corazón"
    },
    {
      "especialidadId": "NEUR",
      "nombre": "Neurología",
      "descripcion": "Especialidad médica que trata los trastornos del sistema nervioso"
    }
  ]
}`,
      },
      {
        method: 'GET',
        path: '/subespecialidades',
        description: 'List subspecialties filtered by parent specialty.',
        parameters: [
          { name: 'especialidadId', type: 'string', required: true, description: 'Parent specialty ID' },
        ],
        responseExample: `{
  "subespecialidades": [
    {
      "subEspecialidadId": "CARD-ELECTRO",
      "especialidadId": "CARD",
      "nombre": "Electrofisiología Cardíaca",
      "descripcion": "Subespecialidad de cardiología enfocada en el sistema eléctrico del corazón"
    }
  ]
}`,
      },
    ],
  },
  {
    id: 'seguros',
    title: 'Seguros API',
    description: 'Get insurance providers and their coverage.',
    baseUrl: '/seguros',
    endpoints: [
      {
        method: 'GET',
        path: '',
        description: 'List all insurance providers or get specific one.',
        parameters: [
          { name: 'seguroId', type: 'string', required: false, description: 'Get specific insurance by ID' },
        ],
        responseExample: `{
  "seguros": [
    {
      "seguroId": "RIMAC",
      "nombre": "RIMAC Seguros",
      "descripcion": "Seguros de salud y vida"
    },
    {
      "seguroId": "PACIFICO",
      "nombre": "Pacífico Seguros",
      "descripcion": "Seguros de salud y EPS"
    }
  ]
}`,
      },
      {
        method: 'GET',
        path: '/seguros-clinicas',
        description: 'Get clinics covered by a specific insurance provider.',
        parameters: [
          { name: 'seguroId', type: 'string', required: true, description: 'Insurance provider ID' },
        ],
        responseExample: `{
  "seguroId": "RIMAC",
  "clinics": [
    {
      "clinicaId": "CLINIC-001",
      "nombreClinica": "Clínica San Felipe",
      "ubicacion": "Av. Gregorio Escobedo 650, Jesús María"
    }
  ]
}`,
      },
    ],
  },
];

function MethodBadge({ method }: { method: EndpointMethod }) {
  const colors = {
    GET: 'bg-blue-50 text-blue-700 border-blue-200',
    POST: 'bg-green-50 text-green-700 border-green-200',
    PUT: 'bg-orange-50 text-orange-700 border-orange-200',
    DELETE: 'bg-red-50 text-red-700 border-red-200',
  };

  return (
    <span className={`px-2 py-1 text-xs font-semibold rounded border ${colors[method]}`}>
      {method}
    </span>
  );
}

function CodeBlock({ code }: { code: string }) {
  return (
    <pre className="bg-gray-50 border border-gray-200 rounded-lg p-4 overflow-x-auto text-sm">
      <code className="text-gray-800 font-mono">{code}</code>
    </pre>
  );
}

function ParameterTable({ parameters }: { parameters: Parameter[] }) {
  if (parameters.length === 0) return null;

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-gray-200">
            <th className="text-left py-3 px-4 text-gray-600 font-semibold">Parameter</th>
            <th className="text-left py-3 px-4 text-gray-600 font-semibold">Type</th>
            <th className="text-left py-3 px-4 text-gray-600 font-semibold">Required</th>
            <th className="text-left py-3 px-4 text-gray-600 font-semibold">Description</th>
          </tr>
        </thead>
        <tbody>
          {parameters.map((param, idx) => (
            <tr key={idx} className="border-b border-gray-100 last:border-0">
              <td className="py-3 px-4">
                <code className="text-gray-900 font-mono bg-gray-50 px-2 py-1 rounded text-xs">
                  {param.name}
                </code>
              </td>
              <td className="py-3 px-4 text-gray-600">{param.type}</td>
              <td className="py-3 px-4">
                {param.required ? (
                  <span className="text-red-600 font-semibold text-xs">required</span>
                ) : (
                  <span className="text-gray-400 text-xs">optional</span>
                )}
              </td>
              <td className="py-3 px-4 text-gray-600">
                {param.description}
                {param.default && (
                  <span className="block text-xs text-gray-400 mt-1">Default: {param.default}</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function EndpointCard({ endpoint, baseUrl }: { endpoint: Endpoint; baseUrl: string }) {
  return (
    <div className="bg-white/70 backdrop-blur-md border border-white/20 shadow-lg rounded-xl p-6 mb-6">
      <div className="flex items-center gap-3 mb-4">
        <MethodBadge method={endpoint.method} />
        <code className="text-gray-900 font-mono text-sm font-semibold">{baseUrl}{endpoint.path || '/'}</code>
      </div>

      <p className="text-gray-600 mb-6">{endpoint.description}</p>

      {endpoint.parameters.length > 0 && (
        <div className="mb-6">
          <h4 className="text-sm font-semibold text-gray-900 mb-3">Query Parameters</h4>
          <ParameterTable parameters={endpoint.parameters} />
        </div>
      )}

      <div className="mb-4">
        <h4 className="text-sm font-semibold text-gray-900 mb-3">Response Example</h4>
        <CodeBlock code={endpoint.responseExample} />
      </div>

      {endpoint.notes && endpoint.notes.length > 0 && (
        <div className="mt-4 p-4 bg-blue-50 border border-blue-100 rounded-lg">
          <p className="text-xs font-semibold text-blue-900 mb-2">Notes</p>
          <ul className="space-y-1">
            {endpoint.notes.map((note, idx) => (
              <li key={idx} className="text-xs text-blue-800">• {note}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default function DocsPage() {
  const [selectedSection, setSelectedSection] = useState<string>('search');

  const currentSection = API_DOCS.find((s) => s.id === selectedSection) || API_DOCS[0];

  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">API Reference</h1>
          <p className="text-gray-600">Complete documentation for HealthForAll backend endpoints</p>
        </div>

        <div className="flex gap-8">
          {/* Sidebar */}
          <aside className="w-64 flex-shrink-0">
            <div className="bg-white/70 backdrop-blur-md border border-white/20 shadow-lg rounded-xl p-4 sticky top-8">
              <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3">
                Endpoints
              </h3>
              <nav className="space-y-1">
                {API_DOCS.map((section) => (
                  <button
                    key={section.id}
                    onClick={() => setSelectedSection(section.id)}
                    className={`w-full text-left px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                      selectedSection === section.id
                        ? 'bg-gray-100 text-gray-900'
                        : 'text-gray-600 hover:bg-gray-50'
                    }`}
                  >
                    {section.title}
                  </button>
                ))}
              </nav>

              <div className="mt-6 pt-6 border-t border-gray-200">
                <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3">
                  Resources
                </h3>
                <div className="space-y-2">
                  <a
                    href="https://aws.amazon.com/dynamodb/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block text-sm text-gray-600 hover:text-gray-900"
                  >
                    DynamoDB Docs
                  </a>
                  <a
                    href="https://aws.amazon.com/lambda/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block text-sm text-gray-600 hover:text-gray-900"
                  >
                    AWS Lambda
                  </a>
                </div>
              </div>
            </div>
          </aside>

          {/* Main Content */}
          <main className="flex-1 min-w-0">
            <div className="bg-white/70 backdrop-blur-md border border-white/20 shadow-xl rounded-2xl p-8 mb-8">
              <h2 className="text-3xl font-bold text-gray-900 mb-2">{currentSection.title}</h2>
              <p className="text-gray-600 mb-4">{currentSection.description}</p>
              <div className="flex items-center gap-2 p-3 bg-gray-50 border border-gray-200 rounded-lg">
                <span className="text-xs font-semibold text-gray-500 uppercase">Base URL</span>
                <code className="text-sm font-mono text-gray-900">
                  {process.env.NEXT_PUBLIC_API_URL || 'https://api.healthforall.com'}
                  {currentSection.baseUrl}
                </code>
              </div>
            </div>

            <div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">Endpoints</h3>
              {currentSection.endpoints.map((endpoint, idx) => (
                <EndpointCard key={idx} endpoint={endpoint} baseUrl={currentSection.baseUrl} />
              ))}
            </div>

            {/* Authentication Section */}
            <div className="mt-8 bg-white/70 backdrop-blur-md border border-white/20 shadow-lg rounded-xl p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Authentication</h3>
              <p className="text-gray-600 text-sm mb-4">
                All API endpoints are public and do not require authentication for this hackathon version.
                In production, implement API Gateway authorization with API keys or JWT tokens.
              </p>
              <CodeBlock
                code={`// Example request with future API key
fetch('https://api.healthforall.com/search/doctors?ubigeoId=150117&especialidadId=CARD', {
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY'
  }
});`}
              />
            </div>

            {/* Pagination Section */}
            <div className="mt-6 bg-white/70 backdrop-blur-md border border-white/20 shadow-lg rounded-xl p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Pagination</h3>
              <p className="text-gray-600 text-sm mb-4">
                All list endpoints support pagination using <code className="bg-gray-100 px-1 rounded">page</code> and{' '}
                <code className="bg-gray-100 px-1 rounded">pageSize</code> query parameters.
              </p>
              <ul className="space-y-2 text-sm text-gray-600">
                <li>• Default page: <code className="bg-gray-100 px-1 rounded">1</code></li>
                <li>• Default pageSize: <code className="bg-gray-100 px-1 rounded">10</code></li>
                <li>• Minimum page: <code className="bg-gray-100 px-1 rounded">1</code></li>
                <li>• Maximum pageSize: <code className="bg-gray-100 px-1 rounded">100</code></li>
              </ul>
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}

