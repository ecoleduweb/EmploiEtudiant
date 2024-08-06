import * as yup from "yup"

const schema = yup.object().shape({
    title: yup
        .string()
        .max(255, "Le titre du poste doit être de 255 caractères maximum")
        .required("Le titre du poste est requis"),
    address: yup
        .string()
        .max(
            255,
            "L'adresse du lieu de travail doit être de 255 caractères maximum",
        )
        .required("L'adresse du lieu de travail est requise"),
    description: yup
        .string()
        .max(
            30000,
            "La description de l'offre doit être de 30000 caractères maximum",
        )
        .required("La description de l'offre est requise"),
    dateEntryOffice: yup
        .string()
        .required("La date d'entrée en fonction est requise")
        .test("is-date", "Veuillez choisir une date valide !", (value) => {
            return !isNaN(Date.parse(value))
        }),
    deadlineApply: yup
        .string()
        .required("La date limite de l'offre est requise")
        .test("is-date", "Veuillez choisir une date valide !", (value) => {
            return !isNaN(Date.parse(value))
        }),
    email: yup
        .string()
        .max(255, "Le courriel doit être de 255 caractères maximum")
        .matches(
            /\.[a-z]+$/,
            "Le courriel doit être de format valide : courriel@domaine.ca",
        )
        .email("Le courriel n'est pas valide")
        .required("Le courriel est requis"),
    hoursPerWeek: yup
        .string()
        .required("Le nombre d'heures par semaine est requis")
        .test(
            "is-number",
            "Veuillez entrer un nombre d'heure valide !",
            (value) => {
                return !isNaN(Number(value)) && Number(value) > 0
            },
        ),
    salary: yup
        .string()
        .max(
            255,
            "Le salaire doit être de 255 caractères maximum",
        )
        .required("Le salaire est requis"),
    approbationMessage: yup
        .string()
        .max(
            6000,
            "Le salaire doit être de 6000 caractères maximum",
        ),
    idProgramme: yup.array().min(1, "Le programme visé est requis"),
    acceptCondition: yup
        .boolean()
        .required("Vous devez accepter les conditions")
        .oneOf([true], "Vous devez accepter les conditions"),
    studyPrograms: yup
        .array()
        .min(1, "Le programme visé est requis")
        .required("Le programme visé est requis"),
    scheduleIds: yup
        .array()
        .min(1, "Le type d'emplois est requis")
        .required("Le type d'emplois est requis")
})

export const entrepriseSchema = yup.object().shape({
    address: yup
        .string()
        .required("Vous devez ajouter une adresse à votre entreprise")
        .max(255, "L'adresse de l'entreprise doit être au maximum 255 caractères"),
    cityId: yup
        .number()
        .required("Vous devez mettre une ville à votre entreprise")
        .test(
            "is-number",
            "Vous devez mettre une ville à votre entreprise",
            (value) => {
                return value >= 1
            }
        ),
    email: yup
        .string()
        .required("Vous devez mettre un email à votre entreprise")
        .max(255, "L'email doit être 255 caractères maximum"),
    name: yup
        .string()
        .required("Vous devez nommer votre entreprise")
        .max(255, "Le nom de votre entreprise doit être maximum 255 caractères"),
    phone: yup
        .string()
        .required("Vous devez mettre un numéro de téléphone à votre entreprise")
        .max(255, "Le numéro de téléphone doit être au maximum 255 caractères")

})

export default schema
