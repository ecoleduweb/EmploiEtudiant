<script lang="ts">
    import "../../styles/global.css"
    import Button from "../../Components/Inputs/Button.svelte"
    import { writable } from "svelte/store"
    import type { Enterprise } from "../../Models/Enterprise"
    import OfferRow from "../../Components/JobOffer/OfferRow.svelte"
    import CreateEditJobOffer from "../../Components/JobOffer/CreateEditJobOffer.svelte"
    import ApprouveOffre from "../../Components/JobOffer/ApprouveOffre.svelte"
    import { GET } from "../../ts/server"
    import { onMount} from "svelte"
    import Modal from "../../Components/Common/Modal.svelte"
    import ArchiveConfirm from "../../Components/JobOffer/ArchiveConfirm.svelte"
    import { currentUser, isLoggedIn } from "$lib"
    import LoadingSpinner from "../../Components/Common/LoadingSpinner.svelte"
    import type { JobOfferDetails } from "../../Models/JobOfferDetails"
    import ModifyEnterprise from "../../Components/Enterprise/ModifyEnterprise.svelte"
    import { checkIfUserHaveEnterprise } from "../../Service/EnterpriseService"
    import {hiddenListsService} from "../../Service/CollapsedOfferLists"
    import DeleteOffer from "../../Components/JobOffer/DeleteOffer.svelte"

    let showApproveModal = false;
    let showCreateEditOffer = false;
    let showEditEnterprise = false;
    let showArchiveModal = false;
    let jobOfferSelected: JobOfferDetails = {} as any
    let isJobOfferEdit = false
    let isModerator = false
    
    let iconeUp = "▲"
    let iconeDown = "▼"
    



    const { 
        isRefusedHidden, 
        isToBeApprovedHidden,
        isToComeHidden,
        isDisplayedHidden,
        isExpiredHidden
    } = hiddenListsService;
    let showDeleteModal = false

    const handleCreateOffer = () => {
        showCreateEditOffer = true
        jobOfferSelected = undefined as any
    }

    const handleDeleteClick = (jobOffer: JobOfferDetails) => {
        jobOfferSelected = jobOffer
        showDeleteModal = true
    }

    const deleteOfferAndCloseModal = (idJobOffer: number | null) => {
       //jobOfferSelected = jobOffer;
       showDeleteModal = false

       if (idJobOffer !== null) {
            jobOffers.update((jobOffers) => jobOffers.filter((x) => x.id !== idJobOffer))
        }
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

    const closeModalDelete = () => 
    {
        showDeleteModal = false
    }

    const onFinishedCallBack = async () => 
    {
        await getJobOffersEmployer()

        closeModalApprove()
        closeModalArchive()
        closeModalCreateEdit()
        closeModalDelete()
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
                await getJobOffersEmployer();    
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

    const getJobOffersEmployer = async () => {
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
                <span class="text">MES OFFRES D&apos;EMPLOIS </span>
            </h1>
            {#if isRefusedOffer.length > 0}
                <div class="refusedOffers">
                    <div class="offersHeader ">
                        <h2 class="textSections">Offres refusées</h2>  
                        <Button cssId="btnHideRefusedOfferList" text={$isRefusedHidden ? iconeUp : iconeDown} onClick={() => {hiddenListsService.isRefusedHidden.update(value => !value);}}></Button>
                    </div>
                    <div id="refusedOffersList" style="display: {$isRefusedHidden ? 'none' : 'block'}">
                        <table>
                    <thead>
                        <tr>
                            <th>Titre</th>
                            <th>Entreprise</th>
                            <th>Description</th>
                            <th>Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {#each isRefusedOffer as offer}
                                <OfferRow
                                    {isModerator}
                                    offer={offer}
                                    handleEditModalClick={() => {handleEditEmploiClick(offer)}}
                                    handleApproveModalClick={() => {handleApproveClick(offer)}}
                                    handleArchiveModalClick={() => {handleArchiveClick(offer)}}
                                    handleDeleteModalClick={() => {handleDeleteClick(offer)}}
                            />
                    
                                {/each}
                    </div>
                </div>
                    </tbody>
                </table>
            {/if}
            {#if toBeApprovedOffer.length > 0}
                <div class="toBeApprovedOffers">
                    <div class="offersHeader">
                    <h2 class="textSections">Offres en attente d'approbation</h2>
                        <Button cssId="btnHidetoBeApprovedOfferList" text={$isToBeApprovedHidden? iconeUp : iconeDown} onClick={() =>{hiddenListsService.isToBeApprovedHidden.update(value => !value);}}></Button>
                    </div>
                    <div id="toBeApprovedOffersList" style="display: {$isToBeApprovedHidden ? 'none' : 'block'}">
                    <!-- Tableau pour afficher les offres en attente d'approbation -->
            <table>
                <thead>
                    <tr>
                        <th>Titre</th>
                        <th>Entreprise</th>
                        <th>Description</th>
                        <th>Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {#each toBeApprovedOffer as offer}
                            <OfferRow
                            {isModerator}
                            {offer}
                            handleEditModalClick={() => {handleEditEmploiClick(offer)}}
                            handleApproveModalClick={() => {handleApproveClick(offer)}}
                            handleArchiveModalClick={() => {handleArchiveClick(offer)}}
                            handleDeleteModalClick={() => {handleDeleteClick(offer)}}
                    />
                            {/each}
                </tbody>
            </table>
                    </div>
                </div>
            {/if}
            {#if offerToCome.length > 0}
                <div class="offerToCome">
                    <div class="offersHeader">
                        <h2 class="textSections">Offres bientôt affichées</h2>
                        <Button cssId="btnHideOfferToCome" text={$isToComeHidden? iconeUp : iconeDown} onClick={() => {hiddenListsService.isToComeHidden.update(value => !value);}}></Button>
                    </div>
                    <div id="offersToComeList" style="display: {$isToComeHidden ? 'none' : 'block'}">                
                        <table>
                    <thead>
                        <tr>
                            <th>Titre</th>
                            <th>Entreprise</th>
                            <th>Description</th>
                            <th>Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                    {#each offerToCome as offer}
                                <OfferRow
                                    {isModerator}
                                    {offer}
                                    handleEditModalClick={() => {handleEditEmploiClick(offer)}}
                                    handleApproveModalClick={() => {handleApproveClick(offer)}}
                                    handleArchiveModalClick={() => {handleArchiveClick(offer)}}
                                    handleDeleteModalClick={() => {handleDeleteClick(offer)}}
                                />
                            {/each}
                    </div>
                </div>
                    </tbody>
                </table>
            {/if}

            {#if offerDisplayed.length > 0}
            <div class="offerDisplayed">
                <div class="offersHeader">
                    <h2 class="textSections">Offres affichées</h2>
                    <Button cssId="btnHideOfferDisplayed" text={$isDisplayedHidden? iconeUp : iconeDown} onClick={() => {hiddenListsService.isDisplayedHidden.update(value => !value);}}></Button>
                </div>
                <div id="offerDisplayedList" style="display: {$isDisplayedHidden ? 'none' : 'block'}">
                    <table>
                    <thead>
                        <tr>
                            <th>Titre</th>
                            <th>Entreprise</th>
                            <th>Description</th>
                            <th>Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                    {#each offerDisplayed as offer}
                            <OfferRow
                                {isModerator}
                                {offer}
                                handleEditModalClick={() => {handleEditEmploiClick(offer)}}
                                handleApproveModalClick={() => {handleApproveClick(offer)}}
                                handleArchiveModalClick={() => {handleArchiveClick(offer)}}
                                handleDeleteModalClick={() => {handleDeleteClick(offer)}}
                            /> 
                        {/each}
                </div>
            </div>
                    </tbody>
                </table>
            {/if}
            {#if expiredOffer.length > 0}
                <div class="expiredOffer">
                    <div class="offersHeader">
                        <h2 class="textSections">Offres expirées</h2>
                            <Button cssId="btnHideExpiredOffer" text={$isExpiredHidden ? iconeUp : iconeDown} onClick={() => { hiddenListsService.isExpiredHidden.update(value => !value);}} ></Button>
                    </div>
                        <div id="expiredOfferList" style="display: {$isExpiredHidden ? 'none' : 'block'}">
                        {#each expiredOffer as offer}
                            <OfferRow
                                {isModerator}
                                {offer}
                                handleEditModalClick={() => {handleEditEmploiClick(offer)}}
                                handleApproveModalClick={() => {handleApproveClick(offer)}}
                                handleArchiveModalClick={() => {handleArchiveClick(offer)}}
                                handleDeleteModalClick={() => {handleDeleteClick(offer)}}
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
    {#if showDeleteModal}
    <Modal handleCloseClick={() => closeModalDelete()}>
        <DeleteOffer
            offer={jobOfferSelected}
            deleteOfferAndCloseModal={deleteOfferAndCloseModal}
            closeModalDelete={closeModalDelete}
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
        color: white;
        font-size: 2.5vw;
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
        text-align: left; /* Ajuste selon le design */
        border-bottom: 1px solid #ddd; /* Ligne séparatrice */
        font-weight: bold;
        text-align: left; /* Alignement du texte des en-têtes */
    }
    .offersHeader {
        display: flex;
        justify-content: space-between;
        width: 55%;
    }



    @media (max-width: 768px) {
        h2 {
            font-size: 4vw;
        }
        .text {
            font-size: 6vw;
        }
        table thead {
            font-size: 3vw; 
        }
        table tbody {
            font-size: 3vw; 
        }
    }
</style>
