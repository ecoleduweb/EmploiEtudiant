import { browser } from '$app/environment';

export interface CollapseListsStates {
    hideRefusedOffer: boolean;
    hideToBeApprovedOffer: boolean;
    hideOfferToCome: boolean;
    hideOfferDisplayed: boolean;
    hideExpiredOffer: boolean;
}

const defaultStates: CollapseListsStates = {
    hideRefusedOffer: false,
    hideToBeApprovedOffer: false,
    hideOfferToCome: false,
    hideOfferDisplayed: false,
    hideExpiredOffer: false
};

const LOCAL_STORAGE_KEY = "hiddenListsStates";

export function getStatesFromStorage(): CollapseListsStates {
    if (!browser) return { ...defaultStates };

    const stored = localStorage.getItem(LOCAL_STORAGE_KEY);
    if (!stored) return { ...defaultStates };

    try {
        const parsed = JSON.parse(stored);
        return parsed as CollapseListsStates;
    } catch (e) {
        console.error("Erreur lors du parse des états:", e);
        return { ...defaultStates };
    }
}

export function storeStatesInStorage(states: CollapseListsStates): void {
    if (!browser) return;

    try {
        localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(states));
    } catch (e) {
        console.error("Erreur lors du stockage des états:", e);
    }
}

export function updateState(
    currentStates: CollapseListsStates,
    key: keyof CollapseListsStates,
    value: boolean
): CollapseListsStates {
    const newStates = { ...currentStates, [key]: value };
    storeStatesInStorage(newStates);
    return newStates;
}
