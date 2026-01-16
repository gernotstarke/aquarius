# ADR-030: Git Worktrees fuer Parallelarbeit

**Status:** Accepted
**Datum:** 2025-12-18
**Entscheider:** Gernot

## Kontext

Mehrere parallele Aufgaben erfordern getrennte Working Directories ohne ständigen Branch-Wechsel.

## Entscheidung

Wir nutzen Git Worktrees, um parallele Branches lokal in separaten Verzeichnissen zu bearbeiten.

## Konsequenzen

- Schnellere Kontextwechsel ohne Stash/Checkout.
- Mehrere Arbeitsverzeichnisse muessen gepflegt werden.

## Lokales Workflow-Beispiel

```bash
# neuen Worktree fuer Feature-Branch anlegen
git worktree add ../aquarius-arch-feature feature/something

# in den Worktree wechseln
cd ../aquarius-arch-feature

# spaeter: Feature in main integrieren
git switch main
git pull
git switch feature/something
git rebase main
git switch main
git merge feature/something

# Aenderungen aus anderem Branch holen (ohne Wechsel)
git fetch origin
git rebase origin/main
```

## Lokaler Worktree-Wechsler (fzf)

```bash
gw() {
  local wt
  wt=$(git worktree list 2>/dev/null | \
       awk '{print $1 " [" $2 "]"}' | \
       fzf --prompt="Worktree > " \
           --height=40% \
           --reverse) || return

  cd "${wt%% *}"
}
```
