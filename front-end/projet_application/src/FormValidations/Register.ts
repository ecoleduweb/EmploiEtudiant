import * as yup from "yup";
import { createForm } from "felte";
import type { RegisterUser } from "../Models/User";
import type { Register } from "../Models/Register";
import { validator } from "@felte/validator-yup";


export const schema = yup.object({
    user: yup.object<RegisterUser>({
        firstName: yup.string().required("Prénom requis").max(255, "Le prénom ne peut pas dépasser 255 caractères"),
        lastName: yup.string().required("Nom de famille requis").max(255, "Le nom de famille ne peut pas dépasser 255 caractères"),
        email: yup.string().email("Courriel invalide").required("Courriel requis").max(255, "Le courriel ne peut pas dépasser 255 caractères"),
        password: yup.string()
            .required("Mot de passe requis")
            .min(12, "Le mot de passe doit comporter au moins 12 caractères")
            .matches(
                /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{12,})/,
                "Ne correspond pas aux critères de sécurité"
            ),
    }),
    validatePassword: yup.string()
        .required("Confirmer le mot de passe")
        .oneOf([yup.ref("user.password")], "Les mots de passes ne correspondent pas"),
});


export const registerTemplate = {
    generate: (): Register => ({
        user: { firstName: "", lastName: "", email: "", password: "" },
        validatePassword: "",
        token: ""
    })
};


export const validateRegisterForm = (handleSubmit: (values: Register) => void, register: Register) => {
    return createForm<any>({
        initialValues: { ...register },
        extend: [validator({ schema })],
        onSubmit: (values) => handleSubmit(values as Register),
    });
}