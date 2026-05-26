<script lang="ts">
    import { onMount } from "svelte"
    import type { JobOfferDetails } from "../../Models/JobOfferDetails"
    import type { Enterprise } from "../../Models/Enterprise"
    import { removeHtmlTags, toFormattedDateString } from "../../ts/utils"

    interface Props {
        isModerator: boolean
        offer: JobOfferDetails
        enterprise?: Enterprise | null
        handleEditModalClick: (id: number) => void
        handleApproveModalClick: (id: number) => void
        handleArchiveModalClick: (id: number) => void
        handleDeleteModalClick: (id: number) => void
    }

    let {
        isModerator,
        offer,
        enterprise = null,
        handleEditModalClick,
        handleApproveModalClick,
        handleArchiveModalClick,
        handleDeleteModalClick,
    }: Props = $props()

    let enterpriseName = $state("Entreprise inconnue")

    onMount(() => {
        if (offer.enterprise) {
            enterpriseName = offer.enterprise.name
        } else if (enterprise) {
            enterpriseName = enterprise.name
        }
    })
</script>

<tr class="offreEmploi">
    <td>{offer.title}</td>
    <td>{enterpriseName}</td>
    <td
        >{@html removeHtmlTags(offer.description).length > 100
            ? removeHtmlTags(offer.description).substring(0, 100) + "..."
            : removeHtmlTags(offer.description)}</td
    >
    <td>{toFormattedDateString(offer.offerDebut)}</td>
    <td>
        {#if isModerator}
            <button
                class="button"
                onclick={() => handleApproveModalClick(offer.id)}
            >
                <img class="image" src="check.svg" alt="approve" />
            </button>
        {/if}
        <button class="button" onclick={() => handleDeleteModalClick(offer.id)}>
            <img class="image" src="delete.svg" alt="supprimer" />
        </button>

        <button
            class="button edit"
            onclick={() => handleEditModalClick(offer.id)}
        >
            <img class="image" src="edit.svg" alt="modifier" />
        </button>
        {#if offer.isApproved && new Date()
                .toISOString()
                .split("T")[0] <= new Date(offer.deadlineApply)
                    .toISOString()
                    .split("T")[0]}
            <button
                class="button"
                onclick={() => handleArchiveModalClick(offer.id)}
            >
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
        cursor: pointer;
        transition: background-color 0.3s ease;
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
    td {
        color: white;
    }

    tr:hover {
        background-color: #555b66;
    }
</style>
