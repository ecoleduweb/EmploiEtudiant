<script lang="ts">
    import "../../styles/global.css"
    import Button from "../../Components/Inputs/Button.svelte"
    import Link from "../../Components/Inputs/Link.svelte"
    import type { Register } from "../../Models/Register.ts"
    import { POST } from "../../ts/server"
    import { env } from "$env/dynamic/public"
    import { logIn } from "../../lib/tokenLib"
    import Popup from "../../Components/Common/Popup.svelte"
    import type { User } from "../../Models/User"
    import {
        validateRegisterForm,
        registerTemplate,
    } from "../../FormValidations/Register"
    const handleSubmit = async (values: Register) => {
        try {
            const captchaToken = await doRecaptcha()

            if (captchaToken) {
                const response = await POST<any, User>("/auth/register", {
                    ...values.user,
                    captchaToken,
                })
                logIn(response.data)
            } else {
                popupEnabled = true
            }
        } catch (error) {
            console.error("Registration error:", error)
            alert("Une erreur est survenue.")
        }
    }

    const { form, errors } = validateRegisterForm(
        handleSubmit,
        registerTemplate.generate(),
    )

    let popupEnabled = $state(false)

    const closePopup = () => {
        popupEnabled = false
    }

    let key = env.PUBLIC_RECAPTCHA_KEY
    let token = $state("")

    const doRecaptcha = async () => {
        return new Promise((resolve) => {
            grecaptcha.ready(() => {
                grecaptcha
                    .execute(key, { action: "submit" })
                    .then((recaptchaToken) => {
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
    <form use:form class="form-register">
        <div class="info-block">
            <h2>Informations <span class="hightlight">personnelles</span></h2>
            <div class="form-fields">
                <div class="form-inputs">
                    <label for="firstName">Prénom</label>
                    <input type="text" id="firstName" name="user.firstName" />
                    {#if $errors.user?.firstName}
                        <p class="errors-input">{$errors.user.firstName}</p>
                    {/if}
                </div>
                <div class="form-inputs">
                    <label for="lastName">Nom de famille</label>
                    <input type="text" id="lastName" name="user.lastName" />
                    {#if $errors.user?.lastName}
                        <p class="errors-input">{$errors.user.lastName}</p>
                    {/if}
                </div>
            </div>
        </div>

        <div class="info-block">
            <h2>
                Informations de l'<span class="hightlight">utilisateur</span>
            </h2>
            <div class="form-connexion">
                <div class="form-inputs">
                    <label for="email">Courriel</label>
                    <input id="email" name="user.email" class="input-basic" />
                    <p class="errors-input">
                        {#if $errors.user?.email}
                            {$errors.user.email}
                        {/if}
                    </p>
                </div>

                <div class="form-inputs">
                    <label for="password">Mot de passe</label>
                    <input
                        class="input-basic"
                        type="password"
                        id="password"
                        name="user.password"
                    />
                    <p>
                        <span class="password-requirements"
                            >Mot de passe complexe (12 caractères, 1 majuscule,
                            1 minuscule, 1 chiffre, 1 caractère spécial)</span
                        >
                    </p>
                    <p class="errors-input">
                        {#if $errors.user?.password}{$errors.user.password}{/if}
                    </p>
                </div>

                <div class="form-inputs">
                    <label for="confirm_password">Valider Mot de passe</label>
                    <input
                        class="input-basic"
                        type="password"
                        id="confirm_password"
                        name="validatePassword"
                    />
                    <p class="errors-input">
                        {#if $errors.validatePassword}
                            {$errors.validatePassword}
                        {/if}
                    </p>
                </div>
            </div>
        </div>

        {#if $errors.token}
            <p class="errors-input">{$errors.token}</p>
        {/if}

        <div class="form-inputs form-submit">
            <div class="form-buttons">
                <Link text="Retour" href="/" />
            </div>
            <div class="form-buttons">
                <Button
                    cssId="submitButton"
                    submit={true}
                    text="Créer"
                    onClick={() => {}}
                />
            </div>
        </div>
    </form>

    {#if popupEnabled}
        <Popup
            approbationMessage="Le captcha à échoué."
            handleApproveClick={closePopup}
        ></Popup>
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
    }
</style>
