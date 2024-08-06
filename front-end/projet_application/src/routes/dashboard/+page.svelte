<script lang="ts">
    import "../../styles/global.css"
    import Button from "../../Components/Inputs/Button.svelte"
    import { writable } from "svelte/store"
    import type { JobOffer } from "../../Models/Offre"
    import type { Enterprise } from "../../Models/Enterprise"
    import OfferRow from "../../Components/JobOffer/OfferRow.svelte"
    import CreateEditJobOffer from "../../Components/JobOffer/CreateEditJobOffer.svelte"
    import ApprouveOffre from "../../Components/JobOffer/ApprouveOffre.svelte"
    import { GET } from "../../ts/server"
    import { onMount } from "svelte"
    import Modal from "../../Components/Common/Modal.svelte"
    import ArchiveConfirm from "../../Components/JobOffer/ArchiveConfirm.svelte"
    import { currentUser, isLoggedIn } from "$lib"
    import LoadingSpinner from "../../Components/Common/LoadingSpinner.svelte"

    let showApproveModal = false;
    let showCreateEditOffer = false;
    let showArchiveModal = false;
    let jobOfferSelected: JobOffer = {} as any
    let isJobOfferEdit = false
    let isModerator = false
    const handleCreateOffer = () => {
        showCreateEditOffer = true
        jobOfferSelected = undefined as any
    }

    const handleEditEmploiClick = (jobOffer: JobOffer) => {
        isJobOfferEdit = true
        jobOfferSelected = jobOffer;
        showCreateEditOffer = true
    }
    const handleApproveClick = (jobOffer: JobOffer) => {
        jobOfferSelected = jobOffer;
        showApproveModal = true;
    }
    const handleArchiveClick = (jobOffer: JobOffer) => 
    {
        jobOfferSelected = jobOffer;
        showArchiveModal = true;
    }
    
    const closeModalApprove = () => {
        showApproveModal = false 
    }
    const closeModalCreateEdit = () => 
    {
        showCreateEditOffer = false
        isJobOfferEdit = false
    }
    const closeModalArchive = () => 
    {
        showArchiveModal = false
    }

    const onFinishedCallBack = async () => 
    {
        await getJobOffersEmployeur()

        closeModalApprove()
        closeModalArchive()
        closeModalCreateEdit()
    }

    let enterprise: Enterprise = {
        id: 0,
        name: "",
        address: "",
        email: "",
        phone: "",
        cityId: 0,
        isTemporary: false,
    }
    
    let loaded = false
    
    onMount(async () => {
        try 
        {
            if ($isLoggedIn) {
                isModerator = ($currentUser as any).isModerator === true
                await getJobOffersEmployeur()
            }
        }
        catch (error) 
        {
            console.error("Error while loading:", error)
        }

        finally 
        {
            loaded = true
        }
    })

    const jobOffers = writable<JobOffer[]>([])



    const getJobOffersEmployeur = async () => {
        try {
            // Il est possible qu'il n'y ait pas d'offres encore quand c'est un nouvel employeur.
            const response = await GET<any>(
                "/jobOffer/employer/all",
            )
            if (response) 
            {
                jobOffers.set(response)
            }
        } catch (error) {
            console.error("Error fetching job offers:", error)
        }
    }
    let dateNow = new Date().toISOString().split("T")[0]

    $: toBeApprovedOffer = $jobOffers.filter((x) => x.isApproved === null)
    $: isRefusedOffer = $jobOffers.filter((x) => x.isApproved === false)
    $: offerToCome = $jobOffers.filter((x) => {
        if (!x.isApproved) return false
        let dateDebut = new Date(x.offerDebut).toISOString().split("T")[0]
        return dateNow < dateDebut
    })
    $: offerDisplayed = $jobOffers.filter((x) => {
        if (!x.isApproved) return false
        let dateDebut = new Date(x.offerDebut).toISOString().split("T")[0]
        let dateFin = new Date(x.deadlineApply).toISOString().split("T")[0]
        return dateNow >= dateDebut && dateNow <= dateFin
    })
    $: expiredOffer = $jobOffers.filter((x) => {
        if (!x.isApproved) return false
        let dateFin = new Date(x.deadlineApply).toISOString().split("T")[0]
        return dateFin < dateNow
    })
</script>

<main>
    <section class="haut">
        <div class="haut-gauche">
            <div class="divFlex">
                <Button
                    onClick={handleCreateOffer}
                    text="Créer une nouvelle offre"
                />
            </div>
        </div>
    </section>

    {#if !loaded}
        <section class="Loading">
            <LoadingSpinner />
        </section>
    {:else}
        <section class="offres">
            {#if isModerator === true}
                <p class="textOffre">Les offres d'emplois</p>
            {/if}
            {#if isModerator === false}
                <p class="textOffre">Mes offres d'emplois</p>
            {/if}
            {#if isRefusedOffer.length > 0}
                <h2 class="textSections">Offres refusées</h2>
                {#each isRefusedOffer as offer}
                    <OfferRow
                        {isModerator}
                        offer={offer}
                        handleEditModalClick={() => {handleEditEmploiClick(offer)}}
                        handleApproveModalClick={() => {handleApproveClick(offer)}}
                        handleArchiveModalClick={() => {handleArchiveClick(offer)}}
                    />
                {/each}
            {/if}
            {#if toBeApprovedOffer.length > 0}
                <h2 class="textSections">Offres en attente d'approbation</h2>
                {#each toBeApprovedOffer as offer}
                    <OfferRow
                        {isModerator}
                        {offer}
                        handleEditModalClick={() => {handleEditEmploiClick(offer)}}
                        handleApproveModalClick={() => {handleApproveClick(offer)}}
                        handleArchiveModalClick={() => {handleArchiveClick(offer)}}
                    />
                {/each}
            {/if}
            {#if offerToCome.length > 0}
                <h2 class="textSections">Offres bientôt affichées</h2>
                {#each offerToCome as offer}
                    <OfferRow
                        {isModerator}
                        {offer}
                        handleEditModalClick={() => {handleEditEmploiClick(offer)}}
                        handleApproveModalClick={() => {handleApproveClick(offer)}}
                        handleArchiveModalClick={() => {handleArchiveClick(offer)}}
                    />
                {/each}
            {/if}
            {#if offerDisplayed.length > 0}
                <h2 class="textSections">Offres affichées</h2>
                {#each offerDisplayed as offer}
                    <OfferRow
                        {isModerator}
                        {offer}
                        handleEditModalClick={() => {handleEditEmploiClick(offer)}}
                        handleApproveModalClick={() => {handleApproveClick(offer)}}
                        handleArchiveModalClick={() => {handleArchiveClick(offer)}}
                    />
                {/each}
            {/if}
            {#if expiredOffer.length > 0}
                <h2 class="textSections">Offres expirées</h2>
                {#each expiredOffer as offer}
                    <OfferRow
                        {isModerator}
                        {offer}
                        handleEditModalClick={() => {handleEditEmploiClick(offer)}}
                        handleApproveModalClick={() => {handleApproveClick(offer)}}
                        handleArchiveModalClick={() => {handleArchiveClick(offer)}}
                    />
                {/each}
            {/if}
        </section>
    {/if}

    <style scoped>
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


    {#if showApproveModal}    
    <Modal handleCloseClick={onFinishedCallBack}>
        <ApprouveOffre
            offer={jobOfferSelected}
            handleApproveClick={onFinishedCallBack}
        />
    </Modal>
    {/if}
    {#if showCreateEditOffer}    
    <Modal handleCloseClick={onFinishedCallBack}>
        <CreateEditJobOffer
            onFinished={onFinishedCallBack}
            isJobOfferEdit={isJobOfferEdit}
            jobOffer={jobOfferSelected}
            {enterprise}
        />
    </Modal>
    {/if}
    {#if showArchiveModal}
    <Modal handleCloseClick={onFinishedCallBack}>
        <ArchiveConfirm
            offer={jobOfferSelected}
            handleApproveClick={onFinishedCallBack}
        />
    </Modal>
    {/if}
</main>

<style scoped>
    main {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 2vh;
        min-height: 77vh;
    }
    .haut {
        width: 100%;
        margin-bottom: 2vh;
    }
    .haut-gauche {
        width: 30%;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .divFlex {
        display: flex;
        margin-bottom: 2vh;
    }
    .offres {
        width: 100%;
        display: flex;
        flex-direction: column;
    }
    .textOffre {
        font-size: 2.5em;
        margin: 0;
        margin-bottom: 2vh;
        color: white;
    }
    .textSections {
        font-size: 1.8em;
        margin: 0;
        margin-top: 5vh;
        color: white;
    }
</style>
