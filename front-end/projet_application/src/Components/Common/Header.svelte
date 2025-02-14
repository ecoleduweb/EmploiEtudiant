<script lang="ts">
    import { goto } from "$app/navigation"
    import { onMount } from "svelte"
    import { jwtDecode } from "jwt-decode"
    import type Token from "../../Models/Token"
    import { isLoggedIn, currentUser, studyPrograms } from "$lib" // La variable writable de login.
    import { GET } from "../../ts/server"
    import { decodeToken, disconnectUser, isTokenExpired, logIn, setInfoFromDecoded } from "../../lib/tokenLib"
    import { Hamburger } from 'svelte-hamburgers';
    import { GoogleAnalytics } from '@beyonk/svelte-google-analytics'


    let open: boolean;

    const fetchStudyPrograms = async () => 
    {
        try {
            let response = await GET<any>(
                `/studyProgram/studyPrograms`,
                false
            )

            if (response)
            return response
        } catch (error) {
            console.error("Error fetching job offers:", error)
        }
    }

    onMount(async () => {
        try 
        {
            isLoggedIn.set(!isTokenExpired())

            if ($isLoggedIn)
            {
                const decoded = decodeToken()
                setInfoFromDecoded(decoded)
            }
            else
            {
                disconnectUser()
            }
        }
        catch (err) 
        {}
        finally 
        {
            studyPrograms.set(await fetchStudyPrograms())
        }
    })
    
    const handleEmploi = () => {
        open = false
        goto("/emplois")
    }
    const handleEnterprise = () => {
        open = false
        goto("/enterprise")
    }
    const handleDashboard = () => {
        open = false
        goto("/dashboard")
    }
    const handleUtilisateur = () => {
        open = false
        goto("/users")
    }
    const handleProgrammes = () => {
        open = false
        goto("/programmes")
    }
    const handleProfile = () => 
    {
        open = false
        goto("/profile")
    }
    const handleLogin = () => {
        open = false
        goto("/login")
    }
    const handleRegister = () => {
        open = false
        goto("/register")
    }

    const handleLogout = () => {
        open = false
        isLoggedIn.set(false)
        currentUser.set(undefined)
        goto("/")
        localStorage.removeItem("token")
    }
</script>

<header>
    <div class="logo-img">
        <a href="/" class="image"><img src="logo.png" alt="Logo" /></a>
    </div>
    <!--MENU MOBILE --------------------------- -->
    <div class={$isLoggedIn ? "burger" : "burger-disconnected"}>
        <Hamburger bind:open --color="white"/>
        {#if open}
        <div class="menu-dropdown">
            {#if $currentUser?.isModerator}
            <div class="option">
                <button class="button" on:click={handleEnterprise}>
                    <p class="textSearch">Entreprises</p>
                </button>
                <button class="button" on:click={handleUtilisateur}>
                    <p class="textSearch">Utilisateurs</p>
                </button>
                <button class="button" on:click={handleProgrammes}>
                    <p class="textSearch">Programmes d'études</p>
                    <img class="iconeLogout" src="edit.svg" alt="Edit icon" />
                </button>
                <button class="button" on:click={handleEmploi}>
                    <p class="textSearch">Trouver un emploi</p>
                    <img class="iconeLogout" src="searchBar.svg" alt="Search icon" />
                </button>
                <button class="button" on:click={handleDashboard}>
                    <p class="textSearch">Tableau de bord</p>
                    <img class="iconeLogout" src="searchBar.svg" alt="Search icon" />
                </button>
                <button class="button" on:click={handleProfile}>
                    <p class="textSearch">Connecté en tant que : {$currentUser?.firstName} {$currentUser?.lastName} </p>
                </button>
                <button class="button" on:click={handleLogout}>
                    <p class="textSearch">Déconnexion</p>
                    <img class="iconeLogout" src="logout.svg" alt="Logout icon" />
                </button>
            </div>
            {/if}
            {#if !($currentUser?.isModerator) && $isLoggedIn}
            <div class="option">
                <button class="button" on:click={handleDashboard}>
                    <p class="textSearch">Tableau de bord</p>
                    <img class="iconeSearch" src="searchBar.svg" alt="Search icon" />
                </button>
                <button class="button" on:click={handleLogout}>
                    <p class="textSearch">Déconnexion</p>
                    <img class="iconeLogout" src="logout.svg" alt="Logout icon" />
                </button>
            </div>
            {/if}
            {#if !$isLoggedIn}
            <div class="option">
                <button class="button" on:click={handleEmploi}>
                    <p class="textSearch">Trouver un emploi</p>
                    <img class="iconeLogout" src="searchBar.svg" alt="Search icon" />
                </button>
                <button class="button" on:click={handleLogin}>
                    <p class="textSearch">Connexion entreprise</p>
                    <img class="iconeLogout" src="business.svg" alt="Business icon" />
                </button>
                <button class="button" on:click={handleRegister}>
                    <p class="textSearch">Créer un compte entreprise</p>
                    <img class="iconeLogout" src="add.svg" alt="Add icon" />
                </button>
            </div>
            {/if}
        </div>
        {/if}
    </div>
    <!--MENU MOBILE FIN --------------------------- -->
    
    <div class="ul-group">
        <ul class="ul-menu">
            {#if $currentUser?.isModerator}
                <style scoped>
                    .logo-img {
                        width: 40% !important;
                    }
                </style>
                
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

                <div class="option">
                    <button
                        class="button logout-button"
                        on:click={handleProgrammes}
                    >
                        <p class="textLogout">Programmes d'études</p>
                        <img
                            class="iconeLogout"
                            src="edit.svg"
                            alt="Logout icon"
                        />
                    </button>
                </div>

            {/if}

            <div class="option">
                <button class={$isLoggedIn ? "button" : "button-disconnected"} on:click={handleEmploi}>
                    <p class="textSearch">Trouver un emploi</p>
                    <img
                        class="iconeSearch"
                        src="searchBar.svg"
                        alt="Search icon"
                    />
                </button>
            </div>

            {#if $isLoggedIn}

                {#if $currentUser?.isModerator}
                    <style scoped>
                        .logo-img {
                            width: 45% !important;
                        }
                    </style>
                {/if}

                <div class="option">
                    <button
                        class="button logout-button"
                        on:click={handleDashboard}
                    >
                        <p class="textLogout">Tableau de bord</p>
                        <img
                            class="iconeSearch"
                            src="searchBar.svg"
                            alt="Search icon"
                        />
                    </button>
                </div>

                <div class="option dropdown">
                    <button class="button {$isLoggedIn ? "dropbtn" : "dropbtn-disconnected"}" id="loginDropDown">
                        <img
                            class="iconeProfile"
                            src="profile.svg"
                            alt="Business icon"
                        />
                    </button>
                    <div class="{$currentUser?.isModerator ? "dropdown-content-profile-admin" : "dropdown-content-profile"}">
                        <a href="/profile">Modifier mon profil </a>
                        <a href="/" on:click={handleLogout}>Déconnexion</a>
                    </div>
                </div>

            {:else}

                <div class="option dropdown">
                    <button class="button {$isLoggedIn ? "dropbtn" : "dropbtn-disconnected"}" id="loginDropDown">
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
        </ul>
    </div>
</header>

<style scoped>
    header {
        display: flex;
        flex-direction: row;
        width: 100%;
        height: 6.25vw;
        background-color: #1e2634;
        border-bottom: 1px solid #00ad9a;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }

    .logo-img {
        display: flex;
        justify-items: center;
        align-items: center;
    }

    .image {
        position: relative;
        left: 5vw;
        /* left: 140px; */
        width: 13vw;
        height: fit-content;
    }

    .image img {
        width: 13vw;
        height: auto;
    }

    .ul-group {
        display: flex;
        margin-left: 10vw;
        justify-content: right;
    }

    .ul-menu {
        width: 75vw;
        display: flex;
        justify-content: right;
        list-style: none;
        padding: 0;
        margin: 0;
    }

    button {
        background-color: #1e2634;
        color: white;
        text-decoration: none;
        display: block;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        width: 9vw;
        height: 100%;
        padding: 10px 0px 10px 0px;
    }

    .button-disconnected {
        display: flex;
        justify-content: center;
        align-items: center;
        padding-left: 15px;
        margin-left: 15px;
        margin-right: 15px;
        width: 15vw;
    }	

    .dropbtn-disconnected {
        width: 15vw;
    }


    .option {
        width: 25%;
    }


    button:hover {
        background-color: #555b66;
    }

    .iconeProfile {
        width: 3vw;
    }

    p,
    a {
        color: white;
        margin: 0;
        padding: 0;
        text-align: center;
        width: 100%;
        font-size: 1.1vw;
    }

    /* Existing CSS styles */

    /* Dropdown Button */
    .dropbtn {
        position: relative;
    }

    /* Dropdown Content (Hidden by Default) */
    .dropdown-content {
        display: none;
        position: absolute;
        background-color: #1e2634;
        width: 16.5%;
        box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
        z-index: 1;
        margin-left: 15px;
    }

    .dropdown-content-profile {
        display: none;
        position: absolute;
        background-color: #1e2634;
        width: 16.5%;
        box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
        z-index: 1;
        right : 10vw;
    }

    .dropdown-content-profile-admin {
        display: none;
        position: absolute;
        background-color: #1e2634;
        width: 16.5%;
        box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
        z-index: 1;
        right : 2vw;
    }

        /* Show the dropdown menu on hover */
    .dropdown:hover .dropdown-content,
    .dropdown:hover .dropdown-content-profile,
    .dropdown:hover .dropdown-content-profile-admin {
        display: flex;
        flex-direction: column;
    }

    /* Links inside the dropdown */
    .dropdown-content a,
    .dropdown-content-profile a,
    .dropdown-content-profile-admin a {
        color: white;
        text-decoration: none;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 5.25vw;
        transition: 0.5s;
        background: linear-gradient(
                90deg,
                var(--c1, #268794),
                var(--c2, #2ebaa1) 55%,
                var(--c3, #30a29e) 70%,
                var(--c4, #318e9b) 90%
            )
            var(--x, 0) / 200%;
    }

    /* Change color of dropdown links on hover */
    .dropdown-content a:hover,
    .dropdown-content-profile a:hover,
    .dropdown-content-profile-admin a:hover {
        --x: 100%;
    }

    .button {
        display: flex;
        justify-content: center;
        align-items: center;
        padding-left: 15px;
        margin-left: 15px;
        margin-right: 15px;
    }

    .burger {
        display: none;
    }

    .burger-disconnected {
        display: none;
    }

    .menu-dropdown {
        display: none;
        position: absolute;
        top: 60px; /* Ajustez cette valeur en fonction de la hauteur de votre header */
        left: 0;
        width: 100%;
        background-color: white;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        z-index: 1000;
    }

    .menu-dropdown .option {
        padding: 10px;
        border-bottom: 1px solid #ccc;
    }

    .menu-dropdown .option:last-child {
        border-bottom: none;
    }

    .iconeSearch {
        display: flex;
        align-items: center;
        width: 32px;
        height: 100%;
    }

    .textSearch {
        display: flex;
        align-items: center;
        width: 60%;
        height: 100%;
        margin-right: 8px;
    }

    .textBusiness {
        display: flex;
        align-items: center;
        width: 55%;
        height: 100%;
    }

    .iconeBusiness {
        display: flex;
        align-items: center;
        width: 15%;
        height: 100%;
    }
   

    .logout-button {
        background-color: transparent;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
    }


    .textLogout {
        margin-right: 8px;
    }

    .iconeLogout {
        width: 32px;
    }

    @media (max-width: 768px) {
        header {
        height: 15vw;
        }
        .image img {
            height: 8vW;
            width: 40vw;
        }
        .burger {
            display: flex;
            justify-content: right;
            align-items: right;
            width: 40vw;
        }
        .burger-disconnected {
            display: flex;
            justify-content: right;
            align-items: right;
            width: 40vw;
            margin-left: 32vw;
        }
        .button {
            width: 85vw;
            justify-content: space-between;
            padding-right: 2vw;
        }
        .textSearch {
        display: flex;
        align-items: center;
        width: 100%;
        height: 100%;
        margin-right: 8px;
        font-size: 20px;
        
    }
        .menu-dropdown {
            display: block;
            margin-top: 1vh;
            background-color: rgba(39, 44, 54, 0.767);
        }
        .ul-group {
            display: none;
        }

    }

</style>
