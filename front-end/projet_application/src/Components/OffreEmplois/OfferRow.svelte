<script lang="ts">
    import type { Emploi } from "../../Models/Emploi";
    export let emploi: Emploi;
</script>

<div class="offreEmploi">
    <div class="emploi">
        <div class="info">
            <p class="text">{emploi.titre}</p>
            <p class="text">{emploi.dateFin}</p>
            <p class="text">{emploi.description}</p>
        </div>
        <button class="button">
            <img class="image" src="edit.svg" alt="modifier" />
        </button>
        <button class="button">
            <img class="image" src="cancel.svg" alt="supprimer" />
        </button>
    </div>
</div>

<style scoped>
    .offreEmploi {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        width: 50%;
        border-width: 0px;
        border-bottom: 1px solid #00ad9a;
        background-color: transparent;
    }
    .info {
        display: flex;
        width: 90%;
        font-size: 1.3rem;
        flex-direction: row;
        justify-content: space-around;
    }
    .text {
        width: 20%;
    }
    .emploi {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        color: white;
        border-radius: 4px;
        width: 100%;
        height: 100%;
        padding: 5px 0px 5px 0px;
        transition: background-color 0.1s ease;
    }
    .emploi:hover {
        background-color: #485163;
    }
    .image {
        width: 30px;
        height: 30px;
    }
    .button {
        background-color: transparent;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
        border-radius: 4px;
    }
    .button:hover {
        background-color: #455b66;
    }
</style>
