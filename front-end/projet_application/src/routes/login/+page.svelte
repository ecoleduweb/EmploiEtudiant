<script lang="ts">
    import "../../styles/global.css"
    import Button from "../../Components/Inputs/Button.svelte"
    import Link from "../../Components/Inputs/Link.svelte"
    import type { Login } from "../../Models/Login"
    import { GET, POST } from "../../ts/server"
    import * as yup from "yup"
    import { extractErrors } from "../../ts/utils"
    import { goto } from "$app/navigation"
    import { jwtDecode } from "jwt-decode"
    import { currentUser, isLoggedIn } from "$lib"
    import { onMount } from "svelte"
    import Error from "../+error.svelte"


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
                    
                    if (response.token != "") {
                        localStorage.setItem("token", response.token)
                        
                        const decodedUser = jwtDecode(response.token)
                        currentUser.set(decodedUser) //Sauvegarder l'utilisateur décodé

                        goto("/dashboard")
                        isLoggedIn.set(true) //L'utilisateur est maintenant connecté
                    }

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

    const isTokenExpired = (user: any) => {
        try {
            const currentTime = Math.floor(Date.now() / 1000);
            return user.exp < currentTime
        } catch (error) {
            return true;
        }
    }

    onMount(async () => 
    {
        if ($isLoggedIn && isTokenExpired(currentUser))
        {
            localStorage.token = undefined
            currentUser.set(undefined)
            isLoggedIn.set(false)
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
