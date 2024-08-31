<script lang="ts">
    import "../../styles/global.css";
    import Button from "../../Components/Inputs/Button.svelte";
    import type { ResetPassword } from "../../Models/ResetPassword";
    import * as yup from "yup";
    import { extractErrors } from "../../ts/utils";
    import { POST } from "../../ts/server";
    import { page } from '$app/stores';
    import { goto } from "$app/navigation";
    import Popup from "../../Components/Common/Popup.svelte";
    import { writable } from "svelte/store";
    import type { Register } from "../../Models/Register";

    const schema = yup.object({
        password: yup
            .string()
            .required("Mot de passe requis")
            .matches(/[a-z]/, "Ne respecte pas les criteres")
            .matches(/[A-Z]/, "Ne respecte pas les criteres")
            .matches(/[0-9]/, "Ne respecte pas les criteres")
            .matches(/[!@#$%^&*]/, "Ne respecte pas les criteres")
            .min(12, "Ne respecte pas les criteres"),
        confirmPassword: yup
            .string()
            .required("Confirmer le mot de passe")
            .oneOf([yup.ref("password"), null], "Les mots de passe ne correspondent pas"),
    });

    const lowercaseRegex = /[a-z]/;
    const uppercaseRegex = /[A-Z]/;
    const digitRegex = /[0-9]/;
    const specialCharRegex = /[!@#$%^&*]/;
    const lengthRegex = /.{12,}/;

    const validations = writable({
        lowercase: false,
        uppercase: false,
        digit: false,
        specialChar: false,
        length: false,
        corresponds: false,
    });

    function validatePassword() {
        validations.update((vals) => ({
            ...vals,
            lowercase: lowercaseRegex.test(resetPassword.password),
            uppercase: uppercaseRegex.test(resetPassword.password),
            digit: digitRegex.test(resetPassword.password),
            specialChar: specialCharRegex.test(resetPassword.password),
            length: lengthRegex.test(resetPassword.password),
            corresponds: resetPassword.password === resetPassword.confirmPassword,
        }));
    }

    let errors: ResetPassword = {
        token: "",
        password: "",
        confirmPassword: "",
    };

    let resetPassword: ResetPassword = {
        token: $page.url.searchParams.get('token'),
        password: "",
        confirmPassword: "",
    };

    let successPopupMessage = "Le mot de passe a été défini avec succès.";
    let failedPopupMessage = "Impossible de changer le mot de passe, lien invalide ou expiré?";

    let popupMessage = "";
    let showPopup = false;

    const handlePopupClose = async () => {
        showPopup = false;
        goto("/login");
    };

    const handleSubmit = async () => {
        try {
            // `abortEarly: false` to get all the errors
            await schema.validate(resetPassword, { abortEarly: false });
            errors = {
                token: "",
                password: "",
                confirmPassword: "",
            };

            if (resetPassword.token == null || resetPassword.token === "") {
                errors = {
                    token: "",
                    password: "",
                    confirmPassword: "Lien invalide",
                };
            }

            try {
                await POST<any, any>("/user/resetPassword", resetPassword);
                popupMessage = successPopupMessage;
            } catch (err) {
                popupMessage = failedPopupMessage;
            }

            showPopup = true;
        } catch (err) {
            console.log(err);
            errors = extractErrors(err);
        }
    };
</script>

<section>
    <div class="forgotPassword">
        <h1>Mot de passe oublié</h1>
        <form class="forgotPassword-form" on:submit|preventDefault={handleSubmit}>
            <label for="password">Entrer un nouveau mot de passe </label>
            <input
                type="password"
                class="input-forgotPassword"
                id="password"
                name="password"
                bind:value={resetPassword.password}
                on:input={validatePassword}
            />
            <p class="errors-input">
                {#if errors.password}{errors.password}{/if}
            </p>
            <label for="confirmPassword">Confirmer le mot de passe </label>
            <input
                type="password"
                class="input-forgotPassword"
                id="confirmPassword"
                name="confirmPassword"
                bind:value={resetPassword.confirmPassword}
                on:input={validatePassword}
            />
            <p class="errors-input">
                {#if errors.confirmPassword}{errors.confirmPassword}{/if}
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
                        <span class="text-password">Ne contient pas de chiffre</span>
                    </li>
                {/if}
                {#if $validations.specialChar}
                    <li>
                        <span class="text-password-good">✔</span>
                        <span class="text-password">Contient un caractère spécial</span>
                    </li>
                {:else}
                    <li>
                        <span class="text-password-error">X</span> 
                        <span class="text-password">Ne contient pas de caractère spécial</span>
                    </li>
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
                {#if resetPassword.confirmPassword != ""}
                    {#if $validations.corresponds}
                        <li>
                            <span class="text-password-good">✔</span> 
                            <span class="text-password">Les mots de passe correspondent</span>
                        </li>
                    {:else}
                        <li> 
                            <span class="text-password-error">X</span> 
                            <span class="text-password">Les mots de passe ne correspondent pas</span>
                        </li>
                    {/if}
                {/if}
            </ul>
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