'use client';

import { useState } from 'react';
import { experimental_useObject as useObject } from '@ai-sdk/react';
import { Send, Loader2, MapPin, Stethoscope } from 'lucide-react';
import { Button } from '@/app/components/ui/button';
import { Textarea } from '@/app/components/ui/textarea';
import { Card, CardContent } from '@/app/components/ui/card';
import { searchSchema } from '@/lib/types/search-object';

export function ChatInterface() {
  const [input, setInput] = useState('');
  
  const { object, submit, isLoading } = useObject({
    api: '/api/search',
    schema: searchSchema,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userPrompt = input;
    setInput('');
    submit(userPrompt);
  };

  return (
    <div className="w-full max-w-2xl space-y-6">
      <Card className="bg-white/70 backdrop-blur-md border-white/20 shadow-xl">
        <CardContent className="pt-6">
          <form onSubmit={handleSubmit} className="flex gap-2 items-end">
              <Textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Escribe tu consulta médica..."
                className="resize-none text-gray-900 border-none !outline-none !ring-0 !shadow-none focus:!border-none focus:!outline-none focus:!ring-0 focus:!shadow-none active:!border-none active:!outline-none active:!ring-0 active:!shadow-none"
                disabled={isLoading}
                onKeyDown={(e) => {
                  if (
                    e.key === "Enter" &&
                    !e.shiftKey &&
                    !isLoading &&
                    input.trim()
                  ) {
                    e.preventDefault();
                    handleSubmit(e as any);
                  }
                }}
              />
              <Button
                type="submit"
                variant="default"
                disabled={isLoading || !input.trim()}
                size="icon"
              >
                {isLoading ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                    <Send className="w-5 h-5" />
                )}
              </Button>
          </form>
        </CardContent>
      </Card>

      {object && (
        <Card className="bg-white/70 backdrop-blur-md border-white/20 shadow-xl">
          <CardContent className="pt-6">
            <div className="space-y-4">
              {(object?.especialidad || object?.distrito) && (
                <div className="flex flex-wrap gap-2">
                  {object.especialidad && (
                    <div className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                      <Stethoscope className="w-4 h-4" />
                      <span>{object.especialidad}</span>
                    </div>
                  )}
                  {object.distrito && (
                    <div className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                      <MapPin className="w-4 h-4" />
                      <span>{object.distrito}</span>
                    </div>
                  )}
                </div>
              )}
              {object?.texto && (
                <p className="text-gray-900 leading-relaxed whitespace-pre-wrap">{object.texto}</p>
              )}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

