import type { ErrorResponse } from "../Models/ErrorResponse";
export const extractErrors = (err: ErrorResponse | any) => {
    return err.inner.reduce((acc: string[], err: ErrorResponse) => {
        return { ...acc, [err.path]: err.message };
    }, {});
};