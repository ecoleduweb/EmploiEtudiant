<script lang="ts">
    import "../../styles/global.css"
    import DetailOfferRow from "../../Components/JobOffer/DetailOfferRow.svelte"
    import OfferDetail from "../../Components/JobOffer/OfferDetail.svelte"
    import { writable } from "svelte/store"
    import type { JobOffer } from "../../Models/Offre"
    import { GET } from "../../ts/server"
    import { onMount } from "svelte"
    import Modal from "../../Components/Common/Modal.svelte"
    import LoadingSpinner from "../../Components/Common/LoadingSpinner.svelte"

    const modal = writable(false)

    let loaded = 0

    const loadedOffer = () => 
    {
        loaded++
    }

    const selectedEmploiId = writable(0)
    const openModal = (id: number) => {
        modal.set(true)
        selectedEmploiId.set(id)
    }
    const closeModal = () => {
        modal.set(false)
    }
    const handleEmploiClick = (offreId: number) => {
        openModal(offreId)
    }

    const jobOffers = writable<JobOffer[]>([])
    const getJobOffers = async () => {
        try {
            const response = await GET<any>("/jobOffer/approved")
            jobOffers.set(response)
        } catch (error) {
            console.error("Error fetching job offers:", error)
        }
    }
    onMount(getJobOffers)
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

    
    <section class={loaded == ($jobOffers).length ? "CanBeHidden" : "Loading"}>
        <LoadingSpinner />
    </section>

    <section class={loaded == ($jobOffers).length ? "offres" : "CanBeHidden"}>
        {#each $jobOffers as offre}
            <DetailOfferRow {offre} handleModalClick={handleEmploiClick} OnLoaded={loadedOffer} />
       {/each}
    </section>

    <style scoped>
        .CanBeHidden 
        {
            display: none !important;
        }

        .Loading 
        {
            height: 100%;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            position: fixed;
        }
    </style>

    {#if $modal}
        {#each $jobOffers as emploi}
            {#if emploi.id === $selectedEmploiId}
                <Modal handleCloseClick={closeModal}>
                    <OfferDetail offer={emploi} />
                </Modal>
            {/if}
        {/each}
    {/if}
</main>

<style scoped>
    main {
        height: 100%;
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
