export interface Saison {
  id: number;
  name: string;
  from_date: string;
  to_date: string;
}

export interface SaisonCreate {
  name: string;
  from_date: string;
  to_date: string;
}

export interface Schwimmbad {
  id: number;
  name: string;
  adresse: string;
  phone_no?: string;
  manager?: string;
}

export interface SchwimmbadCreate {
  name: string;
  adresse: string;
  phone_no?: string;
  manager?: string;
}

export interface Wettkampf {
  id: number;
  name: string;
  datum: string;
  max_teilnehmer?: number;
  saison_id: number;
  schwimmbad_id: number;
}

export interface WettkampfCreate {
  name: string;
  datum: string;
  max_teilnehmer?: number;
  saison_id: number;
  schwimmbad_id: number;
}

export interface Kind {
  id: number;
  vorname: string;
  nachname: string;
  geburtsdatum: string;
  geschlecht?: string;
  verein?: string;
}

export interface KindCreate {
  vorname: string;
  nachname: string;
  geburtsdatum: string;
  geschlecht?: string;
  verein?: string;
}
