# Aquarius Frontend

React + TypeScript + Vite frontend for the Aquarius synchronized swimming competition management system.

## Architecture

The frontend follows **Domain-Driven Design (DDD)** principles with domain-specific slicing to align with the backend architecture.

### Domain Structure

```
src/
├── api/               # API service layer (domain-specific)
│   ├── client.ts      # Base axios client
│   ├── kind.ts        # Kind (Child) API
│   ├── anmeldung.ts   # Anmeldung (Registration) API
│   ├── wettkampf.ts   # Wettkampf (Competition) API
│   ├── grunddaten.ts  # Grunddaten (Verein, Verband, Versicherung)
│   ├── saison.ts      # Saison API
│   ├── schwimmbad.ts  # Schwimmbad API
│   ├── figur.ts       # Figur API
│   ├── admin.ts       # Admin & Auth API
│   └── index.ts       # Central exports
├── types/             # TypeScript types (domain-specific)
│   ├── kind.ts        # Kind types
│   ├── anmeldung.ts   # Anmeldung types
│   ├── wettkampf.ts   # Wettkampf types
│   ├── grunddaten.ts  # Grunddaten types
│   ├── saison.ts      # Saison types
│   ├── schwimmbad.ts  # Schwimmbad types
│   ├── figur.ts       # Figur types
│   └── index.ts       # Central exports (for backward compatibility)
├── pages/             # Page components
├── components/        # Shared UI components
└── styles/            # Global styles
```

## API Services

Each domain has its own API service file that encapsulates all HTTP calls for that domain.

### Example Usage

```typescript
// Import from domain-specific file
import { listKinder, createKind, deleteKind, isKindInsured } from '../api/kind';
import { Kind } from '../types/kind';

// Use in React Query
const { data: kinderData } = useQuery({
  queryKey: ['kinder'],
  queryFn: () => listKinder({ limit: 20, search: 'Max' }),
});

const kinder = kinderData?.items || [];
```

### Domain API Services

| Domain | API File | Types File | Description |
|--------|----------|------------|-------------|
| **Kind** | `api/kind.ts` | `types/kind.ts` | Child/participant management |
| **Anmeldung** | `api/anmeldung.ts` | `types/anmeldung.ts` | Competition registrations |
| **Wettkampf** | `api/wettkampf.ts` | `types/wettkampf.ts` | Competition management |
| **Grunddaten** | `api/grunddaten.ts` | `types/grunddaten.ts` | Base data (Verein, Verband, Versicherung) |
| **Saison** | `api/saison.ts` | `types/saison.ts` | Season management |
| **Schwimmbad** | `api/schwimmbad.ts` | `types/schwimmbad.ts` | Venue management |
| **Figur** | `api/figur.ts` | `types/figur.ts` | Figure/routine catalog |
| **Admin** | `api/admin.ts` | - | Authentication & user management |

## Development

### Prerequisites

- Node.js 18+ (tested with Node.js 25.2.1)
- npm or yarn

### Install Dependencies

```bash
npm install
```

### Development Server

```bash
npm run dev
```

Runs the app in development mode at [http://localhost:5173](http://localhost:5173).

### Build

```bash
npm run build
```

Builds the app for production to `dist/`.

**Note:** TypeScript compilation must pass for the build to succeed:

```bash
npx tsc --noEmit
```

### Testing

#### Unit Tests (Vitest)

```bash
npm test
```

Unit tests for API services are located in `src/__tests__/api/`.

#### E2E Tests (Playwright)

```bash
# Install Playwright (first time only)
npx playwright install chromium

# Run E2E tests
npm run test:e2e
```

E2E tests are located in `tests/e2e/` and test complete user workflows:
- `kind-management.spec.ts` - Kind CRUD operations and insurance logic
- `wettkampf-anmeldung.spec.ts` - Complex nested data and business rules
- `workflows.spec.ts` - Complete business workflows
- `smoke.spec.ts` - Basic smoke tests

## Migration Status

### ✅ Completed Components

The following components have been updated to use domain-specific API services:

- `pages/KindList.tsx`
- `pages/KindForm.tsx`
- `pages/AnmeldungList.tsx`
- `pages/AnmeldungForm.tsx`

### 🔄 Pending Migration

The following components still use the old centralized `types/index.ts` imports and direct `apiClient` calls. They will be migrated opportunistically as needed:

- Wettkampf pages (WettkampfList, WettkampfForm, WettkampfDetail)
- Verein pages (VereinList, VereinForm)
- Saison pages (SaisonList, SaisonForm)
- Schwimmbad pages (SchwimmbadList, SchwimmbadForm)
- Figur pages (FigurenList, FigurenForm, FigurDetail)
- Verband & Versicherung pages
- Admin pages (Login, UserList, TOTPSetup, etc.)
- Home page

**Migration is not urgent** - the old imports still work via re-exports in `types/index.ts`.

## Code Style & Patterns

### API Service Pattern

Each API service follows this structure:

```typescript
// Example: api/kind.ts
import apiClient from './client';
import { Kind, KindCreate } from '../types/kind';

export interface KindListParams {
  skip?: number;
  limit?: number;
  search?: string;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

export interface KindListResponse {
  items: Kind[];
  total: number;
}

export const listKinder = async (params: KindListParams = {}): Promise<KindListResponse> => {
  const response = await apiClient.get<Kind[]>('/kind', { params });
  return {
    items: response.data,
    total: parseInt(response.headers['x-total-count'] || '0', 10),
  };
};

export const getKind = async (id: number): Promise<Kind> => {
  const response = await apiClient.get<Kind>(`/kind/${id}`);
  return response.data;
};

// ... more CRUD operations
```

### React Query Integration

```typescript
// List with pagination
const { data: kinderData } = useQuery({
  queryKey: ['kinder', page, pageSize, searchTerm],
  queryFn: () => listKinder({
    skip: (page - 1) * pageSize,
    limit: pageSize,
    search: searchTerm || undefined,
  }),
});

const kinder = kinderData?.items || [];
const totalCount = kinderData?.total || 0;

// Single item
const { data: kind } = useQuery({
  queryKey: ['kind', id],
  queryFn: () => getKind(Number(id)),
  enabled: Boolean(id),
});

// Mutations
const createMutation = useMutation({
  mutationFn: createKind,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['kinder'] });
    navigate('/kind');
  },
});
```

### Type Safety

Always use domain-specific types:

```typescript
// ✅ Good - domain-specific import
import { Kind, KindCreate } from '../types/kind';
import { Verein } from '../types/grunddaten';

// ⚠️ Acceptable but prefer specific imports
import { Kind } from '../types';

// ❌ Avoid - no type safety
const kind: any = ...;
```

## Testing Strategy

### Unit Tests

- Test API service functions in isolation
- Mock `apiClient` using Vitest's `vi.mock()`
- Verify correct parameters, response mapping, and error handling

### E2E Tests

- Use Playwright for full user workflows
- Set up test data via API (more reliable than UI-driven setup)
- Test critical business rules (e.g., vorläufig status, insurance logic)
- Verify eager loading (no N+1 queries, no raw IDs displayed)

## Troubleshooting

### TypeScript Errors

If you encounter TypeScript errors after updating components:

1. Ensure all imports use the correct domain-specific files
2. Check that React Query types are properly specified:
   ```typescript
   useQuery<DataType[], Error, DataType[]>({...})
   ```
3. Wrap API functions in arrow functions for queryFn:
   ```typescript
   queryFn: () => listKinder()  // ✅ Good
   queryFn: listKinder          // ❌ May cause type errors
   ```

### Build Issues

If `npm run build` fails with module errors:

```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

## References

- **Backend API Documentation**: See `backend/README.md`
- **DDD Migration**: [ADR-018: Domain-Driven Design](../../documentation/adr/ADR-018-domain-driven-design.md)
- **Frontend Slicing**: [Issue #39](https://github.com/gernotstarke/aquarius/issues/39)
- **DTO/Mapper Pattern**: [ADR-031: DTO/Mapper Pattern](../../documentation/adr/ADR-031-dto-mapper-pattern.md)
