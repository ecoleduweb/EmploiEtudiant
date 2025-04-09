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
    import TableDashboard from "../../Components/JobOffer/TableDashboard.svelte"
    import {getStatesFromStorage, updateState} from "../../Service/CollapsedOfferLists"
    import type {CollapseListsStates} from "../../Service/CollapsedOfferLists"
    import DeleteOffer from "../../Components/JobOffer/DeleteOffer.svelte"
    
    let showApproveModal = false;
    let showCreateEditOffer = false;
    let showEditEnterprise = false;
    let showArchiveModal = false;
    let jobOfferSelected: JobOfferDetails = {} as any
    let isJobOfferEdit = false
    let isModerator = false
    
    let iconeUp = "⮞"
    let iconeDown = "⮟"
    



    let hideListsStates = getStatesFromStorage();

    function toggleList(nomListe: keyof CollapseListsStates) {
    hideListsStates = updateState(hideListsStates, nomListe, !hideListsStates[nomListe]);
}

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
        .sort((a, b) => new Date(a.offerDebut).getTime() - new Date(b.offerDebut).getTime());
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
                <span>MES OFFRES D&apos;EMPLOIS</span>
            </h1>
            {#if isRefusedOffer.length > 0}
                <div class="offersHeader ">
                    <Button cssId="btnHideRefusedOfferList" text={hideListsStates.hideRefusedOffer ? iconeUp : iconeDown} onClick={() => {toggleList("hideRefusedOffer")}}></Button>
                    <h2 class="textSections">Offres refusées</h2>  
                </div>
                <div id="refusedOffersList" style="display: {hideListsStates.hideRefusedOffer ? 'none' : 'block'}">
                    <TableDashboard
                    offers={isRefusedOffer}
                    isModerator={isModerator}
                    handleEditModalClick={handleEditEmploiClick}
                    handleApproveModalClick={handleApproveClick}
                    handleArchiveModalClick={handleArchiveClick}
                    handleDeleteModalClick={handleDeleteClick}
                    />
                </div>
            {/if}
            {#if toBeApprovedOffer.length > 0}
                <div class="offersHeader">
                    <Button cssId="btnHidetoBeApprovedOfferList" text={hideListsStates.hideToBeApprovedOffer? iconeUp : iconeDown} onClick={() =>{toggleList("hideToBeApprovedOffer")}}></Button>
                    <h2 class="textSections">Offres en attente d'approbation</h2>
                </div>
                <div id="toBeApprovedOffersList" style="display: {hideListsStates.hideToBeApprovedOffer ? 'none' : 'block'}">
                    <TableDashboard
                    offers={toBeApprovedOffer}
                    isModerator={isModerator}
                    handleEditModalClick={handleEditEmploiClick}
                    handleApproveModalClick={handleApproveClick}
                    handleArchiveModalClick={handleArchiveClick}
                    handleDeleteModalClick={handleDeleteClick}
                    />
                </div>
            {/if}
            {#if offerToCome.length > 0}
                <div class="offersHeader">
                    <Button cssId="btnHideOfferToCome" text={hideListsStates.hideOfferToCome? iconeUp : iconeDown} onClick={() => {toggleList("hideOfferToCome")}}></Button>
                    <h2 class="textSections">Offres bientôt affichées</h2>
                </div>
                <div id="offersToComeList" style="display: {hideListsStates.hideOfferToCome ? 'none' : 'block'}"> 
                    <TableDashboard
                    offers={offerToCome}
                    isModerator={isModerator}
                    handleEditModalClick={handleEditEmploiClick}
                    handleApproveModalClick={handleApproveClick}
                    handleArchiveModalClick={handleArchiveClick}
                    handleDeleteModalClick={handleDeleteClick}
                    />
                </div>
            {/if}
            {#if offerDisplayed.length > 0}
                <div class="offersHeader">
                    <Button cssId="btnHideOfferDisplayed" text={hideListsStates.hideOfferDisplayed? iconeUp : iconeDown} onClick={() => {toggleList("hideOfferDisplayed")}}></Button>
                    <h2 class="textSections">Offres affichées</h2>
                </div>
                <div id="offerDisplayedList" style="display: {hideListsStates.hideOfferDisplayed ? 'none' : 'block'}">
                    <TableDashboard
                    offers={offerDisplayed}
                    isModerator={isModerator}
                    handleEditModalClick={handleEditEmploiClick}
                    handleApproveModalClick={handleApproveClick}
                    handleArchiveModalClick={handleArchiveClick}
                    handleDeleteModalClick={handleDeleteClick}
                    />
                </div>
            {/if}
            {#if expiredOffer.length > 0}
            <div class="offersHeader">
                <Button cssId="btnHideExpiredOffer" text={hideListsStates.hideExpiredOffer ? iconeUp : iconeDown} onClick={() => { toggleList("hideExpiredOffer")}} ></Button>
                <h2 class="textSections">Offres expirées</h2>
            </div>
            <div id="expiredOfferList" style="display: {hideListsStates.hideExpiredOffer ? 'none' : 'block'}">
                <TableDashboard
                offers={expiredOffer}
                isModerator={isModerator}
                handleEditModalClick={handleEditEmploiClick}
                handleApproveModalClick={handleApproveClick}
                handleArchiveModalClick={handleArchiveClick}
                handleDeleteModalClick={handleDeleteClick}
                />
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

<style lang="scss" scoped>
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
        color: #00ad9a;
    }
    .offersHeader {
        display: flex;
        justify-content: flex-start;
        align-items: flex-end;
        width:40%;
        :global(.button) {
            margin: 40px 10px 0 10px;
        }
        #btnHideExpiredOffer {
            background: linear-gradient(135deg, #4CAF50, #81C784);
            color: rgb(255, 255, 255);
            border: none;
            border-radius: 12px;
            padding: 10px 16px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
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
