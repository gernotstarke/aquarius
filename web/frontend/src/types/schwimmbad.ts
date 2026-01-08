/**
 * Schwimmbad Types - Swimming pool / venue management
 *
 * These types align with the Schwimmbad domain in the backend.
 */

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
