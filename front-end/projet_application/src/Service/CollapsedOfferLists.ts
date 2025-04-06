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

    const storedData = localStorage.getItem(LOCAL_STORAGE_KEY);
    if (!storedData) return { ...defaultStates };

    try {
        const parsedData = JSON.parse(storedData);
        return {
            hideRefusedOffer: parsedData.hideRefusedOffer ?? defaultStates.hideRefusedOffer,
            hideToBeApprovedOffer: parsedData.hideToBeApprovedOffer ?? defaultStates.hideToBeApprovedOffer,
            hideOfferToCome: parsedData.hideOfferToCome ?? defaultStates.hideOfferToCome,
            hideOfferDisplayed: parsedData.hideOfferDisplayed ?? defaultStates.hideOfferDisplayed,
            hideExpiredOffer: parsedData.hideExpiredOffer ?? defaultStates.hideExpiredOffer
        };
    } catch (error) {
        console.error("Error parsing collapse states from localStorage:", error);
        return { ...defaultStates };
    }
}

/**
 * Sauvegarde les états de collapse dans le localStorage
 */
export function storeStatesInStorage(states: CollapseListsStates): void {
    if (!browser) return;

    try {
        localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(states));
    } catch (error) {
        console.error("Error storing collapse states in localStorage:", error);
    }
}

/**
 * Met à jour un état spécifique et sauvegarde tous les états
 */
export function updateState(
    currentStates: CollapseListsStates,
    key: keyof CollapseListsStates,
    value: boolean
): CollapseListsStates {
    const newStates = { ...currentStates, [key]: value };
    storeStatesInStorage(newStates);
    return newStates;
}