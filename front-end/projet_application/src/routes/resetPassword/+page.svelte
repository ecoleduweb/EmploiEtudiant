<script lang="ts">
    import "../../styles/global.css"
    import Button from "../../Components/Inputs/Button.svelte"
    import type { ResetPassword } from "../../Models/ResetPassword"
    import * as yup from "yup"
    import { extractErrors } from "../../ts/utils"
    import { POST } from "../../ts/server"
    import { page } from '$app/stores'
    import { goto } from "$app/navigation"
    import Popup from "../../Components/Common/Popup.svelte"
    import { writable } from "svelte/store"

    const schema = yup.object({
        password: yup
            .string()
            .required("Mot de passe requis")
            .matches(
                /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{12,})/,
                "Ne correspond pas aux critères de sécurité",
            ),
        confirmPassword: yup
            .string()
            .required("Confirmer le mot de passe")
            .oneOf(
                [yup.ref("password"), null],
                "Les mots de passes ne correspondent pas",
            ),
    })

    let register = {
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

    const lowercaseRegex = /^(?=.*[a-z])/
    const uppercaseRegex = /^(?=.*[A-Z])/
    const digitRegex = /^(?=.*[0-9])/
    const specialCharRegex = /^(?=.*[!@#$%^&*])/
    const lengthRegex = /^(?=.{12,})/

    const validations = writable({
        lowercase: false,
        uppercase: false,
        digit: false,
        specialChar: false,
        length: false,
        corresponds: false,
    })
    
    function validatePassword()
    {
        validations.update((vals) => ({
                ...vals,
                lowercase: lowercaseRegex.test(register.user.password),
                uppercase: uppercaseRegex.test(register.user.password),
                digit: digitRegex.test(register.user.password),
                specialChar: specialCharRegex.test(register.user.password),
                length: lengthRegex.test(register.user.password),
                corresponds: register.user.password == register.validatePassword,
            }))
    }

    let errors: ResetPassword = {
        token: "",
        password: "",
        confirmPassword: "",
    }

    let resetPassword: ResetPassword = {
        token: $page.url.searchParams.get('token'),
        password: "",
        confirmPassword: "",
    }

    let successPopupMessage = "Le mot de passe a été défini avec succès."
    let failedPopupMessage = "Impossible de changer le mot de passe, lien invalide ou expiré?"

    let popupMessage = ""
    let showPopup = false

    const handlePopupClose = async () => 
    {
        showPopup = false
        goto("/login")
    }

    const handleSubmit = async () => {
        try {
            // `abortEarly: false` to get all the errors
            await schema.validate(resetPassword, { abortEarly: false })
            errors = {
                token: "",
                password: "",
                confirmPassword: "",
            }

            if (resetPassword.token == null || resetPassword.token == "") 
            {
                errors = {
                    token: "",
                    password: "",
                    confirmPassword: "Lien invalide"
                }
            }

            try 
            {
                await POST<any,any>("/user/resetPassword", resetPassword)
                popupMessage = successPopupMessage
                
            }
            catch (err) 
            {
                popupMessage = failedPopupMessage
            }

            showPopup = true
        } catch (err) {
            errors = extractErrors(err)
        }
    }
</script>

<section>
    <div class="forgotPassword">
        <h1>Mot de passe oublié</h1>
        <form
            class="forgotPassword-form"
            on:submit|preventDefault={handleSubmit}
        >
            <label for="email">Entrer un nouveau mot de passe </label>
            <input
                type="password"
                class="input-forgotPassword"
                id="password"
                name="password"
                bind:value={resetPassword.password}
            />
            <p class="errors-input">
                {#if errors.password}{errors.password}{/if}
            </p>
            <p class="text-title">
                Votre mot de passe doit contenir au minimum :
            </p>
            <ul class="list-requirements">
                {#if $validations.lowercase}
                <li>
                    <span class="text-password-good">✔</span>
                    <span class="text-password">Contient une lettre minuscule</span>
                </li>
            {:else}
                <li>
                    <span class="text-password-error">X</span> 
                    <span class="text-password">Ne contient pas de lettre minuscule</span>
                </li>
            {/if}
        
            {#if $validations.uppercase}
                <li>
                    <span class="text-password-good">✔</span>
                    <span class="text-password">Contient une lettre majuscule</span>
                </li>
            {:else}
                <li>
                    <span class="text-password-error">X</span> 
                    <span class="text-password">Ne contient pas de lettre majuscule</span>
                </li>
            {/if}
            {#if $validations.digit}
                <li>
                    <span class="text-password-good">✔</span>
                    <span class="text-password">Contient un chiffre</span>
                </li>
            {:else}
                <li>
                    <span class="text-password-error">X</span> 
                    <span class="text-password">Ne contient pas de chiffre</span></li>
            {/if}
            {#if $validations.specialChar}
                <li>
                    <span class="text-password-good">✔</span>
                    <span class="text-password">Contient un caractère spécial</span></li>
            {:else}
                <li>
                    <span class="text-password-error">X</span> 
                    <span class="text-password">Ne contient pas de caractère spécial</span></li>
            {/if}
        
            {#if $validations.length}
                <li>
                    <span class="text-password-good">✔</span> 
                    <span class="text-password">Mot de passe long</span>
                </li>
            {:else}
                <li> 
                    <span class="text-password-error">X</span> 
                    <span class="text-password">Mot de passe trop court</span>
                </li>
            {/if}

            {#if $validations.corresponds && resetPassword.confirmPassword != ""}
            <li>
                <span class="text-password-good">✔</span> 
                <span class="text-password">Mot de passe correspondent</span>
            </li>
        {:else}
            <li> 
                <span class="text-password-error">X</span> 
                <span class="text-password">Mot de passe trop court</span>
            </li>
        {/if}
            </ul>
            <label for="email">Confirmer le mot de passe </label>
            <input
                type="password"
                class="input-forgotPassword"
                id="confirmPassword"
                name="confirmPassword"
                bind:value={resetPassword.confirmPassword}
            />
            <p class="errors-input">
                {#if errors.confirmPassword}{errors.confirmPassword}{/if}
            </p>
            <div class="buttons">
                <div class="button">
                    <Button text="Confirmer" submit={true} />
                </div>
            </div>
        </form>
    </div>
    {#if showPopup}
        <Popup handleApproveClick={handlePopupClose} approbationMessage={popupMessage}></Popup>
    {/if}
</section>

<style scoped>
    @import "../../styles/resetPassword.css";
</style>
