<script lang="ts">
    import Modal from "../Common/Modal.svelte";
    import type { jobOffer } from "../../Models/Offre";
    export let offre: jobOffer;
    export let handleEmploiClick: () => void;
    export let currentPage = window.location.pathname;
</script>

<Modal handleModalClick={handleEmploiClick}>
    <div class="container">
        <div class="titleContainer">
            <h3 class="title">{offre.title}</h3>
            <h4 class="subtitle">{offre.scheduleId}</h4>
        </div>
        {#if currentPage === "/offres"}
            <div class="info">
                <h5 class="infoTitle">Type de poste</h5>
                <p class="text">{offre.title}</p>
                <h5 class="infoTitle">Adresse du lieu de travail</h5>
                <p class="text">{offre.address}</p>
                <h5 class="infoTitle">Description du poste</h5>
                <p class="text">{offre.description}</p>
                <h5 class="infoTitle">Date de début</h5>
                <p class="text">{offre.offerDebut}</p>
                <h5 class="infoTitle">Date limite pour postuler</h5>
                <p class="text">{offre.deadlineApply}</p>
                <h5 class="infoTitle">Où envoyer votre candidature</h5>
                <p class="text">{offre.email}</p>
            </div>
        {/if}
        {#if currentPage === "/dashboard"}
            <div class="info">
                <h5 class="infoTitle">Type de poste</h5>
                <input class="text" type="text" value={offre.title} />
                <h5 class="infoTitle">Adresse du lieu de travail</h5>
                <input class="text" type="text" value={offre.address} />
                <h5 class="infoTitle">Description du poste</h5>
                <input class="text" type="text" value={offre.description} />
                <h5 class="infoTitle">Date de début</h5>
                <input class="text" type="date" value={offre.offerDebut} />
                <h5 class="infoTitle">Date limite pour postuler</h5>
                <input class="text" type="date" value={offre.deadlineApply} />
                <h5 class="infoTitle">Où envoyer votre candidature</h5>
                <input class="text" type="email" value={offre.email} />
            </div>
        {/if}
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
    .subtitle {
        font-size: 1.5rem;
        margin: 0px;
        margin-bottom: 2.25vw;
        color: black;
    }
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
