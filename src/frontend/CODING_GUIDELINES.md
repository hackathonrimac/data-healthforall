# Frontend Coding Guidelines - MANDATORY RULES

## 1. SOLID Principles - NON-NEGOTIABLE

- **Single Responsibility**: Each component serves ONE purpose only
- **Open/Closed**: Extend through props/composition. NEVER modify core components
- **Liskov Substitution**: Components must be interchangeable with their types
- **Interface Segregation**: Keep interfaces small and specific
- **Dependency Inversion**: Import abstractions, inject dependencies

## 2. UI Components - STRICT SHADCN ONLY

### MANDATORY: Use ONLY ShadCN/UI Components

**YOU MUST:**
- Install shadcn components via: `npx shadcn@latest add [component]`
- Use ONLY shadcn components from `@/components/ui`
- Copy components directly from https://ui.shadcn.com
- Customize ONLY with Tailwind classes

**YOU MUST NOT:**
- Create custom UI components when shadcn has an equivalent
- Use ANY external UI library (Material-UI, Ant Design, Chakra, etc.)
- Build basic components from scratch (buttons, inputs, cards, dialogs, etc.)

### ShadCN Component Examples

**Button Usage:**
```tsx
import { Button } from "@/components/ui/button"

// DO THIS
<Button variant="default">Click me</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>

// NOT THIS
<button className="...">Click me</button>
```

**Card Usage:**
```tsx
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"

// DO THIS - Always use shadcn Card
<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Card description</CardDescription>
  </CardHeader>
  <CardContent>Content here</CardContent>
  <CardFooter>Footer content</CardFooter>
</Card>

// NOT THIS
<div className="border rounded-lg p-4">...</div>
```

**Input & Form Usage:**
```tsx
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"

// DO THIS
<div>
  <Label htmlFor="email">Email</Label>
  <Input id="email" type="email" placeholder="Enter email" />
</div>

<Textarea placeholder="Type your message here" />

// NOT THIS
<input type="email" className="..." />
<textarea className="..." />
```

**Dialog/Modal Usage:**
```tsx
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"

// DO THIS
<Dialog>
  <DialogTrigger asChild>
    <Button>Open</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Title</DialogTitle>
      <DialogDescription>Description</DialogDescription>
    </DialogHeader>
    {/* Content */}
  </DialogContent>
</Dialog>

// NOT THIS - custom modal implementation
```

**Other Essential ShadCN Components:**
- `Select` - for dropdowns
- `Checkbox` - for checkboxes
- `RadioGroup` - for radio buttons
- `Switch` - for toggles
- `Tabs` - for tabbed interfaces
- `Toast` - for notifications
- `AlertDialog` - for confirmations
- `Popover` - for popovers
- `Sheet` - for side panels

## 3. Glass Style - MANDATORY FOR ALL UI ELEMENTS

### YOU MUST USE GLASSMORPHISM

**EVERY card, container, or panel MUST use glass effect:**

```tsx
// MANDATORY BASE GLASS CLASS
className="bg-white/70 backdrop-blur-md border border-white/20 shadow-lg"
```

**Glass Style Specifications:**
- **Background**: `bg-white/70` or `bg-white/60` (translucent white)
- **Blur**: `backdrop-blur-md` or `backdrop-blur-lg` (REQUIRED)
- **Border**: `border border-white/20` or `border-gray-200/50`
- **Shadow**: `shadow-lg` or `shadow-xl`
- **Corners**: `rounded-xl` or `rounded-2xl`

### Glass Card Example - YOUR TEMPLATE

```tsx
import { Card, CardContent } from "@/components/ui/card"

// USE THIS PATTERN FOR ALL CARDS
export function GlassCard({ children }: { children: React.ReactNode }) {
  return (
    <Card className="bg-white/70 backdrop-blur-md border border-white/20 shadow-xl rounded-2xl">
      <CardContent className="p-6">
        {children}
      </CardContent>
    </Card>
  )
}
```

### Color Palette - STRICT RULES

**YOU MUST:**
- Use `bg-white` or `bg-white/[60-70]` ONLY
- Text colors: `text-gray-900`, `text-gray-600`, `text-gray-400`
- Use minimal accents (sparingly)

**YOU MUST NOT:**
- Use colored backgrounds (no bg-blue, bg-red, etc.)
- Use dark mode variants (stick to light glass aesthetic)

### Typography - MANDATORY STANDARDS

**Use ONLY these font weights:**
- Headings: `font-semibold` or `font-bold`
- Body text: `font-normal`
- Light text: `font-light` (rarely)

**Use ONLY Tailwind text scale:**
- `text-xs`, `text-sm`, `text-base`, `text-lg`, `text-xl`, `text-2xl`, `text-3xl`

### Spacing - CONSISTENT STANDARDS

**Padding:** Use `p-4`, `p-6`, `p-8` consistently
**Gaps:** Use `gap-4`, `gap-6`, `gap-8` for flex/grid
**Margins:** Prefer `gap` over `margin` when possible

## 4. Code Quality - ENFORCE THESE RULES

### Keep It Simple - NO EXCEPTIONS

**DO:**
- Write simple, readable code
- Trust TypeScript's type system
- Use React's built-in features

**DON'T:**
- Over-engineer solutions
- Create unnecessary abstractions
- Write defensive code unless critical
- Add complex state management when React state suffices

### Component Structure - FOLLOW THIS ORDER

```tsx
// 1. Imports (external first, then internal)
import { useState } from 'react'
import { Card } from '@/components/ui/card'

// 2. Types/Interfaces
interface MyComponentProps {
  title: string
  onSubmit: () => void
}

// 3. Component
export function MyComponent({ title, onSubmit }: MyComponentProps) {
  return <div>{title}</div>
}

// 4. Default export (if needed)
export default MyComponent
```

### File Naming - STRICT CONVENTION

**ALL files MUST use `snake_case`:**
- Components: `my_component.tsx`
- Utilities: `string_utils.ts`
- Hooks: `use_fetch_data.ts`
- Types: `api_types.ts`

**Component exports MUST use `PascalCase`:**
```tsx
// File: my_component.tsx
export function MyComponent() { /* ... */ }
```

## 5. API Integration - MANDATORY PATTERNS

### Next.js API Routes Structure

**YOU MUST organize API routes like this:**
```
app/api/
  ├── search/
  │   └── route.ts          # GET /api/search?query=...
  ├── clinics/
  │   └── route.ts          # GET /api/clinics
  ├── doctors/
  │   └── route.ts          # GET /api/doctors
  ├── especialidades/
  │   └── route.ts          # GET /api/especialidades
  └── seguros/
      └── route.ts          # GET /api/seguros
```

### API Route Pattern - USE THIS TEMPLATE

```tsx
// app/api/search/route.ts
import { NextRequest, NextResponse } from 'next/server'

const AWS_BASE_URL = process.env.AWS_API_URL

export async function GET(request: NextRequest) {
  try {
    const query = request.nextUrl.searchParams.get('query')
    
    if (!query) {
      return NextResponse.json(
        { error: 'Query parameter required' },
        { status: 400 }
      )
    }
    
    const response = await fetch(
      `${AWS_BASE_URL}/search/doctors?query=${encodeURIComponent(query)}`
    )
    
    if (!response.ok) {
      throw new Error(`API responded with status: ${response.status}`)
    }
    
    const data = await response.json()
    return NextResponse.json(data)
    
  } catch (error) {
    console.error('API Error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
```

### Frontend Data Fetching - USE THIS PATTERN

```tsx
// In your component
'use client'

import { useState, useEffect } from 'react'
import { useToast } from '@/components/ui/use-toast'

export function SearchComponent() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const { toast } = useToast()
  
  async function searchDoctors(query: string) {
    setLoading(true)
    try {
      const response = await fetch(`/api/search?query=${encodeURIComponent(query)}`)
      
      if (!response.ok) {
        throw new Error('Search failed')
      }
      
      const data = await response.json()
      setData(data)
      
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch data",
        variant: "destructive",
      })
    } finally {
      setLoading(false)
    }
  }
  
  // Component JSX...
}
```

### API Integration Rules - ENFORCE THESE

**YOU MUST:**
- Proxy ALL backend calls through Next.js API routes
- Create ONE route file per endpoint
- Define response types in `types/api_types.ts`
- Handle errors with shadcn Toast component
- Validate query parameters
- Use `encodeURIComponent` for URL params

**YOU MUST NOT:**
- Call AWS backend directly from client components
- Ignore error handling
- Skip loading states
- Use external state management (React Query, SWR) unless absolutely necessary

## 6. Performance - MANDATORY OPTIMIZATIONS

**YOU MUST:**
- Use Server Components by default
- Add `'use client'` ONLY when needed (interactivity, hooks, browser APIs)
- Lazy load heavy components with `next/dynamic`
- Use `next/image` for ALL images
- Minimize client-side JavaScript

**Example of proper use client:**
```tsx
// page.tsx - Server Component (default)
import { DoctorList } from './doctor_list'

export default function Page() {
  return <DoctorList />
}

// doctor_list.tsx - Client Component (needs interactivity)
'use client'

import { useState } from 'react'
import { Button } from '@/components/ui/button'

export function DoctorList() {
  const [selected, setSelected] = useState(null)
  // ... interactive logic
}
```

## 7. FORBIDDEN PRACTICES - NEVER DO THESE

### ❌ ABSOLUTELY PROHIBITED

**YOU MUST NOT:**
- ❌ Use inline styles (`style={{...}}`)
- ❌ Use CSS modules or separate CSS files
- ❌ Import ANY UI library other than shadcn
- ❌ Build custom buttons, inputs, cards when shadcn has them
- ❌ Use colored backgrounds (only white/glass allowed)
- ❌ Skip glass effect on cards/containers
- ❌ Over-comment code (code should be self-documenting)
- ❌ Use complex state management (Redux, Zustand) without justification
- ❌ Create custom modal/dialog implementations
- ❌ Use class-based components (functional only)

### Examples of What NOT to Do

```tsx
// ❌ BAD - Custom button instead of shadcn
<button className="px-4 py-2 bg-blue-500 rounded">Click</button>

// ✅ GOOD - shadcn button
<Button variant="default">Click</Button>

// ❌ BAD - Custom card without glass effect
<div className="border rounded p-4 bg-gray-100">Content</div>

// ✅ GOOD - shadcn card with glass effect
<Card className="bg-white/70 backdrop-blur-md border border-white/20">
  <CardContent>Content</CardContent>
</Card>

// ❌ BAD - Inline styles
<div style={{ padding: '20px', backgroundColor: 'white' }}>Content</div>

// ✅ GOOD - Tailwind classes
<div className="p-6 bg-white">Content</div>

// ❌ BAD - Direct backend call from client
const data = await fetch('https://aws-api.../doctors')

// ✅ GOOD - Through Next.js API route
const data = await fetch('/api/doctors')
```

## 8. Complete Glass Component Example

```tsx
'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { useToast } from '@/components/ui/use-toast'

export function SearchCard() {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const { toast } = useToast()
  
  async function handleSearch() {
    setLoading(true)
    try {
      const response = await fetch(`/api/search?query=${encodeURIComponent(query)}`)
      const data = await response.json()
      // Handle data...
    } catch (error) {
      toast({
        title: "Error",
        description: "Search failed",
        variant: "destructive",
      })
    } finally {
      setLoading(false)
    }
  }
  
  return (
    <Card className="bg-white/70 backdrop-blur-md border border-white/20 shadow-xl rounded-2xl">
      <CardHeader>
        <CardTitle className="text-2xl font-semibold text-gray-900">
          Search Doctors
        </CardTitle>
        <CardDescription className="text-gray-600">
          Find doctors by name, specialty, or location
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <Input
          placeholder="Enter search query..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <Button 
          onClick={handleSearch}
          disabled={loading}
          className="w-full"
        >
          {loading ? 'Searching...' : 'Search'}
        </Button>
      </CardContent>
    </Card>
  )
}
```

---

## SUMMARY - YOUR COMMANDMENTS

1. **USE SHADCN ONLY** - Never build UI components from scratch
2. **APPLY GLASS EFFECT** - Every card/container must have glassmorphism
3. **KEEP IT SIMPLE** - No over-engineering, trust TypeScript
4. **PROXY APIs** - All backend calls through Next.js API routes
5. **SERVER FIRST** - Use Server Components unless you need client interactivity
6. **WHITE BACKGROUNDS** - No colored backgrounds, only white/glass
7. **SNAKE_CASE FILES** - All filenames in snake_case
8. **NO INLINE STYLES** - Tailwind only, no CSS modules

**Remember: Simplicity > Complexity. Beauty > Feature Bloat. Glass > Everything.**
