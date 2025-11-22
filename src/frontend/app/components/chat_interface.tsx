'use client';

import { useState } from 'react';

export function ChatInterface() {
  const [input, setInput] = useState('');
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userPrompt = input;
    setInput('');
    setResponse('');
    setIsLoading(true);

    try {
      const apiResponse = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: [{ role: 'user', content: userPrompt }]
        }),
      });

      if (!apiResponse.ok) throw new Error('Failed to fetch');

      const reader = apiResponse.body?.getReader();
      const decoder = new TextDecoder();
      let fullResponse = '';

      while (reader) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        fullResponse += chunk;
        setResponse(fullResponse);
      }
    } catch (error) {
      console.error('Error:', error);
      setResponse('Lo siento, ocurrió un error. Por favor, intenta de nuevo.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="w-full max-w-2xl space-y-6">
      <div className="bg-white/70 backdrop-blur-md border border-white/20 shadow-xl rounded-2xl p-6">
        <form onSubmit={handleSubmit}>
          <div className="space-y-4">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Escribe tu consulta médica..."
              className="w-full px-4 py-3 rounded-xl border border-gray-200 bg-white/80 text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-300 focus:border-transparent resize-none"
              rows={4}
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="w-full px-6 py-3 bg-gray-900 text-white rounded-xl font-medium hover:bg-gray-800 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Procesando...' : 'Consultar'}
            </button>
          </div>
        </form>
      </div>

      {(response || isLoading) && (
        <div className="bg-white/70 backdrop-blur-md border border-white/20 shadow-xl rounded-2xl p-6">
          {isLoading && !response ? (
            <div className="flex items-center gap-3">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
              </div>
              <span className="text-gray-500 text-sm">Generando respuesta...</span>
            </div>
          ) : (
            <p className="text-gray-900 leading-relaxed whitespace-pre-wrap">{response}</p>
          )}
        </div>
      )}
    </div>
  );
}

