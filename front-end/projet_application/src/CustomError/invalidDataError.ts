export interface InvalidDataError extends Error {
    field: string;
    name: "InvalidDataError";
}

export function createInvalidDataError(message: string, field: string): InvalidDataError {
    const error = new Error(message) as InvalidDataError;
    error.field = field;
    error.name = "InvalidDataError";
    return error;
}