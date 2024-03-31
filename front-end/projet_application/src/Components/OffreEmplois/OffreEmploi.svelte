<script lang="ts">
    import Modal from "../Common/Modal.svelte";
    import type { Emploi } from "../../Models/Emploi";
    export let emploi: Emploi;
    export let handleEmploiClick: () => void;
</script>

<Modal handleModalClick={handleEmploiClick}>
    <div class="container">
        <div class="titleContainer">
            <h3 class="title">{emploi.title}</h3>
            <h4 class="subtitle">{emploi.scheduleId}</h4>
        </div>
        <div class="info">
            <h5 class="infoTitle">Type de poste</h5>
            <p class="text">{emploi.title}</p>
            <h5 class="infoTitle">Adresse du lieu de travail</h5>
            <p class="text">{emploi.address}</p>
            <h5 class="infoTitle">Description du poste</h5>
            <p class="text">{emploi.description}</p>
            <h5 class="infoTitle">Date de début</h5>
            <p class="text">{emploi.dateEntryOffice}</p>
            <h5 class="infoTitle">Date limite pour postuler</h5>
            <p class="text">{emploi.deadlineApply}</p>
            <h5 class="infoTitle">Où envoyer votre candidature</h5>
            <p class="text">{emploi.email}</p>
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
