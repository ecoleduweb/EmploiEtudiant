<script lang="ts">
    import "../../styles/global.css"
    import Button from "../../Components/Inputs/Button.svelte"
    import Link from "../../Components/Inputs/Link.svelte"
    import type { Register } from "../../Models/Register.ts"
    import { extractErrors } from "../../ts/utils"
    import * as yup from "yup"
    import { POST } from "../../ts/server"
    import { env } from "$env/dynamic/public"
    import { writable } from "svelte/store"
    import { logIn } from "../../lib/tokenLib"
    import Popup from "../../Components/Common/Popup.svelte"

    const schema = yup.object({
        user: yup.object({
            firstName: yup.string().required("Prénom requis"),
            lastName: yup.string().required("Nom de famille requis"),
            email: yup
                .string()
                .email("Courriel invalide")
                .required("Courriel requis"),
            password: yup
                .string()
                .required("Mot de passe requis")
                .matches(
                    /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{12,})/,
                    "Ne correspond pas aux critères de sécurité",
                ),
        }),
        validatePassword: yup
            .string()
            .required("Confirmer le mot de passe")
            .oneOf(
                [yup.ref("user.password")],
                "Les mots de passes ne correspondent pas",
            ),
    })
    let errors: { [key: string]: any } = {
        user: {
            id: 0,
            firstName: "",
            lastName: "",
            email: "",
            password: "",
            role: "",
        },
        validatePassword: "",
        token: "",
    }

    let register: Register = {
        user: {
            id: 0,
            firstName: "",
            lastName: "",
            email: "",
            password: "",
            role: "",
        },
        validatePassword: "",
        token: "",
    }
    const validations = writable({
        lowercase: false,
        uppercase: false,
        digit: false,
        specialChar: false,
        length: false,
    })

    let popupEnabled = false

    const closePopup = () => 
    {
        popupEnabled = false
    }

    const handleSubmit = async () => {
        try {
            const lowercaseRegex = /^(?=.*[a-z])/
            const uppercaseRegex = /^(?=.*[A-Z])/
            const digitRegex = /^(?=.*[0-9])/
            const specialCharRegex = /^(?=.*[!@#$%^&*])/
            const lengthRegex = /^(?=.{12,})/

            validations.update((vals) => ({
                ...vals,
                lowercase: lowercaseRegex.test(register.user.password),
                uppercase: uppercaseRegex.test(register.user.password),
                digit: digitRegex.test(register.user.password),
                specialChar: specialCharRegex.test(register.user.password),
                length: lengthRegex.test(register.user.password),
            }))

            await schema.validate(register, { abortEarly: false })
            errors = {
                user: {
                    id: 0,
                    firstName: "",
                    lastName: "",
                    email: "",
                    password: "",
                    role: "",
                },
                validatePassword: "",
                token: "",
            }

            // Get reCAPTCHA token
            const captchaToken = await doRecaptcha() // Get the reCAPTCHA token

            if (captchaToken) {
                // Perform registration only if we have a valid token
                const response: Register = await POST("/user/register", {
                    email: register.user.email,
                    password: register.user.password,
                    firstName: register.user.firstName,
                    lastName: register.user.lastName,
                    role: "user",
                    captchaToken, // Use the retrieved token
                })
                logIn(response.token)
            } else {
                popupEnabled = true
            }
        } catch (error) {
            // Handle error
            console.error("Registration error:", error)
            errors = extractErrors(error) // Custom error extraction function
        }
    }
    let key = env.PUBLIC_RECAPTCHA_KEY
    let token = writable("")

    // Function to get reCAPTCHA token
    const doRecaptcha = async () => {
        return new Promise((resolve) => {
            grecaptcha.ready(() => {
                grecaptcha
                    .execute(key, { action: "submit" })
                    .then((recaptchaToken) => {
                        token.set(recaptchaToken) // Update the Svelte store
                        resolve(recaptchaToken) // Resolve with the token
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
    <form on:submit|preventDefault={handleSubmit} class="form-register">
        <div class="info-block">
            <h2>Informations personnelles</h2>
            <div class="form-fields">
                <div class="form-inputs">
                    <label for="firstName">Prénom</label>
                    <input
                        type="text"
                        id="firstName"
                        bind:value={register.user.firstName}
                    />
                    <p class="errors-input">
                        {#if errors["user.firstName"]}
                            {errors["user.firstName"]}
                        {/if}
                    </p>
                </div>
                <div class="form-inputs">
                    <label for="lastName">Nom de famille</label>
                    <input
                        type="text"
                        class="input-lastName"
                        id="lastName"
                        name="lastName"
                        bind:value={register.user.lastName}
                    />
                    <p class="errors-input">
                        {#if errors["user.lastName"]}
                            {errors["user.lastName"]}
                        {/if}
                    </p>
                </div>
            </div>
        </div>
        <div class="info-block">
            <h2>Informations de l'utilisateur</h2>
            <div class="form-connexion">
                <div class="form-inputs">
                    <label for="email">Courriel</label>
                    <input id="email" bind:value={register.user.email} />
                    <p class="errors-input">
                        {#if errors["user.email"]}
                            {errors["user.email"]}
                        {/if}
                    </p>
                </div>
                <div class="form-inputs">
                    <label for="password">Mot de passe</label>
                    <input
                        type="password"
                        id="password"
                        bind:value={register.user.password}
                    />
                    <p class="errors-input">
                        {#if errors["user.password"]}
                            {errors["user.password"]}
                        {/if}
                    </p>
                </div>
                <div class="form-inputs">
                    <label for="password">Valider Mot de passe</label>
                    <input
                        type="password"
                        id="confirm_password"
                        bind:value={register.validatePassword}
                    />
                    <p class="errors-input">
                        {#if errors.validatePassword}{errors.validatePassword}{/if}
                    </p>
                </div>
                <div class="password-validation-showcase">
                    <ul>
                        {#if !$validations.lowercase}
                            <li>
                                <div class="validation-criteria-item">
                                    <div>Au moins une lettre minuscule</div>
                                    <div>
                                        {$validations.lowercase ? "✅" : "❌"}
                                    </div>
                                </div>
                            </li>
                        {/if}
                        {#if !$validations.uppercase}
                            <li>
                                <div class="validation-criteria-item">
                                    <div style="margin-right:14%">
                                        Au moins une lettre majuscule
                                    </div>
                                    <div>
                                        {$validations.uppercase ? "✅" : "❌"}
                                    </div>
                                </div>
                            </li>
                        {/if}
                        {#if !$validations.digit}
                            <li>
                                <div class="validation-criteria-item">
                                    <div style="margin-right:14%">
                                        Au moins un chiffre
                                    </div>
                                    <div>
                                        {$validations.digit ? "✅" : "❌"}
                                    </div>
                                </div>
                            </li>
                        {/if}
                    </ul>
                    <ul>
                        {#if !$validations.specialChar}
                            <li>
                                <div class="validation-criteria-item">
                                    <div>Au moins un caractère spécial</div>
                                    <div>
                                        {$validations.specialChar ? "✅" : "❌"}
                                    </div>
                                </div>
                            </li>
                        {/if}
                        {#if !$validations.length}
                            <li>
                                <div class="validation-criteria-item">
                                    <div>Au moins 12 caractères</div>
                                    <div>
                                        {$validations.length ? "✅" : "❌"}
                                    </div>
                                </div>
                            </li>
                        {/if}
                    </ul>
                </div>
            </div>
        </div>
        <p class="errors-input">
            {#if errors.token}
                {errors.token}
            {/if}
        </p>
        <div class="form-inputs form-submit">
            <div class="form-buttons">
                <Link text="Retour" href="/" />
            </div>
            <div class="form-buttons">
                <Button cssId="submitButton" submit={true} text="Créer" onClick={() => {}} />
            </div>
        </div>
    </form>

    <style scoped>
        .container {
            padding-bottom: 10%;
        }
    </style>
    {#if popupEnabled}
        <Popup approbationMessage="Le captcha à échoué." handleApproveClick={closePopup}></Popup>
    {/if}
</div>

<style scoped>
    @import "../../styles/register.css";
</style>
