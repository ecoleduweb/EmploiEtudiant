<script lang="ts">
    import Modal from "../Common/Modal.svelte";
    import type { User } from "../../Models/User";
    import { GET } from "../../ts/server";
    import { onMount } from "svelte";
    export let user: User;
    export let handleUserClick: () => void;

</script>

<Modal handleModalClick={handleUserClick}>
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
