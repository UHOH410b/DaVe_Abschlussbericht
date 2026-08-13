# Deployment

Die Anwendung benötigt eine Node.js-kompatible Laufzeit und einen erreichbaren Weaviate-Cluster.

## Beispiel: Vercel

1. Repository mit Vercel verbinden.
2. Als Projektwurzel `02_Agrardatenkatalog_Base44/App_Code` auswählen.
3. Folgende Umgebungsvariablen setzen:

```env
WEAVIATE_URL="https://dein-cluster.weaviate.cloud"
WEAVIATE_API_KEY="dein-weaviate-api-key"
WEAVIATE_COLLECTION="AtomicRequirement"
SEARCH_LIMIT_DEFAULT="30"
```

4. Build mit `npm run build` ausführen.
5. Nach dem Deployment Quellenübersicht, Beispielsuche und Detailansicht testen.

## Sicherheit und Betrieb

- Der Weaviate-Schlüssel darf nur serverseitig gesetzt werden.
- `.env` und `.env.local` dürfen nicht versioniert werden.
- Für einen produktiven Einsatz fehlen unter anderem Authentifizierung, Rollen- und Rechtekonzept, Protokollierung, Monitoring und ein fachlicher Freigabeprozess.
- Bei einer Ablösung von Weaviate müssen die beiden serverseitigen API-Routen an die neue Datenquelle angepasst werden.
