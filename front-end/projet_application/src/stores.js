import { writable } from 'svelte/store';

export const userToken = writable(null);  // Stocker l'email de l'utilisateur
