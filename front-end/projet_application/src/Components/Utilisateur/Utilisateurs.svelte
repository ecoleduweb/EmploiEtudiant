<script lang="ts">
    import Modal from "../Common/Modal.svelte"
    import type { User } from "../../Models/User"
    import Button from "../Inputs/Button.svelte"
    import { PUT } from "../../ts/server"
    import { onMount } from "svelte"
    export let user: User
    export let handleUserClick: () => void

    let password: string

    const ChangerMotDePasse = () => {
        PUT<any, any>("/user/updatePassword", {
            email: user.email,
            password: password
        })
    }
</script>

<Modal handleCloseClick={handleUserClick}>
    <div class="container">
        <div class="titleContainer">
            <h3 class="title">{user.email}</h3>
        </div>
        <div class="info">
            <h5 class="infoTitle">Email</h5>
            <p class="text">{user.email}</p>
            <h5 class="infoTitle">Prenom</h5>
            <p class="text">{user.firstName}</p>
            <h5 class="infoTitle">Nom</h5>
            <p class="text">{user.lastName}</p>
            <h5 class="infoTitle">Autre informations:</h5>
        </div>

        <div class="motDePasse">
            <h5 class="infoTitle mdpContent">Mot de passe:</h5>
            <input type="text"
                bind:value={password}
                placeholder="Nouveau mot de passe"
                class="input"
            />

            <div class="button mdpContent">
                <Button text="Changer" onClick={() => ChangerMotDePasse()}/>
            </div>
        </div>
    </div>
</Modal>

<style scoped>
    .titleContainer {
        display: flex;
        flex-direction: column;
    }
    .title {
        font-size: 2.5rem;
        color: #00ad9a;
        margin: 0px;
        margin-bottom: 1.5vw;
    }
    /* .subtitle {
        font-size: 1.5rem;
        margin: 0px;
        margin-bottom: 2.25vw;
        color: black;
    } */
    .infoTitle {
        font-size: 1.3rem;
        margin: 0px;
        margin-bottom: 0.5vw;
    }
    .info {
        color: black;
    }
    .motDePasse {
        display: flex;
        justify-content: space-evenly;
        color: black;
    }
    .mdpContent {
    }
    .text {
        font-size: 1.1rem;
        margin: 0px;
        margin-bottom: 1.75vw;
        color: black;
    }
    .container {
        width: 95%;
        display: flex;
        flex-direction: column;
        text-align: left;
        justify-content: space-between;
        color: white;
        border-radius: 4px;
        transition: background-color 0.3s ease;
    }
</style>
