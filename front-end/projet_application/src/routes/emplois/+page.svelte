<script lang="ts">
    import "../../styles/global.css"
    import DetailOfferRow from "../../Components/JobOffer/DetailOfferRow.svelte"
    import OfferDetail from "../../Components/JobOffer/OfferDetail.svelte"
    import { writable } from "svelte/store"
    import { GET } from "../../ts/server"
    import { onMount } from "svelte"
    import Modal from "../../Components/Common/Modal.svelte"
    import LoadingSpinner from "../../Components/Common/LoadingSpinner.svelte"
    import Table from "../../Components/Common/Table.svelte"
    import { pushState } from "$app/navigation"
    import { page } from '$app/stores'
    import type { JobOfferDetails } from "../../Models/JobOfferDetails"

    let showModal = false
    let loaded = false
    let selectedOffer: JobOfferDetails = undefined as any

    const handleAddJobOfferClick = (offer: JobOfferDetails) => {
        showModal = true
        selectedOffer = offer

        pushState("?id=" + offer.id, {})
    }
    
    const closeModal = () => {
        showModal = false
        pushState("/emplois", {})
    }

    const jobOffers = writable<JobOfferDetails[]>([])
    onMount(async () => {
        try {
            const response = await GET<JobOfferDetails[]>("/jobOffer/approved?entrepriseDetails=true&employmentScheduleDetails=true&studyProgramDetails=true")
            jobOffers.set(response)
        } catch (error) {
            console.error("Error fetching job offers:", error)
        }
        finally
        {
            loaded = true

            const id = $page.url.searchParams.get('id')

            if (id !== '') 
            {
                let jobOffer = $jobOffers.find((offer) => offer.id.toString() == id)
                
                if (jobOffer) 
                {
                    showModal = true
                    selectedOffer = jobOffer
                }
            }
        }
    })

        // Définition des colonnes pour le tableau des offres d'emploi
        const columns = [
        { key: 'posteVise', label: 'Poste visé' },
        { key: 'typeEmploi', label: "Type d'emploi", class: "rowTitles" },
        { key: 'dateLimite', label: 'Date limite pour postuler', class: "rowTitles" },
        { key: 'programmesVises', label: 'Programmes visés', class: "rowTitles" },
        { key: 'employeur', label: 'Employeur' },
        { 
        key: 'details', 
        label: 'Détails',
        formatter: (offer) => `<img class="image" src="add.svg" alt="ajouter" onclick="handleModalClick(${JSON.stringify(offer)})" />`
    }
    ];
</script>

<main>
    <section class="haut">
        <div class="haut-gauche">
            <h1 class="title">
                <span class="text">OFFRES D'EMPLOI </span><span class="text">
                    DISPONIBLES</span
                >
            </h1>
        </div>
    </section>

    
    <section>
        {#if loaded}
        <div class="emplois-table">
            <Table
                    columns={columns}
                    data={$jobOffers}
                    handleModalClick={handleAddJobOfferClick}
                    rowComponent={DetailOfferRow}
            />
        </div>
        <!--
            <table>
                <thead>
                    <tr>
                        <th>Poste visé</th>
                        <th class="rowTitles">Type d'emploi</th>
                        <th class="rowTitles">Date limite pour postuler</th>
                        <th class="rowTitles">Programmes visés</th>
                        <th>Employeur</th>
                        <th>Détails</th>
                    </tr>
                </thead>
                <tbody>
                {#each $jobOffers as offer}
                    <DetailOfferRow {offer} handleModalClick={handleAddJobOfferClick} />
                {/each}
                </tbody>
            </table>
        -->
        {:else}
            <div class="loading">
                <LoadingSpinner />
            </div>
        {/if}
    </section>

    <style scoped>
        .loading 
        {
            height: 100%;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            position: fixed;
        }
    </style>

    {#if showModal}
        <Modal handleCloseClick={closeModal}>
            <OfferDetail offer={selectedOffer} />
        </Modal>
    {/if}
</main>

<style scoped>
    main {
        flex: 1;
        display: flex;
        flex-direction: column;
        margin: 12px;
    }

    .title {
        left: 7.2%;
        margin: 0;
        margin-top: 30px;
    }
    .title span:first-child {
        color: white;
        margin: 0;
    }
    .title span:last-child {
        color: #00ad9a;
        margin: 0;
    }
    .text {
        font-size: 2.5vw;
        margin: 0;
    }

    .haut {
        display: flex;
        width: 85%;
        margin-bottom: 30px;
    }
    .haut-gauche {
        display: flex;
        flex-direction: column;
        width: 50%;
    }

    /* Section des tableaux*/
    table {
        width: 100%; /* Prend toute la largeur disponible */
        border-collapse: collapse; /* Fusionne les bordures pour un bon alignement */
        table-layout: fixed; /* Force une répartition égale des colonnes */
    }

    thead {
        color: white;
    }

    th {
        padding: 12px 12px 12px 0;
        text-align: left;
        border-bottom: 1px solid #ddd;
        font-weight: bold;
        text-align: left;
        color: #00ad9a;
    }

    @media (max-width: 768px)
    {
        .text{
            font-size: 6vw;
            width: 100%;
        }
        .title
        {
            width: 100vw;
        }
    }
</style>
