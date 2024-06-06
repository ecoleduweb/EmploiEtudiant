<script lang="ts">
    import { goto } from "$app/navigation"
    import { onMount } from "svelte"
    import { jwtDecode } from "jwt-decode"
    import type Token from "../../Models/Token"
    import { isLoggedIn, currentUser } from "$lib" // La variable writable de login.

    let firstName = "" // Déclarer une variable pour stocker l'email
    let lastName = "" // Déclarer une variable pour stocker l'email
    let isModerator = false

    
    onMount(async () => {
        const token = localStorage.getItem("token")
        isLoggedIn.set(!!token)
        if (token) {
            var decoded = jwtDecode<Token>(token)
            
            currentUser.set(decoded)

            firstName = decoded.firstName
            lastName = decoded.lastName
            isModerator = decoded.isModerator
        }
    })
    
    const handleEmploi = () => {
        goto("/emplois")
    }
    const handleEnterprise = () => {
        goto("/enterprise")
    }
    const handleDashboard = () => {
        goto("/dashboard")
    }
    const handleUtilisateur = () => {
        goto("/utilisateur")
    }

    const handleLogout = () => {
        isLoggedIn.set(false)
        goto("/")
        localStorage.removeItem("token")
    }
</script>

<header>
    <div class="logo-img">
        <a href="/" class="image"><img src="logo.png" alt="Logo" /></a>
    </div>
    <div class="ul-group">
        <ul class="ul-menu">
            {#if $isLoggedIn}
                <div class="option">
                    <p class="email">
                        <br />Connecté en tant que <br />{firstName}
                        {lastName}
                    </p>
                </div>
                <div class="option">
                    <button
                        class="button logout-button"
                        on:click={handleLogout}
                    >
                        <p class="textLogout">Déconnexion</p>
                        <img
                            class="iconeLogout"
                            src="logout.svg"
                            alt="Logout icon"
                        />
                    </button>
                </div>
                <div class="option">
                    <button
                        class="button logout-button"
                        on:click={handleDashboard}
                    >
                        <p class="textLogout">Tableau de bord</p>
                    </button>
                </div>
                {#if isModerator}
                    <div class="option">
                        <button
                            class="button logout-button"
                            on:click={handleEnterprise}
                        >
                            <p class="textLogout">Entreprises</p>
                        </button>
                    </div>
                    <div class="option">
                        <button
                            class="button logout-button"
                            on:click={handleUtilisateur}
                        >
                            <p class="textLogout">Utilisateurs</p>
                        </button>
                    </div>
                {/if}
            {:else}
                <div class="option dropdown">
                    <button class="button dropbtn">
                        <p class="textBusiness">Offrir un emploi</p>
                        <img
                            class="iconeBusiness"
                            src="business.svg"
                            alt="Business icon"
                        />
                    </button>
                    <div class="dropdown-content">
                        <a href="/login">Connexion entreprise</a>
                        <a href="/register">Créer un compte entreprise</a>
                    </div>
                </div>
            {/if}
            <div class="option">
                <button class="button" on:click={handleEmploi}>
                    <p class="textSearch">Trouver un emploi</p>
                    <img
                        class="iconeSearch"
                        src="searchBar.svg"
                        alt="Search icon"
                    />
                </button>
            </div>
        </ul>
    </div>
</header>

<style scoped>
    @import "../../styles/header.css";

    .logout-button {
        background-color: transparent;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
    }

    .textLogout,
    .email {
        margin-right: 8px;
    }

    .iconeLogout {
        width: 24px;
    }
</style>
