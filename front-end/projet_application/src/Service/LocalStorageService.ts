

export const addDataToLocalStorage = (key: string, data: any) => {
    localStorage.setItem(key, JSON.stringify(data));
}

export const getDataFromLocalStorage = (key: string) => {
    const data = localStorage.getItem(key);
    return data ? JSON.parse(data) : null;
}

export const removeDataFromLocalStorage = (key: string) => {
    localStorage.removeItem(key);
}

