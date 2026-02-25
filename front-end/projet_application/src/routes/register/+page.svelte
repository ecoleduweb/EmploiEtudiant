<script lang="ts">
    import "../../styles/global.css"
    import Button from "../../Components/Inputs/Button.svelte"
    import Link from "../../Components/Inputs/Link.svelte"
    import type { Register } from "../../Models/Register.ts"
    import { extractErrors } from "../../ts/utils"
    import * as yup from "yup"
    import { POST } from "../../ts/server"
    import { env } from "$env/dynamic/public"
    import { logIn } from "../../lib/tokenLib"
    import Popup from "../../Components/Common/Popup.svelte"

    const schema = yup.object({
        user: yup.object({
            firstName: yup.string().required("Prénom requis"),
            lastName: yup.string().required("Nom de famille requis"),
            email: yup.string().email("Courriel invalide").required("Courriel requis"),
            password: yup.string()
                .required("Mot de passe requis")
                .matches(
                    /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{12,})/,
                    "Ne correspond pas aux critères de sécurité"
                ),
        }),
        validatePassword: yup.string()
            .required("Confirmer le mot de passe")
            .oneOf([yup.ref("user.password")], "Les mots de passes ne correspondent pas"),
    })

    let errors = $state({
        user: { id:0, firstName:"", lastName:"", email:"", password:"", role:"" },
        validatePassword:"",
        token:"",
    })

    let register: Register = $state({
        user: { id:0, firstName:"", lastName:"", email:"", password:"", role:"" },
        validatePassword:"",
        token:"",
    })

    let validations = $state({
        lowercase: false,
        uppercase: false,
        digit: false,
        specialChar: false,
        length: false,
        corresponds: false,
    })

    let popupEnabled = $state(false)
    let showPasswordValidations = $state(false)

    const closePopup = () => { popupEnabled = false }

    const lowercaseRegex = /^(?=.*[a-z])/
    const uppercaseRegex = /^(?=.*[A-Z])/
    const digitRegex = /^(?=.*[0-9])/
    const specialCharRegex = /^(?=.*[!@#$%^&*])/
    const lengthRegex = /^(?=.{12,})/

    function validatePassword() {
        validations = {
            ...validations,
            lowercase: lowercaseRegex.test(register.user.password),
            uppercase: uppercaseRegex.test(register.user.password),
            digit: digitRegex.test(register.user.password),
            specialChar: specialCharRegex.test(register.user.password),
            length: lengthRegex.test(register.user.password),
            corresponds: register.user.password === register.validatePassword,
        }
    }

    const handleSubmit = async (event:any) => {
        event.prevenDefault();
        try {
            validatePassword()
            showPasswordValidations = true
            await schema.validate(register, { abortEarly: false })

            errors = {
                user: { id:0, firstName:"", lastName:"", email:"", password:"", role:"" },
                validatePassword:"",
                token:"",
            }

            const captchaToken = await doRecaptcha()

            if (captchaToken) {
                const response: Register = await POST("/user/register", {
                    email: register.user.email,
                    password: register.user.password,
                    firstName: register.user.firstName,
                    lastName: register.user.lastName,
                    role: "user",
                    captchaToken,
                })
                logIn(response.data.token)
            } else {
                popupEnabled = true
            }
        } catch (error) {
            console.error("Registration error:", error)
            errors = extractErrors(error)
        }
    }

    let key = env.PUBLIC_RECAPTCHA_KEY
    let token = $state("")

    const doRecaptcha = async () => {
        return new Promise((resolve) => {
            grecaptcha.ready(() => {
                grecaptcha.execute(key, { action: "submit" }).then((recaptchaToken) => {
                    token = recaptchaToken
                    resolve(recaptchaToken)
                })
            })
        })
    }
</script>

<svelte:head>
    <script src="https://www.google.com/recaptcha/api.js?render={key}"></script>
</svelte:head>

<div class="container">
    <h1>Créer un compte</h1>
    <form onsubmit={handleSubmit} class="form-register">
        <div class="info-block">
            <h2>Informations <span class="hightlight">personnelles</span></h2>
            <div class="form-fields">
                <div class="form-inputs">
                    <label for="firstName">Prénom</label>
                    <input type="text" id="firstName" bind:value={register.user.firstName} />
                    <p class="errors-input">{#if errors["user.firstName"]}{errors["user.firstName"]}{/if}</p>
                </div>
                <div class="form-inputs">
                    <label for="lastName">Nom de famille</label>
                    <input id="lastName" name="lastName" bind:value={register.user.lastName} />
                    <p class="errors-input">{#if errors["user.lastName"]}{errors["user.lastName"]}{/if}</p>
                </div>
            </div>
        </div>

        <div class="info-block">
            <h2>Informations de l'<span class="hightlight">utilisateur</span></h2>
            <div class="form-connexion">
                <div class="form-inputs">
                    <label for="email">Courriel</label>
                    <input id="email" bind:value={register.user.email} class="input-basic" />
                    <p class="errors-input">{#if errors["user.email"]}{errors["user.email"]}{/if}</p>
                </div>

                <div class="form-inputs">
                    <label for="password">Mot de passe</label>
                    <input class="input-basic" type="password" id="password" bind:value={register.user.password} oninput={validatePassword} />
                    <p><span class="password-requirements">Mot de passe complexe (12 caractères, 1 majuscule, 1 minuscule, 1 chiffre, 1 caractère spécial)</span></p>
                    <p class="errors-input">{#if errors["user.password"]}{errors["user.password"]}{/if}</p>
                </div>

                <div class="form-inputs">
                    <label for="confirm_password">Valider Mot de passe</label>
                    <input class="input-basic" type="password" id="confirm_password" bind:value={register.validatePassword} oninput={validatePassword} />
                    <p class="errors-input">{#if errors.validatePassword}{errors.validatePassword}{/if}</p>
                </div>

                <div class="password-validation-showcase">
                    {#if showPasswordValidations}
                        <ul class="list-requirements">
                            {#if validations.lowercase}<li><span class="text-password-good">✔</span> Contient une lettre minuscule</li>{:else}<li><span class="text-password-error">X</span> Ne contient pas de lettre minuscule</li>{/if}
                            {#if validations.uppercase}<li><span class="text-password-good">✔</span> Contient une lettre majuscule</li>{:else}<li><span class="text-password-error">X</span> Ne contient pas de lettre majuscule</li>{/if}
                            {#if validations.digit}<li><span class="text-password-good">✔</span> Contient un chiffre</li>{:else}<li><span class="text-password-error">X</span> Ne contient pas de chiffre</li>{/if}
                            {#if validations.specialChar}<li><span class="text-password-good">✔</span> Contient un caractère spécial</li>{:else}<li><span class="text-password-error">X</span> Ne contient pas de caractère spécial</li>{/if}
                            {#if validations.length}<li><span class="text-password-good">✔</span> Mot de passe long</li>{:else}<li><span class="text-password-error">X</span> Mot de passe trop court</li>{/if}
                            {#if register.validatePassword != ""}
                                {#if validations.corresponds}<li><span class="text-password-good">✔</span> Mot de passe correspondent</li>{:else}<li><span class="text-password-error">X</span> Mot de passe ne correspondent pas</li>{/if}
                            {/if}
                        </ul>
                    {/if}
                </div>
            </div>
        </div>

        <p class="errors-input">{#if errors.token}{errors.token}{/if}</p>

        <div class="form-inputs form-submit">
            <div class="form-buttons">
                <Link text="Retour" href="/" />
            </div>
            <div class="form-buttons">
                <Button cssId="submitButton" submit={true} text="Créer" onClick={() => {}} />
            </div>
        </div>
    </form>

    {#if popupEnabled}
        <Popup approbationMessage="Le captcha à échoué." handleApproveClick={closePopup}></Popup>
    {/if}
</div>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #f5f5f5;
}

label {
    display: block;
    margin-bottom: 5px;
}

.form-register {
    display: flex;
    flex-direction: column;
    align-items: center;
    border: 1px solid #ccc;
    background-color: #ffff;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    /* Add a subtle box shadow */
    border-radius: 15px;
    width: 60%;
    padding: 0 10px;
}

.form-inputs {
    display: flex;
    flex-direction: column;
    margin: 10px 10px;
    width: 90%;
}

.form-buttons {
    display: flex;
    flex-direction: row;
    padding: 10px 0;
    width: 50%;
    justify-content: center;
    margin: 10px;
}

.form-submit {
    display: flex;
    flex-direction: row;
}

.info-block {
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    width: 80%;
    padding: 10px;
    margin: 10px 0;
    border: 1px solid #c1c1;
    border-radius: 15px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    /* Add a subtle box shadow */
    background-color: #ffff;
}

.form-fields {
    display: flex;
    flex-direction: row;
    margin-left: 10px;
    justify-content: left;
    flex-wrap: wrap;
    width: 100%;
}

.text-password {
    width: 100%;
    text-align: left;
    color: #878787;
    font-size: 12px;
    margin: 0px;
}

.text-password-error {
    width: 100%;
    text-align: left;
    color: #ff0000;
    font-size: 12px;
    margin: 0px;
}

.text-password-good {
    width: 100%;
    text-align: left;
    color: #31f500;
    font-size: 12px;
    margin: 0px;
}

.list-requirements {
    width: 100%;
    color: #878787;
    margin-top: 0px;
    margin-bottom: 20px;
}

.form-connexion {
    flex-direction: column;
    margin: 10px 10px;
    width: 100%;
    justify-content: center;
}

.password-requirements {
    color: #878787;
    font-size: 0.7rem;
    max-width: 90%;
}
/**
Reste à mettre ça responsive :wink:
(Faudrait changer le flex-direction du parent pour column sur tel)

- W

*/
.password-validation-showcase {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-self: center;
    gap: 25%;
    left: 10%;
    margin-top: 3%;
    width: 100%;
}

@media screen and (max-width: 900px) and (min-width: 300px) {
    .form-register {
        width: 85%;
    }

    .container > h1 {
        margin-bottom: 13px;
        margin-top: 13px;
    }

    .form-inputs {
        margin-left: 6%;
        margin-right: 6%;
        width: 100%;
    }

    .input-basic {
        max-width: 85%;
    }

    .password-requirements {
        color: #878787;
        font-size: 0.7rem;
    }

    ul {
        padding-left: 10%;
        min-width: 20%;
    }
}
</style>