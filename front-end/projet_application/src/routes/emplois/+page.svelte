<script lang="ts">
    import "../../styles/global.css"
    import EmploiRow from "../../Components/JobOffer/EmploiRow.svelte"
    import OffreEmploi from "../../Components/JobOffer/OffreEmploi.svelte"
    import { writable } from "svelte/store"
    import type { JobOffer } from "../../Models/Offre"
    import { GET } from "../../ts/server"
    import { onMount } from "svelte"
    import Modal from "../../Components/Common/Modal.svelte"

    const modal = writable(false)
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
    <section class="offres">
        {#each $jobOffers as offre}
            <EmploiRow {offre} handleModalClick={handleEmploiClick} />
        {/each}
    </section>
    {#if $modal}
        {#each $jobOffers as emploi}
            {#if emploi.id === $selectedEmploiId}
                <Modal handleCloseClick={closeModal}>
                    <OffreEmploi offer={emploi} />
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
</style>
