import * as yup from "yup"
import type { JobOffer } from "../Models/Offre"
import { createForm } from "felte"

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
            100000,
            "La description de l'offre doit être de 100 000 caractères maximum",
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
    offerLink: yup
        .string()
        .max(255, "Le lien vers l'offre doit être de 255 caractères maximum")
        .url("Le lien doit être une URL valide et débuter par https://"), //TODO valider l'url au back
    acceptCondition: yup
        .boolean()
        .required("Vous devez accepter les conditions")
        .oneOf([true], "Vous devez accepter les conditions"),
    studyPrograms: yup
        .array()
        .min(1, "Le programme visé est requis")
        .required("Le programme visé est requis"),
    employmentSchedules: yup
        .array()
        .min(1, "Au moins un type d'emploi est requis")
        .required("Le type d'emploi est requis"),
    enterpriseId: yup
        .number()
        .required("Vous devez choisir une entreprise"),
    enterprise: yup.object().when('enterpriseId', {
        is: (val: number) => val <= 0,
        then: (schema) => schema.shape({
            address: yup
                .string()
                .required("Vous devez ajouter une adresse à votre entreprise")
                .max(255, "L'adresse de l'entreprise doit être au maximum 255 caractères"),
            cityId: yup
                .number()
                .required("Vous devez choisir une ville pour votre entreprise")
                .min(1, "Vous devez choisir une ville pour votre entreprise"),
            email: yup
                .string()
                .required("Votre entreprise doit avoir un courriel")
                .email("Le courriel doit être valide")
                .max(255, "Le courriel doit être 255 caractères maximum"),
            name: yup
                .string()
                .required("Vous devez nommer votre entreprise")
                .max(255, "Le nom de votre entreprise doit être maximum 255 caractères"),
            phone: yup
                .string()
                .required("Vous devez mettre un numéro de téléphone à votre entreprise")
                .max(255, "Le numéro de téléphone doit être au maximum 255 caractères"),
        }),
        otherwise: (schema) => schema.strip(),
    })
})

export const validateForm = (handleSubmit: (values: any) => void, jobOffer: JobOffer) => {
    return createForm({
        initialValues: { ...jobOffer },
        validate: async (values) => {
            try {
                schema.validateSync(values, { abortEarly: false });
                return {};
            } catch (err: any) {
                const errors: any = {};
                err.inner.forEach((value: any) => {
                    errors[value.path] = value.message;
                });
                return errors;
            }
        },
        onSubmit: handleSubmit,
    });
}

export const jobOfferTemplate = {
    generate: (): JobOffer => ({
        id: 0,
        title: "",
        address: "",
        description: "",
        offerDebut: new Date().toISOString().split("T")[0],
        dateEntryOffice: new Date().toISOString().split("T")[0],
        deadlineApply: new Date().toISOString().split("T")[0],
        email: "",
        hoursPerWeek: 0,
        internship: false,
        offerLink: "",
        offerStatus: 0,
        salary: "",
        isApproved: false,
        approbationMessage: "",
        acceptCondition: false,
        employmentSchedules: [],
        studyPrograms: [],
        approvedDate: "",
        enterprise: {
            id: 0,
            name: "",
            address: "",
            email: "",
            phone: "",
            cityId: 0,
            isTemporary: false,
        },
    })
}