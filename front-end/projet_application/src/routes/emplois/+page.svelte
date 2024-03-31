<script lang="ts">
    import "../../styles/global.css";
    import Header from "../../Components/Common/Header.svelte";
    import Footer from "../../Components/Common/Footer.svelte";
    import EmploiRow from "../../Components/OffreEmplois/EmploiRow.svelte";
    import OffreEmploi from "../../Components/OffreEmplois/OffreEmploi.svelte";
    import { writable } from "svelte/store";
    import type { Emploi } from "../../Models/Emploi";
    import { GET } from "../../ts/server";
    import { onMount } from "svelte";

    const modal = writable(false);
    const selectedEmploiId = writable(0);
    const openModal = (id: number) => {
        modal.set(true);
        selectedEmploiId.set(id);
    };
    const closeModal = () => {
        modal.set(false);
    };
    const handleEmploiClick = (offreId: number) => {
        openModal(offreId);
    };

    const jobOffers = writable<Emploi[]>([]);
    const getJobOffers = async () => {
        try {
            const response = await GET<any>("/jobOffer/offresEmploi");
            console.log("response", response);
            jobOffers.set(response);
        } catch (error) {
            console.error("Error fetching job offers:", error);
        }
    };
    onMount(getJobOffers);
</script>

<Header />
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
            <EmploiRow emploi={offre} handleModalClick={handleEmploiClick}
            ></EmploiRow>
        {/each}
    </section>
    {#if $modal}
        {#each $jobOffers as emploi}
            {#if emploi.id === $selectedEmploiId}
                <OffreEmploi {emploi} handleEmploiClick={closeModal} />
            {/if}
        {/each}
    {/if}
</main>
<Footer />

<style scoped>
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
        widows: 85%;
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
