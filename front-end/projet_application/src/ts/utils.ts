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