<script lang="ts">
    import "../../styles/global.css"
    import { onMount } from "svelte"
    import { writable } from "svelte/store"
    import { GET } from "../../ts/server"
    import type { User } from "../../Models/User"
    import UserConfigurationModal from "../../Components/Utilisateur/Utilisateurs.svelte"
    import UtilisateurRow from "../../Components/Utilisateur/UtilisateurRow.svelte"
    import LoadingSpinner from "../../Components/Common/LoadingSpinner.svelte"

    let loaded = $state(false)
    let selectedUser: User | null = $state(null)

    const handleUserClick = (user: User) => {
        openModal(user)
    }
    const openModal = (user: User) => {
        selectedUser = user
    }
    const closeModal = async () => {
        console.log("Closing modal...")
        selectedUser = null
        await getUsers()
    }

    let users: User[] = $state([])

    const getUsers = async () => {
        try {
            users = await GET<User[]>("/user/all")
            loaded = true
        } catch (error) {
            console.error("Error fetching users:", error)
        }
    }

    onMount(getUsers)
</script>

<main>
    {#if loaded}
        <section class="haut">
            <div class="haut-gauche">
                <h1 class="title">
                    <span class="text">LISTE DES</span>
                    <span class="text">UTILISATEURS</span>
                </h1>
            </div>
        </section>
        <section class="offres">
            <h2 class="textSections">Admins</h2>
            {#each users.filter((user) => user.isModerator) as user}
                <UtilisateurRow
                    {user}
                    handleModalClick={() => handleUserClick(user)}
                />
            {/each}
        </section>
        <section class="offres">
            <h2 class="textSections">Utilisateurs</h2>
            {#each users.filter((user) => !user.isModerator) as user}
                <UtilisateurRow
                    {user}
                    handleModalClick={() => handleUserClick(user)}
                />
            {/each}
        </section>

        {#if selectedUser}
            <UserConfigurationModal
                user={selectedUser}
                onCloseModal={closeModal}
            />
        {/if}
    {:else}
        <div class="loading">
            <LoadingSpinner />
        </div>
    {/if}
</main>

<style scoped>
    .title {
        left: 7.2%;
        margin: 0;
        margin-top: 30px;
    }
    .title span:first-child {
        color: white;
        margin: 0;
    }
    .title span:last-child {
        color: #00ad9a;
        margin: 0;
    }
    .text {
        font-size: 2.5vw;
        margin: 0;
    }
    main {
        display: flex;
        flex-direction: column;
        width: 100%;
    }
    .haut {
        display: flex;
        width: 85%;
        margin-bottom: 30px;
    }
    .haut-gauche {
        display: flex;
        flex-direction: column;
        width: 50%;
        margin-left: 5.2%;
    }
    .textSections {
        font-size: 1.8em;
        margin: 0;
        margin-top: 15px;
        margin-bottom: 5;
        color: white;
    }
    .offres {
        display: flex;
        flex-direction: column;
        width: 90%;
        margin-left: 5%;
    }

    @media (max-width: 768px) {
        .text {
            font-size: 6vw;
        }
        .title {
            width: 100vw;
        }
    }
</style>
