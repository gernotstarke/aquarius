# ADR-003: TanStack Query für Server State Management

**Status:** Akzeptiert
**Datum:** 2025-12-17
**Entscheider:** Architektur-Team

## Kontext

Die Frontend-Anwendungen müssen Daten vom Backend-API laden, cachen, aktualisieren und synchronisieren. Dies erfordert ein robustes State-Management-System für Server-State.

## Entscheidung

Wir verwenden **TanStack Query (React Query)** für Server State Management in beiden Frontend-Modulen.

## Begründung

### Vorteile

- **Automatic Caching** - Verhindert unnötige API-Calls
- **Background Refetching** - Hält Daten aktuell
- **Optimistic Updates** - Sofortiges UI-Feedback
- **Retry Logic** - Automatische Wiederholungen bei Fehlern
- **DevTools** - Exzellente Debugging-Erfahrung
- **TypeScript-First** - Vollständige Type-Safety
- **Offline Support** - Funktioniert mit Service Worker
- **Window Focus Refetching** - Smart Data Synchronization

### Alternativen

| Alternative | Grund für Ablehnung |
|-------------|---------------------|
| **Redux + RTK Query** | Zu viel Boilerplate, komplexere API |
| **SWR** | Weniger Features, kleinere Community |
| **Apollo Client** | Nur für GraphQL, Overkill für REST |
| **Eigene Lösung** | Wartungsaufwand, Fehleranfälligkeit |

## Konsequenzen

### Positiv

- Drastisch reduzierter Boilerplate-Code
- Automatische Loading- und Error-States
- Optimierte Performance durch intelligentes Caching
- Offline-Fähigkeit gut integrierbar
- Konsistente Datensynchronisation

### Negativ

- Learning Curve für Team
- Zusätzliche Abhängigkeit (minimal, da well-maintained)

## Technische Details

```typescript
// Query Hook Beispiel
export const useWettkampf = (id: string) => {
  return useQuery({
    queryKey: ['wettkampf', id],
    queryFn: () => api.wettkampf.getById(id),
    staleTime: 5 * 60 * 1000, // 5 Minuten
  });
};

// Mutation Hook Beispiel
export const useCreateAnmeldung = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: AnmeldungCreate) => api.anmeldung.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['anmeldungen'] });
    },
  });
};
```

**Dependencies:**
```json
{
  "@tanstack/react-query": "^5.0.0",
  "@tanstack/react-query-devtools": "^5.0.0"
}
```

## Integration mit PWA

TanStack Query persistiert den Cache im Service Worker, um Offline-Funktionalität zu gewährleisten.
