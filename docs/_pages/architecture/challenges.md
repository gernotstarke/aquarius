---
permalink: /challenges/
title: "Herausforderungen in der Architektur"
layout: protected
header:
  overlay_image: /assets/images/splash/aquarius-architecture-header-1500x400.webp
  actions:
    - label: "Startseite"
      url: "/"
    - label: "Anforderungen"
      url: "/requirements/"
    - label: "Architektur"
      url: "/architecture/"
    - label: "Anwendungen"
      url: "/app/"
toc: true
toc_label: "Challenges"
toc_icon: "exclamation-triangle"
---

# Architectural Challenges in Aquarius

This document describes the key architectural challenges that make Aquarius an excellent case study for software architecture education. Each challenge represents real-world problems that require careful architectural decisions and trade-offs.

---

## 1. CAP Theorem & Mobile Rating Consistency

**Challenge:** Mobile judges need to rate performances in real-time, even with unreliable network connectivity, while maintaining data consistency across all devices.

**Conflicts:**
- **Consistency**: All judges should see the same competition state
- **Availability**: Rating must work even offline (spotty WiFi in swimming pools)
- **Partition Tolerance**: Network splits are common during competitions

**Architectural Implications:**
- Choose CP or AP in CAP theorem
- Eventual consistency vs. strong consistency
- Conflict resolution strategies
- CRDT (Conflict-free Replicated Data Types) vs. operational transformation

**Questions for Architecture Students:**
- What happens when two judges rate the same performance offline with different scores?
- How do you merge divergent states when devices reconnect?
- What consistency guarantees are acceptable for competition fairness?

---

## 2. Privacy & Security of Children's Data (GDPR/DSGVO)

**Challenge:** Protect sensitive personal data of minor participants while enabling legitimate competition management.

**Requirements:**
- GDPR/DSGVO compliance for EU participants
- Consent management (parents/guardians)
- Right to be forgotten
- Data minimization
- Access control (who can see what data?)
- Audit logging (who accessed/changed data?)

**Architectural Implications:**
- Data encryption at rest and in transit
- Role-based access control (RBAC)
- Anonymization/pseudonymization strategies
- Secure API authentication
- Data retention policies
- Audit trail architecture

**Questions for Architecture Students:**
- How do you implement "right to be forgotten" while maintaining competition history?
- What data must be retained for legal/insurance purposes?
- How do you balance transparency (results) with privacy (personal data)?

---

## 3. High Availability During Competitions

**Challenge:** System must be 100% available during competition hours - any downtime causes chaos.

**Critical Scenarios:**
- Competition registration opens → spike in traffic
- Results announcement → everyone checks simultaneously
- Mobile judges rating → cannot afford disconnects
- Start number assignment → must not fail mid-competition

**Architectural Implications:**
- Redundancy and failover strategies
- Circuit breakers and graceful degradation
- Offline-first mobile architecture
- Local caching and sync strategies
- Database replication (Turso edge replicas)
- Load balancing and auto-scaling

**Questions for Architecture Students:**
- What happens if the central server crashes mid-competition?
- How do you handle partial system failures (database up, but app server down)?
- What's your RTO (Recovery Time Objective) and RPO (Recovery Point Objective)?

---

## 4. Atomic Start Number Assignment

**Challenge:** Each participant must receive exactly one unique start number, even under concurrent registration.

**Problems:**
- Race conditions in distributed system
- Multiple registration clerks working simultaneously
- Database transaction isolation
- Network delays and retries
- Preliminary vs. final registrations
- Waiting list management when max participants reached

**Architectural Implications:**
- Database-level atomic operations (SELECT FOR UPDATE)
- Optimistic vs. pessimistic locking
- Idempotency of registration API
- Distributed locks (if multi-region)
- Event sourcing for audit trail

**Questions for Architecture Students:**
- How do you prevent duplicate start numbers without serializing all registrations?
- What happens if a registration fails halfway through?
- How do you handle "preliminary" registrations that might become final?

---

## 5. Integration with Swimming Federation API

**Challenge:** Integrate with external Deutscher Schwimm-Verband (DSV) API for participant verification and result reporting.

**API Characteristics:**
- Rate-limited (max 10 requests/minute)
- Unreliable (occasional timeouts)
- Complex authentication (OAuth 2.0 + rotating credentials)
- Strict data format requirements (XML Schema)
- Batch submission windows (results must be submitted within 24h)
- Versioning (API changes without backward compatibility)

**Architectural Implications:**
- Adapter pattern for external API
- Retry strategies with exponential backoff
- Circuit breaker pattern
- Request queuing and throttling
- Caching of verification results
- Graceful degradation (offline verification)
- API versioning strategy

**Questions for Architecture Students:**
- How do you handle API rate limits during peak registration?
- What if the federation API is down during result submission deadline?
- How do you test integration without hammering production API?

---

## 6. Historical Data & Figure Catalog Evolution

**Challenge:** Figure catalogs change over time, but historical competition results must remain comparable.

**Scenarios:**
- New figures added mid-season
- Difficulty ratings adjusted (Figure A was 7.0, now 7.5)
- Figures retired/deprecated
- Rule changes (judging criteria modified)
- Historical analysis: "Compare 2024 vs 2026 competitions"

**Data Integrity Problems:**
- Which figure catalog version was used in a competition?
- Can you re-calculate historical scores with new ratings?
- How do you display figures that no longer exist?
- What if a judge rated a figure that's now invalid?

**Architectural Implications:**
- Temporal data modeling (bitemporal tables)
- Immutable event log
- Versioning of catalog data
- Snapshot isolation for competitions
- Data migration strategies
- Backward-compatible APIs

**Questions for Architecture Students:**
- How do you model "Figure catalog valid from 2024-01-01 to 2024-12-31"?
- Should historical scores be recalculated when difficulty changes?
- How do you handle competitions that span a catalog change?

---

## 7. Real-time Score Aggregation & Display

**Challenge:** Aggregate scores from multiple judges in real-time and display results immediately on public screens.

**Complexity:**
- 5-7 judges rating simultaneously
- Different scoring algorithms (average, drop highest/lowest, weighted)
- Tie-breaking rules
- Live leaderboard updates
- Handling late/corrected scores
- Performance under load (100+ spectators watching)

**Architectural Implications:**
- Event-driven architecture (publish scores as events)
- Stream processing (Kafka, Redis Streams)
- WebSocket for live updates
- CQRS (Command Query Responsibility Segregation)
- Materialized views for leaderboard
- Eventual consistency handling

**Questions for Architecture Students:**
- How do you handle a judge changing their score 5 minutes later?
- What if scores arrive out of order due to network delays?
- How do you prevent flickering/jumping leaderboard displays?

---

## 8. Offline-First Mobile Architecture

**Challenge:** Judges' mobile apps must work perfectly without internet, syncing later when connected.

**Requirements:**
- Full functionality offline (rating, viewing schedules)
- Local data persistence
- Sync when connectivity returns
- Conflict detection and resolution
- Bandwidth optimization (swimming pools have poor WiFi)
- Battery efficiency

**Architectural Implications:**
- Local-first architecture (SQLite on device)
- Turso local replicas with edge sync
- Differential sync (only changed data)
- Compression of sync payloads
- Background sync workers
- Offline queue for operations

**Questions for Architecture Students:**
- How do you sync 50 MB of competition data over slow 3G?
- What if a judge's device runs out of storage during offline operation?
- How do you handle schema migrations when devices are offline for days?

---

## 9. Multi-Tenancy & Competition Isolation

**Challenge:** Multiple competitions running simultaneously must be strictly isolated while sharing infrastructure.

**Scenarios:**
- 5 competitions on same weekend
- Different organizers, different participants
- Shared figure catalog, separate competition data
- Per-competition customization (rules, scoring)
- Cross-competition reports (federation statistics)

**Architectural Implications:**
- Database schema design (shared vs. separate)
- Tenant identification strategy
- Data access policies
- Resource quotas and rate limiting
- Backup and restore per tenant
- Cost allocation

**Questions for Architecture Students:**
- Schema-per-tenant vs. shared-schema with tenant_id?
- How do you prevent Competition A from seeing Competition B's data?
- What if one competition needs a custom scoring algorithm?

---

## 10. Audit Trail & Score Traceability

**Challenge:** Every score and registration change must be traceable for dispute resolution and transparency.

**Requirements:**
- Who changed what, when, and why?
- Immutable history (cannot delete/alter past events)
- Reconstruction of system state at any point in time
- Compliance with sports federation regulations
- Performance (auditing cannot slow down operations)

**Architectural Implications:**
- Event sourcing architecture
- Append-only event log
- Snapshot + replay for performance
- Separate audit storage (WORM - Write Once Read Many)
- Temporal queries
- GDPR compliance (right to be forgotten vs. immutability)

**Questions for Architecture Students:**
- How do you implement event sourcing without killing performance?
- What if you need to "delete" data for GDPR but maintain audit trail?
- How long do you retain event history?

---

## Summary: Cross-Cutting Concerns

These challenges interact and amplify each other:

```
Example Scenario: Judge submits score offline during network outage
↓
Triggers: Offline-first architecture (#8)
↓
Must: Ensure unique start number wasn't duplicated (#4)
↓
Must: Sync eventually with CAP constraints (#1)
↓
Must: Audit who scored what (#10)
↓
Must: Respect GDPR on sync (#2)
↓
Must: Aggregate with other judges' scores (#7)
↓
Must: Display on public screen (#3 - availability)
↓
Must: Work with historical figure catalog (#6)
```

---

## Further Reading

- Martin Kleppmann: "Designing Data-Intensive Applications"
- Eric Evans: "Domain-Driven Design"
- Pat Helland: "Life beyond Distributed Transactions"
- GDPR Technical Guidelines
- arc42 Architecture Documentation Template


[← Zurück zur Architektur-Übersicht](/architecture/)
