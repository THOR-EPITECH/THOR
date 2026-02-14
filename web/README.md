# 🌐 THOR - Interface Web

Interface web moderne pour THOR (Travel Order Resolver) construite avec Next.js 14, React et Tailwind CSS.

## 📋 Table des matières

- [Vue d'ensemble](#-vue-densemble)
- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Architecture](#-architecture)
- [Composants principaux](#-composants-principaux)
- [Développement](#-développement)

## 🎯 Vue d'ensemble

L'interface web THOR offre une expérience utilisateur complète pour la recherche d'itinéraires ferroviaires :

- 🎤 **Recherche vocale** : Enregistrement audio via microphone
- ⌨️ **Recherche textuelle** : Saisie manuelle de la demande
- 🗺️ **Carte interactive** : Visualisation des trajets avec Leaflet.js
- 🚄 **Détails enrichis** : Temps, distance, types de trains, correspondances

## ✨ Fonctionnalités

### 🔍 Recherche Intelligente

- **Saisie vocale** : Enregistrement et conversion audio → texte
- **Saisie textuelle** : Interface de recherche intuitive
- **Suggestions** : Trajets populaires pré-configurés
- **Validation en temps réel** : Vérification des villes

### 🗺️ Visualisation Cartographique

- **Carte interactive Leaflet** : Affichage sur fond de carte sombre
- **Tracés ferroviaires réels** : Géométries précises des voies SNCF
- **Filtrage intelligent** : Suppression des points géométriques aberrants (>50km)
- **Correspondances visuelles** : Lignes jaunes pointillées pour les transferts inter-gare
- **Tracés partiels** : Lignes pointillées pour géométries incomplètes (<80% valide)
- **Restriction géographique** : Zoom et bounds limités à la France
- **Popups détaillées** : Informations au clic sur les segments

### 🚄 Détails de l'Itinéraire

- **Liste des segments** : Étapes du trajet avec temps et distance
- **Types de trains** : Badges colorés (TGV, OUIGO, Intercités, TER, Correspondance)
- **Correspondances inter-gare** : Affichage en jaune (ex: Paris Montparnasse → Gare de Lyon)
- **Statistiques globales** : Temps total, distance totale, nombre de trains/correspondances

### 📚 Documentation Interactive

- **Pages de documentation** : Guide complet accessible depuis l'interface
- **Installation** : Instructions d'installation et configuration
- **STT** : Détails sur la transcription audio (Whisper)
- **NLP** : Extraction des informations de voyage (spaCy)
- **Pathfinding** : Algorithme Dijkstra optimisé avec pénalités intelligentes
- **Code interactif** : Exemples avec coloration syntaxique

## 📦 Installation

### Prérequis

- Node.js 18+ ou Bun
- L'API THOR doit être démarrée sur `http://localhost:8000`

### Installation des dépendances

```bash
cd web
npm install
```

### Variables d'environnement

Créez un fichier `.env.local` :

```bash
# URL de l'API Flask (optionnel, par défaut via proxy Next.js)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Démarrage

```bash
# Mode développement
npm run dev

# Mode production
npm run build
npm start
```

L'interface sera accessible sur `http://localhost:3000`

## 🏗️ Architecture

### Stack Technique

- **Framework** : [Next.js 14](https://nextjs.org/) (App Router)
- **UI** : [React 18](https://react.dev/) + [TypeScript](https://www.typescriptlang.org/)
- **Styling** : [Tailwind CSS](https://tailwindcss.com/)
- **Cartes** : [Leaflet.js](https://leafletjs.com/) + [React Leaflet](https://react-leaflet.js.org/)
- **Icônes** : [Lucide React](https://lucide.dev/)
- **API** : Fetch vers Flask via proxy Next.js

### Structure du Projet

```
web/
├── src/
│   ├── app/                    # Routes Next.js (App Router)
│   │   ├── page.tsx            # Page d'accueil avec recherche
│   │   ├── layout.tsx          # Layout global
│   │   ├── globals.css         # Styles globaux
│   │   ├── api/                # API Routes (proxy vers Flask)
│   │   │   ├── extract/        # POST /api/extract
│   │   │   ├── transcribe/     # POST /api/transcribe
│   │   │   └── route/          # POST /api/route
│   │   └── docs/               # Pages de documentation
│   │       ├── page.tsx        # Index de la documentation
│   │       ├── installation/   # Guide d'installation
│   │       ├── stt/            # Doc Speech-to-Text
│   │       ├── nlp/            # Doc NLP
│   │       └── pathfinding/    # Doc Pathfinding
│   ├── components/             # Composants React
│   │   ├── SearchInput.tsx     # Barre de recherche vocale/textuelle
│   │   ├── RouteMapClient.tsx  # Carte Leaflet interactive
│   │   ├── RouteDetails.tsx    # Détails de l'itinéraire
│   │   ├── LoadingSpinner.tsx  # Indicateur de chargement
│   │   └── CodeBlock.tsx       # Blocs de code avec coloration
│   └── types/                  # Types TypeScript
│       └── index.ts            # Définitions des interfaces (Route, Segment, etc.)
├── public/                     # Assets statiques
├── package.json                # Dépendances Node.js
├── tsconfig.json               # Configuration TypeScript
├── tailwind.config.ts          # Configuration Tailwind
└── next.config.js              # Configuration Next.js
```

## 🧩 Composants Principaux

### SearchInput

Composant de recherche avec support vocal et textuel.

**Props:**
- `onSearch: (text: string) => void` - Callback lors de la recherche textuelle
- `onVoiceResult: (result: any) => void` - Callback lors de la recherche vocale
- `isLoading: boolean` - État de chargement

**Fonctionnalités:**
- Enregistrement audio via `MediaRecorder` API
- Conversion WebM → WAV automatique
- Upload et traitement via API `/api/transcribe`
- Suggestions de trajets populaires

### RouteMapClient

Composant carte interactive pour afficher les itinéraires.

**Props:**
- `segments: Segment[]` - Liste des segments de l'itinéraire

**Fonctionnalités:**
- **Affichage des tracés ferroviaires** : Polylines avec géométries réelles
- **Filtrage des points aberrants** : Détection des sauts >50km
- **Correspondances inter-gare** : Lignes jaunes pointillées entre derniers/premiers points affichés
- **Tracés incomplets** : Lignes pointillées si <80% des points valides
- **Markers de gares** : Positionnement précis aux extrémités des segments
- **Popups interactives** : Détails au clic (from, to, temps, distance, type)
- **Zone d'interaction agrandie** : Polyline invisible (weight: 15) pour faciliter le clic
- **Restriction France** : `maxBounds` et `minZoom: 5`

**Algorithmes:**
- `calculateDistance(lat1, lon1, lat2, lon2)` : Distance haversine entre 2 points
- `splitIntoValidSegments(coords)` : Filtre les points causant des sauts >50km
- Détection d'inversion de géométrie (si segment filtré est inversé par rapport aux gares)

### RouteDetails

Composant d'affichage des détails de l'itinéraire.

**Props:**
- `route: Route` - Objet route avec métadonnées et segments

**Fonctionnalités:**
- **Résumé global** : Temps total, distance, nombre de trains/correspondances
- **Liste des segments** : Tableau avec from/to, temps, distance, type de train
- **Badges colorés** : TGV (bleu), OUIGO (rose), Intercités (violet), TER (vert), Correspondance (jaune)
- **Détails enrichis** : Nombre de trains par jour, types alternatifs

### CodeBlock

Composant pour afficher du code avec coloration syntaxique.

**Props:**
- `language: string` - Langage (python, bash, json, etc.)
- `children: string` - Code à afficher

**Fonctionnalités:**
- Coloration syntaxique via `highlight.js`
- Bouton de copie
- Numérotation des lignes
- Support multilingue

## 🎨 Styling

### Thème

- **Dark Mode** : Thème sombre par défaut
- **Palette de couleurs** :
  - Background: `bg-[#0a0a0a]`
  - Cards: `bg-zinc-900/50` avec bordure `border-zinc-800/50`
  - Accents: Bleu (TGV), Rose (OUIGO), Violet (Intercités), Vert (TER), Jaune (Correspondance)

### Classes Tailwind Communes

```css
/* Card */
.card {
  @apply bg-zinc-900/50 border border-zinc-800/50 backdrop-blur-sm rounded-lg p-6;
}

/* Bouton primaire */
.btn-primary {
  @apply bg-blue-600 hover:bg-blue-700 text-white rounded-lg px-4 py-2 transition-colors;
}

/* Badge de type de train */
.badge-tgv {
  @apply bg-blue-500/10 text-blue-400 border-blue-500/20;
}
```

## 🔧 Développement

### Commandes Utiles

```bash
# Démarrer en développement
npm run dev

# Build de production
npm run build

# Démarrer en production
npm start

# Linter
npm run lint

# Tests (si configurés)
npm test
```

### Hot Reload

Next.js offre le hot reload automatique :
- Les modifications de composants sont appliquées instantanément
- Les modifications de pages rechargent la page
- Les modifications de `layout.tsx` rechargent l'application

### Debugging

```typescript
// Dans les composants
console.log('Debug info:', data);

// Côté serveur (API Routes)
console.log('[API] Request received:', req.body);
```

Les logs serveur apparaissent dans le terminal, les logs client dans la console du navigateur.

## 🌍 Déploiement

### Vercel (Recommandé)

```bash
# Installer Vercel CLI
npm i -g vercel

# Déployer
vercel
```

### Docker

```bash
# Depuis la racine du projet
docker-compose up -d
```

### Build manuel

```bash
# Build
npm run build

# Le dossier .next/ contient l'application buildée
# Démarrer avec
npm start
```

## 📡 API Endpoints

L'interface communique avec l'API Flask via proxy Next.js :

### POST `/api/extract`

Extraction NLP depuis un texte.

**Body:**
```json
{
  "text": "Je veux aller de Paris à Lyon"
}
```

**Response:**
```json
{
  "origin": "Paris",
  "destination": "Lyon",
  "confidence": 0.95,
  "route": { ... }
}
```

### POST `/api/transcribe`

Transcription audio → texte + extraction NLP.

**Body:** `FormData` avec fichier audio WAV

**Response:**
```json
{
  "transcription": "je veux aller de paris à lyon",
  "extraction": {
    "origin": "Paris",
    "destination": "Lyon",
    "route": { ... }
  }
}
```

### POST `/api/route`

Recherche d'itinéraire direct.

**Body:**
```json
{
  "origin": "Paris",
  "destination": "Lyon"
}
```

**Response:**
```json
{
  "origin": "Paris",
  "destination": "Lyon",
  "segments": [
    {
      "from": "Paris Gare de Lyon",
      "to": "Lyon Part Dieu",
      "temps_min": 120,
      "distance_km": 465,
      "type_train": "TGV",
      "geometry": { ... }
    }
  ],
  "metadata": { ... }
}
```

## 🐛 Dépannage

### Erreur: "Cannot find module 'leaflet'"

```bash
npm install leaflet react-leaflet
npm install -D @types/leaflet
```

### Erreur: "API not responding"

Vérifiez que l'API Flask tourne sur `http://localhost:8000` :

```bash
cd api
python app.py
```

### Carte ne s'affiche pas

Vérifiez que les CSS de Leaflet sont importés dans `layout.tsx` :

```typescript
import 'leaflet/dist/leaflet.css';
```

### Build échoue

Effacez le cache et réinstallez :

```bash
rm -rf .next node_modules
npm install
npm run build
```

## 🔗 Liens Utiles

- [Next.js Documentation](https://nextjs.org/docs)
- [React Leaflet Guide](https://react-leaflet.js.org/docs/start-introduction/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [API THOR](../api/README.md)

---

**Développé avec ❤️ par l'équipe THOR**
