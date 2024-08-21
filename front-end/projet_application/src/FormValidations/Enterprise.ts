import * as yup from "yup"

export const entrepriseSchema = yup.object().shape({
    address: yup
        .string()
        .min(3, "L'addresse de l'entreprise doit être au minimum 3 caractères")
        .max(255, "L'adresse de l'entreprise doit être au maximum 255 caractères"),
    cityId: yup
        .number()
        .test(
            "is-number",
            "Vous devez mettre une ville à votre entreprise",
            (value) => {
                return value != undefined ? value >= 1 : false
            }
        ),
    email: yup
        .string()
        .min(4, "Le courriel doit être 4 caractères minimum")
        .max(255, "Le courriel doit être 255 caractères maximum"),
    name: yup
        .string()
        .max(255, "Le nom de votre entreprise doit être maximum 255 caractères"),
    phone: yup
        .string()
        .max(255, "Le numéro de téléphone doit être au maximum 255 caractères")

})