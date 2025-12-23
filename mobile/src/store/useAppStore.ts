import { create } from 'zustand';
import { createJSONStorage, persist } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { User, Wettkampf, Figur } from '../types';

interface AppState {
  token: string | null;
  user: User | null;
  wettkaempfe: Wettkampf[];
  selectedWettkampf: Wettkampf | null;
  selectedFigur: Figur | null;
  
  // Actions
  setAuth: (token: string, user: User) => void;
  logout: () => void;
  setWettkaempfe: (wettkaempfe: Wettkampf[]) => void;
  selectWettkampf: (wettkampf: Wettkampf) => void;
  selectFigur: (figur: Figur) => void;
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      wettkaempfe: [],
      selectedWettkampf: null,
      selectedFigur: null,

      setAuth: (token, user) => set({ token, user }),
      logout: () => set({ token: null, user: null, selectedWettkampf: null, selectedFigur: null }),
      setWettkaempfe: (wettkaempfe) => set({ wettkaempfe }),
      selectWettkampf: (wettkampf) => set({ selectedWettkampf: wettkampf }),
      selectFigur: (figur) => set({ selectedFigur: figur }),
    }),
    {
      name: 'arqua42-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
