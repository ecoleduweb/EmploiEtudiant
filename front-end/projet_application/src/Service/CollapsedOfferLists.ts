import { writable, type Writable } from 'svelte/store';
import { browser } from '$app/environment';

interface CollapseListsStates {
    isRefusedHidden: boolean;
    isToBeApprovedHidden: boolean;
    isToComeHidden: boolean;
    isDisplayedHidden: boolean;
    isExpiredHidden: boolean;
}

class CollapseListsStatesService {
    private localStorageKey = "hiddenListsStates";

    public isRefusedHidden: Writable<boolean> = writable(false);
    public isToBeApprovedHidden: Writable<boolean> = writable(false);
    public isToComeHidden: Writable<boolean> = writable(false);
    public isDisplayedHidden: Writable<boolean> = writable(false);
    public isExpiredHidden: Writable<boolean> = writable(false);

    constructor() {
        // Charger les états uniquement côté client
        if (browser) {
            this.loadHiddenStates();
            this.setupStateSubscriptions();
        }
    }

    // Charger les états depuis le localStorage
    private loadHiddenStates(): void {
        const storedStates = this.getDataFromLocalStorage();

        if (storedStates) {
            this.isRefusedHidden.set(storedStates["btnHideRefusedOfferList"] || false);
            this.isToBeApprovedHidden.set(storedStates["btnHidetoBeApprovedOfferList"] || false);
            this.isToComeHidden.set(storedStates["btnHideOfferToCome"] || false);
            this.isDisplayedHidden.set(storedStates["btnHideOfferDisplayed"] || false);
            this.isExpiredHidden.set(storedStates["btnHideExpiredOffer"] || false);
        }
    }

    // Configurer des abonnements pour sauvegarder automatiquement
    private setupStateSubscriptions(): void {
        this.isRefusedHidden.subscribe(() => this.saveHiddenStates());
        this.isToBeApprovedHidden.subscribe(() => this.saveHiddenStates());
        this.isToComeHidden.subscribe(() => this.saveHiddenStates());
        this.isDisplayedHidden.subscribe(() => this.saveHiddenStates());
        this.isExpiredHidden.subscribe(() => this.saveHiddenStates());
    }

    private getDataFromLocalStorage(): { [key: string]: boolean } | null {
        if (!browser) return null;

        const data = localStorage.getItem(this.localStorageKey);
        return data ? JSON.parse(data) : null;
    }

    private saveHiddenStates(): void {
        if (!browser) return;

        // Créer un objet avec les états actuels
        const stateToStore = {
            "btnHideRefusedOfferList": this.getCurrentValue(this.isRefusedHidden),
            "btnHidetoBeApprovedOfferList": this.getCurrentValue(this.isToBeApprovedHidden),
            "btnHideOfferToCome": this.getCurrentValue(this.isToComeHidden),
            "btnHideOfferDisplayed": this.getCurrentValue(this.isDisplayedHidden),
            "btnHideExpiredOffer": this.getCurrentValue(this.isExpiredHidden)
        };

        // Sauvegarder dans le localStorage
        localStorage.setItem(this.localStorageKey, JSON.stringify(stateToStore));
    }

    // Méthode utilitaire pour obtenir la valeur actuelle d'un store
    private getCurrentValue(store: Writable<boolean>): boolean {
        let value: boolean | undefined;
        store.subscribe(($value) => {
            value = $value;
        })();
        return value ?? false;
    }
}

// Créer une instance unique
export const hiddenListsService = new CollapseListsStatesService();