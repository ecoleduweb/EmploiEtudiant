<script lang="ts">
    import { onMount } from "svelte";
    import type { JobOfferDetails } from "../../Models/JobOfferDetails";
    import type { JobOffer } from "../../Models/Offre";
    import type { Enterprise } from "../../Models/Enterprise";
    export let isModerator: boolean;
    export let offer:  JobOfferDetails;
    export let enterprise: Enterprise | null = null; 

    
    export let handleEditModalClick: (id: number) => void;
    export let handleApproveModalClick: (id: number) => void;
    export let handleArchiveModalClick: (id: number) => void;
    export let handleDeleteModalClick: (id: number) => void

    let enterpriseName = "Entreprise inconnue";

    onMount(() => {
        if (offer.enterprise) {
            enterpriseName = offer.enterprise.name;
        } else if (enterprise) {
            enterpriseName = enterprise.name;
        }
    });
</script>


<tr class="offreEmploi">
    <td>{offer.title}</td>
    <td>{enterpriseName}</td>
    <td>{@html offer.description.length > 100 ? offer.description.substring(0, 100) + "..." : offer.description}</td>
    <td>{offer.offerDebut}</td>
    <td>
        {#if isModerator}
            <button class="button" on:click={() => handleApproveModalClick(offer.id)}>
                <img class="image" src="check.svg" alt="approve" />
            </button>
            <button class="button" on:click={()=> handleDeleteModalClick(offer.id)}>
                <img class="image" src="delete.svg" alt="supprimer" />
            </button>
        {/if}
        <button class="button edit" on:click={() => handleEditModalClick(offer.id)}>
            <img class="image" src="edit.svg" alt="modifier" />
        </button>
        {#if offer.isApproved && ((new Date().toISOString().split("T")[0]) <= (new Date(offer.deadlineApply).toISOString().split("T")[0]))}
            <button class="button" on:click={() => handleArchiveModalClick(offer.id)}>
                <img class="image" src="archive.svg" alt="supprimer" />
            </button>
        {/if}
    </td>
</tr>

<style scoped>
    .offreEmploi {
        align-items: center;
        color: white;
        width: 100%;
        border-width: 0px;
        border-bottom: 1px solid #00ad9a;
        background-color: transparent;
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
    tr:hover {
        background-color: #555b66;
    }
</style>
