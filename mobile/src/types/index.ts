export interface User {
  username: string;
  email?: string;
  full_name?: string;
  is_active: boolean;
  role: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface Wettkampf {
  id: number;
  name: string;
  datum: string;
  saison_id: number;
  schwimmbad_id: number;
}

export interface Figur {
  id: number;
  name: string;
  beschreibung?: string;
  schwierigkeitsgrad?: number;
  kategorie?: string;
  altersklasse?: string;
  bild?: string;
}

export interface AuthState {
  token: string | null;
  user: User | null;
  setAuth: (token: string, user: User) => void;
  logout: () => void;
}
