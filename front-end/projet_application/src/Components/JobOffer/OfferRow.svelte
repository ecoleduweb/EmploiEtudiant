<script lang="ts">
    import { onMount } from "svelte"
    import type { JobOffer } from "../../Models/Offre"
    export let isModerator: boolean
    export let offer: JobOffer
    export let handleEditModalClick: (id: number) => void
    export let handleApproveModalClick: (id: number) => void
    export let handleArchiveModalClick: (id: number) => void
</script>

<div class="offreEmploi">
    <div class="emploi">
        <div class="info">
            <p class="text">{offer.title}</p>
            <p class="text">{offer.offerDebut}</p>
            <p class="text">{ offer.description.length > 100 ? offer.description.substring(0, 100) + "..." : offer.description}</p>
        </div>
        <div class="info-mobile">
            <p class="text">{offer.title}</p>
        </div>
        {#if isModerator === true}
            <button
                class="button"
                on:click={() => handleApproveModalClick(offer.id)}
            >
                <img class="image" src="check.svg" alt="approve" />
            </button>
        {/if}
        <button class="button" on:click={() => handleEditModalClick(offer.id)}>
            <img class="image" src="edit.svg" alt="modifier" />
        </button>
        {#if offer.isApproved && ((new Date().toISOString().split("T")[0]) <= (new Date(offer.deadlineApply).toISOString().split("T")[0]))}
            <button class="button" on:click={() => handleArchiveModalClick(offer.id)}>
                <img class="image" src="archive.svg" alt="supprimer" />
            </button>
        {/if}
    </div>
</div>

<style scoped>
    .offreEmploi {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        width: 55%;
        border-width: 0px;
        border-bottom: 1px solid #00ad9a;
        background-color: transparent;
    }
    .info {
        display: flex;
        width: 90%;
        font-size: 1.15rem;
        flex-direction: row;
        justify-content: left;
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
    .info-mobile {
        display: none;
    }

    @media (max-width: 768px) {
         .info{
            display: none;
        }
        .info-mobile {
            display: flex;
            width: 100%;
            font-size: 1.15rem;
            flex-direction: row;
            justify-content: left;
        }
        .text {
            width: 100%;
        }
    }
    

</style>
