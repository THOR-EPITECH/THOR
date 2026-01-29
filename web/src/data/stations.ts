// Positions GPS des principales gares françaises
export const stationPositions: Record<string, { lat: number; lon: number }> = {
  'Paris Montparnasse': { lat: 48.8412, lon: 2.3205 },
  'Paris Gare de Lyon': { lat: 48.8443, lon: 2.3737 },
  'Paris Nord': { lat: 48.8809, lon: 2.3553 },
  'Paris Est': { lat: 48.8767, lon: 2.3584 },
  'Paris Saint-Lazare': { lat: 48.8762, lon: 2.3253 },
  'Lyon Part-Dieu': { lat: 45.7602, lon: 4.8597 },
  'Lyon Perrache': { lat: 45.7485, lon: 4.8262 },
  'Marseille Saint-Charles': { lat: 43.3028, lon: 5.3804 },
  'Bordeaux Saint-Jean': { lat: 44.8256, lon: -0.5566 },
  'Toulouse Matabiau': { lat: 43.6112, lon: 1.4537 },
  'Nantes': { lat: 47.2173, lon: -1.5418 },
  'Rennes': { lat: 48.1035, lon: -1.6726 },
  'Lille Flandres': { lat: 50.6365, lon: 3.0698 },
  'Lille Europe': { lat: 50.6388, lon: 3.0754 },
  'Strasbourg': { lat: 48.5850, lon: 7.7350 },
  'Nice Ville': { lat: 43.7049, lon: 7.2620 },
  'Montpellier Saint-Roch': { lat: 43.6047, lon: 3.8808 },
  'Biarritz': { lat: 43.4682, lon: -1.5490 },
  'Bayonne': { lat: 43.4929, lon: -1.4748 },
  'Dax': { lat: 43.7102, lon: -1.0537 },
  'Avignon TGV': { lat: 43.9217, lon: 4.7863 },
  'Aix-en-Provence TGV': { lat: 43.4553, lon: 5.3173 },
  'Massy TGV': { lat: 48.7253, lon: 2.2608 },
  'Le Mans': { lat: 47.9954, lon: 0.1921 },
  'Poitiers': { lat: 46.5827, lon: 0.3333 },
  'Angoulême': { lat: 45.6500, lon: 0.1557 },
  'Tours': { lat: 47.3900, lon: 0.6933 },
  'Saint-Pierre-des-Corps': { lat: 47.3858, lon: 0.7256 },
  'Marne-la-Vallée Chessy': { lat: 48.8722, lon: 2.7767 },
  'Lyon Saint-Exupéry TGV': { lat: 45.7219, lon: 5.0778 },
  'Valence TGV': { lat: 44.9785, lon: 4.9697 },
  'Grenoble': { lat: 45.1915, lon: 5.7148 },
  'Annecy': { lat: 45.9023, lon: 6.1211 },
  'Dijon Ville': { lat: 47.3234, lon: 5.0271 },
  'Besançon Franche-Comté TGV': { lat: 47.3075, lon: 5.9563 },
  'Mulhouse Ville': { lat: 47.7426, lon: 7.3426 },
  'Reims': { lat: 49.2583, lon: 4.0243 },
  'Orléans': { lat: 47.9089, lon: 1.9052 },
  'Le Havre': { lat: 49.4944, lon: 0.1226 },
  'Rouen Rive Droite': { lat: 49.4489, lon: 1.0937 },
  'Caen': { lat: 49.1782, lon: -0.3469 },
  'Brest': { lat: 48.3878, lon: -4.4803 },
  'Quimper': { lat: 47.9975, lon: -4.0963 },
  'Lorient': { lat: 47.7457, lon: -3.3653 },
  'Vannes': { lat: 47.6586, lon: -2.7583 },
  'Saint-Brieuc': { lat: 48.5156, lon: -2.7606 },
  'Saint-Malo': { lat: 48.6481, lon: -2.0082 },
  'La Rochelle Ville': { lat: 46.1528, lon: -1.1476 },
  'Perpignan': { lat: 42.6977, lon: 2.8797 },
  'Nîmes': { lat: 43.8328, lon: 4.3653 },
  'Clermont-Ferrand': { lat: 45.7792, lon: 3.0997 },
  'Limoges Bénédictins': { lat: 45.8363, lon: 1.2679 },
};

export function getStationPosition(stationName: string): { lat: number; lon: number } | null {
  // Recherche exacte
  if (stationPositions[stationName]) {
    return stationPositions[stationName];
  }
  
  // Recherche partielle
  const normalizedName = stationName.toLowerCase();
  for (const [name, pos] of Object.entries(stationPositions)) {
    if (name.toLowerCase().includes(normalizedName) || normalizedName.includes(name.toLowerCase())) {
      return pos;
    }
  }
  
  return null;
}
