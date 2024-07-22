<script lang="ts">
    import "../../styles/global.css"
    import Button from "../../Components/Inputs/Button.svelte"
    import Link from "../../Components/Inputs/Link.svelte"
    import * as yup from "yup"
    import { extractErrors } from "../../ts/utils"
    import type { ForgotPassword } from "../../Models/ForgotPassword.ts"
    import { POST } from "../../ts/server"
    import Popup from "../../Components/Common/Popup.svelte"
    const schema = yup.object().shape({
        email: yup
            .string()
            .required("Entrer un courriel")
            .email("Le courriel n'est pas valide"),
    })

    let errors: ForgotPassword = {
        email: "",
    }

    let login: ForgotPassword = {
        email: "",
    }

    let successPopupMessage = "La requête de changement de mot de passe à été envoyée."
    let failedPopupMessage = "La requête de changement de mot de passe n'a pas pu être envoyée."

    let popupMessage = ""
    let showPopup = false

    const handlePopupClose = async () => 
    {
        showPopup = false
    }

    const handleSubmit = async () => {
        try {
            // `abortEarly: false` to get all the errors
            await schema.validate(login, { abortEarly: false })
            errors = {
                email: "",
            }

            try 
            {
                await POST<any, any>('/user/requestResetPassword', login, false)
                popupMessage = successPopupMessage
            } catch (err) 
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
            <label for="email">Entrez votre courriel</label>
            <input
                type="text"
                class="input-forgotPassword"
                id="email"
                name="email"
                bind:value={login.email}
            />
            <p class="errors-input">
                {#if errors.email}{errors.email}{/if}
            </p>
            <p class="text-password">
                Un courriel vous sera envoyé pour réinitialiser votre mot de
                passe
            </p>

            <div class="buttons">
                <div class="button">
                    <Link text="Retour" href="/login" />
                </div>
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
    @import "../../styles/forgotPassword.css";
</style>
