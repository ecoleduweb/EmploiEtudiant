import type { ErrorResponse } from "../Models/ErrorResponse"
export const extractErrors = (err: ErrorResponse | any) => {
    return err.inner.reduce((acc: string[], err: ErrorResponse) => {
        return { ...acc, [err.path]: err.message }
    }, {})
}

export const toFormattedDateString = (date: Date): string => {
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
}


export const formatPhoneNumber = (phone: string): string => {
    // Supprime tous les caractères non numériques
    const cleaned = phone.replace(/\D/g, '');
    const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
    if (match) {
        return `(${match[1]}) ${match[2]}-${match[3]}`;
    }
    return phone;
};

export const getShortURL = (url: string) => {
    try {
        const { hostname } = new URL(url);
        return hostname;
    } catch (e) {
        return url;
    }
};

export const isObjectEmpty = (obj: any) => {
    return Object.keys(obj).length === 0;
}