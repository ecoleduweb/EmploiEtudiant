<script lang="ts">
    import "../../styles/global.css"
    import { onMount } from "svelte"
    import { writable } from "svelte/store"
    import { GET } from "../../ts/server"
    import type { User } from "../../Models/User"
    import UserComponent from "../../Components/Utilisateur/Utilisateurs.svelte"
    import UtilisateurRow from "../../Components/Utilisateur/UtilisateurRow.svelte"
    import LoadingSpinner from "../../Components/Common/LoadingSpinner.svelte"

    let loaded = false
    const modal = writable(false)
    const selectedUserId = writable(0)

    const handleUserClick = (id: number) => {
        openModal(id)
    }
    const openModal = (id: number) => {
        modal.set(true)
        selectedUserId.set(id)
    }
    const closeModal = async () => {
        modal.set(false)
        await getUsers()
    }

    let users: User[]

    const getUsers = async () => {
        try {
            const response = await GET<any>("/user/all")
            users = response.users
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
                    handleModalClick={() => handleUserClick(user.id)}
                />
            {/each}
        </section>
        <section class="offres">
            <h2 class="textSections">Utilisateurs</h2>
            {#each users.filter((user) => !user.isModerator) as user}
                <UtilisateurRow
                    {user}
                    handleModalClick={() => handleUserClick(user.id)}
                />
            {/each}
        </section>

        {#if $modal}
            {#each users as user}
                {#if user.id === $selectedUserId}
                    <UserComponent {user} handleUserClick={closeModal} />
                {/if}
            {/each}
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
