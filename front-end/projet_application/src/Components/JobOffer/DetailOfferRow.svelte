<script lang="ts">
    import type { JobOfferDetails } from "../../Models/JobOfferDetails"

    interface Props {
        offer: JobOfferDetails
        handleModalClick: (offer: JobOfferDetails) => void
    }

    let { offer, handleModalClick }: Props = $props()
</script>

<tr class="offreEmploi" onclick={() => handleModalClick(offer)}>
    <td>{offer.title}</td>
    <td class="desktop-only"
        >{offer.employementSchedules?.map((x) => x.description).join(", ")}</td
    >
    <td class="desktop-only">{offer.deadlineApply}</td>
    <td class="desktop-only"
        >{offer.studyPrograms?.map((x) => x.name).join(", ")}</td
    >
    <td>{offer.enterprise?.name}</td>
    <td><img class="image" src="add.svg" alt="ajouter" /></td>
</tr>
employementSchedules

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
        display: table-row;
    }

    .image {
        width: 30px;
        height: 30px;
    }

    tr:hover {
        background-color: #555b66;
        cursor: pointer;
    }

    @media (max-width: 768px) {
        .desktop-only {
            display: none;
        }
        .image {
            width: 30px;
            height: 30px;
        }
    }
</style>
