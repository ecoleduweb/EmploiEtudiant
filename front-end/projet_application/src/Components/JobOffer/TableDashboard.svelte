<!-- TableDashboard.svelte -->
<script lang="ts">
    import type { JobOffer } from "../../Models/Offre"
    import OfferRow from "./OfferRow.svelte"

    interface Props {
        offers?: JobOffer[]
        isModerator?: boolean
        handleEditModalClick: (offer: JobOffer) => void
        handleApproveModalClick: (offer: JobOffer) => void
        handleArchiveModalClick: (offer: JobOffer) => void
        handleDeleteModalClick: (offer: JobOffer) => void
    }

    let {
        offers = [],
        isModerator = false,
        handleEditModalClick,
        handleApproveModalClick,
        handleArchiveModalClick,
        handleDeleteModalClick,
    }: Props = $props()
</script>

<div class="table-container">
    <table>
        <thead>
            <tr>
                <th class="column-Titre">Titre</th>
                <th class="column-Entreprise">Entreprise</th>
                <th class="column-Description">Description</th>
                <th class="column-Date">Date d'affichage</th>
                <th class="column-Actions">Actions</th>
            </tr>
        </thead>
        <tbody>
            {#each offers as offer}
                <OfferRow
                    {isModerator}
                    {offer}
                    {handleEditModalClick}
                    handleApproveModalClick={() =>
                        handleApproveModalClick(offer)}
                    handleArchiveModalClick={() =>
                        handleArchiveModalClick(offer)}
                    handleDeleteModalClick={() => {
                        handleDeleteModalClick(offer)
                    }}
                />
            {/each}
        </tbody>
    </table>
</div>

<style>
    .table-container {
        width: 100%;
        overflow-x: auto;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
    }

    thead {
        color: white;
    }

    th {
        padding: 12px 12px 12px 0;
        text-align: left;
        border-bottom: 1px solid #ddd;
        font-weight: bold;
        color: #00ad9a;
    }
    th.column-Titre {
        width: 20%;
    }
    th.column-Entreprise {
        width: 10%;
    }
    th.column-Date {
        width: 9%;
    }
    th.column-Actions {
        width: 11%;
    }
    @media (max-width: 768px) {
        th {
            font-size: 3vw;
        }
    }
</style>
