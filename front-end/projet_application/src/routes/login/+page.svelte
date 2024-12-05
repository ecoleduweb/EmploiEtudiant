<script lang="ts">
    import "../../styles/global.css"
    import Button from "../../Components/Inputs/Button.svelte"
    import Link from "../../Components/Inputs/Link.svelte"
    import type { Login } from "../../Models/Login"
    import { POST } from "../../ts/server"
    import * as yup from "yup"
    import { extractErrors } from "../../ts/utils"
    import { isLoggedIn } from "$lib"
    import { onMount } from "svelte"
    import { disconnectUser, isTokenExpired, logIn } from "../../lib/tokenLib"


    const schema = yup.object().shape({
        email: yup
            .string()
            .required("Entrer un courriel")
            .email("Le courriel n'est pas valide"),
        password: yup.string().required("Le mot de passe est requis"),
    })

    let errors: Login = {
        email: "",
        password: "",
    }

    let form: Login = {
        email: "",
        password: "",
    }

    const handleSubmit = async () => {
        try {
            // `abortEarly: false` to get all the errors
            await schema.validate(form, { abortEarly: false })
            errors = {
                email: "",
                password: "",
            }
            try {
                try {
                    const response = await POST<Login, any>("/user/login", form, false)
                    logIn(response.data.token)
                }
                catch (err) 
                {
                    if (err.name == 403) 
                    {
                        errors = {
                            email: "",
                            password: "Compte désactivé",
                        }
                    }
                    else 
                    {
                        throw err
                    }

                }
            } catch (error) {
                errors = {
                    email: "",
                    password: "Courriel ou mot de passe invalide",
                }
            }
        } catch (err) {
            errors = extractErrors(err)
        }
    }


    onMount(async () => 
    {
        if ($isLoggedIn && isTokenExpired())
        {
            disconnectUser()
        }
    })
</script>

<section>
    <div class="login">
        <h1>Authentification</h1>
        <form on:submit|preventDefault={handleSubmit} class="login-form">
            <label for="email">Nom d'utilisateur</label>
            <input
                type="text"
                class="input-login"
                id="email"
                name="email"
                bind:value={form.email}
            />
            <p class="errors-input">
                {#if errors.email}{errors.email}{/if}
            </p>
            <label for="password">Mot de passe</label>
            <input
                type="password"
                class="input-login"
                id="password"
                name="password"
                bind:value={form.password}
            />
            <p class="errors-input">
                {#if errors.password}{errors.password}{/if}
            </p>
            <Button text="Se connecter" submit={true} />
            <div class="submit">
                <Link href="forgotPassword" text="Mot de passe oublié ?" />
            </div>
            <Link href="register" text="Créer un utilisateur" />
        </form>
    </div>
</section>

<style scoped>
    @import "../../styles/login.css";
</style>
