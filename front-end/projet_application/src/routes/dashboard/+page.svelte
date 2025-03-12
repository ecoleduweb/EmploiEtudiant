<script lang="ts">
    import "../../styles/global.css"
    import Button from "../../Components/Inputs/Button.svelte"
    import { writable } from "svelte/store"
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
    import type { JobOfferDetails } from "../../Models/JobOfferDetails"
    import ModifyEnterprise from "../../Components/Enterprise/ModifyEnterprise.svelte"
    import { checkIfUserHaveEnterprise } from "../../Service/EnterpriseService"
    import { bool } from "yup"

    let showApproveModal = false;
    let showCreateEditOffer = false;
    let showEditEnterprise = false;
    let showArchiveModal = false;
    let jobOfferSelected: JobOfferDetails = {} as any
    let isJobOfferEdit = false
    let isModerator = false
    let iconeUp = "▲"
    let iconeDown = "▼"
    let iconeRefused;
    let iconeToBeApproved;
    let iconeToCome;
    let iconeDisplayed;
    let iconeExpired;
    

    const handleCreateOffer = () => {
        showCreateEditOffer = true
        jobOfferSelected = undefined as any
    }
    
    const handleEditEnterprise = () => {
        showEditEnterprise = true
    }
        const handleEditEmploiClick = (jobOffer: JobOfferDetails) => {
        isJobOfferEdit = true
        jobOfferSelected = jobOffer;
        showCreateEditOffer = true
    }
    const handleApproveClick = (jobOffer: JobOfferDetails) => {
        jobOfferSelected = jobOffer;
        showApproveModal = true;
    }
    const handleArchiveClick = (jobOffer: JobOfferDetails) => 
    {
        jobOfferSelected = jobOffer;
        showArchiveModal = true;
    }
    const handleChangeListVisibility = (idList: string, idButton : string) => 
    {
        let list = document.getElementById(idList)
        let button = document.getElementById(idButton)
        console.log(iconeDown)
        console.log(iconeUp)
        list!.style.display === "none" ? list!.style.display = "block" : list!.style.display = "none"
        button!.innerHTML === iconeDown ? button!.innerHTML = iconeUp : button!.innerHTML = iconeDown

    }
    const closeEditEnterprise = () => {
        showEditEnterprise = false
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

    let userHaveEnterprise = false

    onMount(async () => {
        userHaveEnterprise = await checkIfUserHaveEnterprise($currentUser)

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

    const jobOffers = writable<JobOfferDetails[]>([])



    const getJobOffersEmployeur = async () => {
        try {
            // Il est possible qu'il n'y ait pas d'offres encore quand c'est un nouvel employeur.
            const response = await GET<JobOfferDetails[]>(
                "/jobOffer/employer/all?entrepriseDetails=true&employmentScheduleDetails=true&studyProgramDetails=true",
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

            {#if userHaveEnterprise}
                <div class="divFlex" id="editEnterprise">
                    <Button
                        onClick={handleEditEnterprise}
                        text="Modifier ton entreprise"
                    />
                </div>
            {/if}
        </div>
    </section>

    {#if !loaded}
        <section class="Loading">
            <LoadingSpinner />
        </section>
    {:else}
        <section class="offres">
            <h1 class="title">
                <span class="text">MES OFFRES D'EMPLOIS </span>
            </h1>
            {#if isRefusedOffer.length > 0}
                <div class="refusedOffers">
                    <div class="refusedOffersHeader">
                        <h2 class="textSections">Offres refusées</h2>  
                        <Button cssId="btnHideRefusedOfferList" text={iconeDown} onClick={() => handleChangeListVisibility("refusedOffersList", "btnHideRefusedOfferList")}></Button>
                    </div>
                    <div id="refusedOffersList">
                        {#each isRefusedOffer as offer}
                        <OfferRow
                            {isModerator}
                            offer={offer}
                            handleEditModalClick={() => {handleEditEmploiClick(offer)}}
                            handleApproveModalClick={() => {handleApproveClick(offer)}}
                            handleArchiveModalClick={() => {handleArchiveClick(offer)}}
                        />
                    
                        {/each}
                    </div>
                </div>
            {/if}
            {#if toBeApprovedOffer.length > 0}
                <div class="toBeApprovedOffers">
                    <div class="toBeApprovedOfferHeader">
                        <h2 class="textSections">Offres en attente d'approbation</h2>
                        <Button cssId="btnHidetoBeApprovedOfferList" text={iconeDown} onClick={() => handleChangeListVisibility("toBeApprovedOffersList", "btnHidetoBeApprovedOfferList")}></Button>
                    </div>
                    <div id="toBeApprovedOffersList">
                        {#each toBeApprovedOffer as offer}
                            <OfferRow
                                {isModerator}
                                {offer}
                                handleEditModalClick={() => {handleEditEmploiClick(offer)}}
                                handleApproveModalClick={() => {handleApproveClick(offer)}}
                                handleArchiveModalClick={() => {handleArchiveClick(offer)}}
                            />
                        {/each}
                    </div>
                </div>
            {/if}
            {#if offerToCome.length > 0}
                <div class="offerToCome">
                    <div class="offerToComeHeader">
                        <h2 class="textSections">Offres bientôt affichées</h2>
                        <Button cssId="btnHideOfferToCome" text={iconeDown} onClick={() => handleChangeListVisibility("offersToComeList", "btnHideOfferToCome")}></Button>
                    </div>
                    <div id="offersToComeList">                
                        {#each offerToCome as offer}
                            <OfferRow
                                {isModerator}
                                {offer}
                                handleEditModalClick={() => {handleEditEmploiClick(offer)}}
                                handleApproveModalClick={() => {handleApproveClick(offer)}}
                                handleArchiveModalClick={() => {handleArchiveClick(offer)}}
                            />
                        {/each}
                    </div>
                </div>
            {/if}

            {#if offerDisplayed.length > 0}
                <div class="offerDisplayed">
                    <div class="offerDisplayedHeader">
                        <h2 class="textSections">Offres affichées</h2>
                        <Button cssId="btnHideOfferDisplayed" text={iconeDown} onClick={() => handleChangeListVisibility("offerDisplayedList", "btnHideOfferDisplayed")}></Button>
                    </div>
                    <div id="offerDisplayedList">
                        {#each offerDisplayed as offer}
                            <OfferRow
                                {isModerator}
                                {offer}
                                handleEditModalClick={() => {handleEditEmploiClick(offer)}}
                                handleApproveModalClick={() => {handleApproveClick(offer)}}
                                handleArchiveModalClick={() => {handleArchiveClick(offer)}}
                            /> 
                        {/each}
                    </div>
                </div>
            {/if}
            {#if expiredOffer.length > 0}
                <div class="expiredOffer">
                    <div class="expiredOfferHeader">
                        <h2 class="textSections">Offres expirées</h2>
                        <Button cssId="btnHideExpiredOffer" text={iconeDown} onClick={() => handleChangeListVisibility("expiredOfferList", "btnHideExpiredOffer")}></Button>
                    </div>
                        <div id="expiredOfferList">
                        {#each expiredOffer as offer}
                            <OfferRow
                                {isModerator}
                                {offer}
                                handleEditModalClick={() => {handleEditEmploiClick(offer)}}
                                handleApproveModalClick={() => {handleApproveClick(offer)}}
                                handleArchiveModalClick={() => {handleArchiveClick(offer)}}
                            />
                        {/each}
                    </div>
                </div>
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
    {#if showEditEnterprise}
        <ModifyEnterprise handleCloseClick={closeEditEnterprise}></ModifyEnterprise>
    {/if}
    {#if showCreateEditOffer}    
    <Modal handleCloseClick={closeModalCreateEdit}>
        <CreateEditJobOffer
            onFinished={onFinishedCallBack}
            isJobOfferEdit={isJobOfferEdit}
            jobOffer={jobOfferSelected}
            {enterprise}
        />
    </Modal>
    {/if}
    {#if showArchiveModal}
    <Modal handleCloseClick={closeModalArchive}>
        <ArchiveConfirm
            offer={jobOfferSelected}
            handleApproveClick={closeModalArchive}
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
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: left;
        gap: 2vw;
        margin-left: 5vw;
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

    .textSections {
        font-size: 1.8em;
        margin: 0;
        margin-top: 5vh;
        color: white;
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
    .refusedOffersHeader, .toBeApprovedOfferHeader, .offerToComeHeader, .offerDisplayedHeader, .expiredOfferHeader {
        display: flex;
        justify-content: space-between;
        width: 33%;
    }

    #refusedOffersList, #toBeApprovedOffersList, #offerToComeList, #offerDisplayedList, #expiredOfferList {
        display: block;
    }
    #refusedOffersHeader, #toBeApprovedOffersList, #offerToComeList, #offerDisplayedList, #expiredOfferList {
        display: flex;
        justify-content: space-between;
    }

    @media (max-width: 768px) {
        .text {
            font-size: 6vw;
        }
    }
</style>
