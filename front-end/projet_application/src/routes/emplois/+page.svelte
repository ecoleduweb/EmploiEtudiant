<script lang="ts">
    import "../../styles/global.css"
    import DetailOfferRow from "../../Components/JobOffer/DetailOfferRow.svelte"
    import OfferDetail from "../../Components/JobOffer/OfferDetail.svelte"
    import { writable } from "svelte/store"
    import { GET } from "../../ts/server"
    import { onMount } from "svelte"
    import Modal from "../../Components/Common/Modal.svelte"
    import LoadingSpinner from "../../Components/Common/LoadingSpinner.svelte"
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
</script>

<main>
    <section class="haut">
        <div class="haut-gauche">
            <h1 class="title">
                <span class="text">EMPLOIS </span><span class="text">
                    DISPONIBLES</span
                >
            </h1>
        </div>
    </section>

    
    <section>
        {#if loaded}
            <div class="rowTitles">
                <h2 class="rowTitle">Titre</h2>
                <h2 class="rowTitle">Horaire</h2>
                <h2 class="rowTitle">Date d'entrée en vigueur</h2>
                <h2 class="rowTitle">Programmes visés</h2>
                <h2 class="rowTitle">Employeur</h2>
                <h2 class="rowTitle">Détails</h2>
            </div>
            {#each $jobOffers as offer}
                <DetailOfferRow {offer} handleModalClick={handleAddJobOfferClick} />
            {/each}
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
        height: 100%;
    }

    .rowTitles {
        display: flex;
        margin-left: 5%;
        justify-content: left;
    }

    .rowTitle {
        color: #00ad9a;
        text-align: center;
        width: 20%;
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
    main {
        display: flex;
        flex-direction: column;
        width: 100%;
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
        margin-left: 5.2%;
    }
    .offres {
        width: fit-content;
        display: flex;
        flex-direction: column;
        width: 100%;
    }
    .offres {
        width: fit-content;
        display: flex;
        flex-direction: column;
        width: 100%;
    }

    @media screen and (max-width: 900px) and (min-width: 300px) 
    {
        .text 
        {
            font-size: 3.3vw;
        }
    }
</style>
