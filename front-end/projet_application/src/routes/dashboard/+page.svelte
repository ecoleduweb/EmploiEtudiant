<script lang="ts">
    import "../../styles/global.css"
    import Button from "../../Components/Inputs/Button.svelte"
    import type { Enterprise } from "../../Models/Enterprise"
    import CreateEditJobOffer from "../../Components/JobOffer/CreateEditJobOffer.svelte"
    import ApproveOffer from "../../Components/JobOffer/ApproveOffer.svelte"
    import { onMount } from "svelte"
    import Modal from "../../Components/Common/Modal.svelte"
    import ArchiveConfirm from "../../Components/JobOffer/ArchiveConfirm.svelte"
    import { currentUser, isLoggedIn } from "$lib"
    import LoadingSpinner from "../../Components/Common/LoadingSpinner.svelte"
    import CreateEditEnterprise from "../../Components/Enterprise/CreateEditEnterprise.svelte"
    import { fetchCurrentUserEnterprise } from "../../Service/EnterpriseService"
    import TableDashboard from "../../Components/JobOffer/TableDashboard.svelte"
    import {
        getStatesFromStorage,
        updateState,
    } from "../../Service/CollapsedOfferLists"
    import type { CollapseListsStates } from "../../Service/CollapsedOfferLists"
    import DeleteOffer from "../../Components/JobOffer/DeleteOffer.svelte"
    import type { JobOffer } from "../../Models/Offre"
    import { fetchJobOffersByEmployer } from "../../Service/JobOfferService"
    import { toFormattedDateString } from "../../ts/utils"

    let jobOfferSelected: JobOffer = $state({} as JobOffer)
    let currentEnterprise: Enterprise | undefined = $state()
    let jobOffers: JobOffer[] = $state([])

    let isModerator = $state(false)
    let showApproveModal = $state(false)
    let showCreateEditOfferModal = $state(false)
    let showEditEnterprise = $state(false)
    let showArchiveModal = $state(false)
    let showLoadingSpinner = $state(false)
    let showDeleteModal = $state(false)

    let iconeUp = "⮞"
    let iconeDown = "⮟"

    let hideListsStates = $state(getStatesFromStorage())

    function toggleList(nomListe: keyof CollapseListsStates) {
        hideListsStates = updateState(
            hideListsStates,
            nomListe,
            !hideListsStates[nomListe],
        )
    }

    const handleCreateOffer = () => {
        showCreateEditOfferModal = true
        jobOfferSelected = undefined as any
    }

    const handleDeleteClick = (jobOffer: JobOffer) => {
        jobOfferSelected = jobOffer
        showDeleteModal = true
    }

    const deleteOfferAndCloseModal = (idJobOffer: number | null) => {
        showDeleteModal = false

        if (idJobOffer !== null) {
            jobOffers = jobOffers.filter((x) => x.id !== idJobOffer)
        }
    }

    const handleShowEditEnterpriseModal = () => {
        showEditEnterprise = true
    }

    const handleShowEditJobOfferModal = (jobOffer: JobOffer) => {
        jobOfferSelected = jobOffer
        showCreateEditOfferModal = true
    }

    const handleShowApproveModal = (jobOffer: JobOffer) => {
        jobOfferSelected = jobOffer
        showApproveModal = true
    }

    const handleShowArchiveModal = (jobOffer: JobOffer) => {
        jobOfferSelected = jobOffer
        showArchiveModal = true
    }

    const handleCloseEditModalEnterprise = (
        enterprise: Enterprise | undefined = undefined,
    ) => {
        if (enterprise) {
            currentEnterprise = enterprise
        }
        showEditEnterprise = false
    }

    const handleCloseModalApprove = async () => {
        showApproveModal = false
    }

    const handleCloseModalCreateEdit = async (
        jobOffer: JobOffer | undefined = undefined,
    ) => {
        if (jobOffer) {
            const index = jobOffers.findIndex((x) => x.id === jobOffer.id)
            if (index !== -1) {
                jobOffers[index] = jobOffer
            } else {
                jobOffers = [jobOffer, ...jobOffers]
            }
        }
        showCreateEditOfferModal = false
    }

    const handleCloseModalArchive = async () => {
        showArchiveModal = false
    }

    const handleCloseModalDelete = async () => {
        showDeleteModal = false
    }

    onMount(async () => {
        try {
            isModerator = $currentUser?.isModerator === true
            jobOffers = await fetchJobOffersByEmployer()
            currentEnterprise = await fetchCurrentUserEnterprise()
        } catch (error) {
            console.error("Error while loading:", error)
        } finally {
            showLoadingSpinner = true
        }
    })

    let dateNow = toFormattedDateString(new Date())

    let toBeApprovedOffer = $derived(
        jobOffers
            .filter((x) => x.isApproved === null)
            .sort(
                (a, b) =>
                    new Date(a.lastModifiedDate!).getTime() -
                    new Date(b.lastModifiedDate!).getTime(),
            ),
    )
    let isRefusedOffer = $derived(
        jobOffers.filter((x) => x.isApproved === false),
    )
    let offerToCome = $derived(
        jobOffers.filter((x) => {
            if (!x.isApproved) return false
            let dateDebut = toFormattedDateString(new Date(x.offerDebut))
            return x.offerDebut < dateDebut
        }),
    )
    let offerDisplayed = $derived(
        jobOffers.filter((x) => {
            if (!x.isApproved) return false
            let dateDebut = toFormattedDateString(new Date(x.offerDebut))
            let dateFin = toFormattedDateString(new Date(x.deadlineApply))
            return dateNow >= dateDebut && dateNow <= dateFin
        }),
    )
    let expiredOffer = $derived(
        jobOffers.filter((x) => {
            if (!x.isApproved) return false
            let dateFin = toFormattedDateString(new Date(x.deadlineApply))
            return dateFin < dateNow
        }),
    )
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

            {#if currentEnterprise}
                <div class="divFlex" id="editEnterprise">
                    <Button
                        onClick={handleShowEditEnterpriseModal}
                        text="Modifier l'entreprise"
                    />
                </div>
            {/if}
        </div>
    </section>

    {#if !showLoadingSpinner}
        <section class="Loading">
            <LoadingSpinner />
        </section>
    {:else}
        <section class="offres">
            <h1 class="title">
                <span>MES OFFRES D&apos;EMPLOI</span>
            </h1>
            {#if isRefusedOffer.length > 0}
                <div class="offersHeader">
                    <Button
                        cssId="btnHideRefusedOfferList"
                        text={hideListsStates.hideRefusedOffer
                            ? iconeUp
                            : iconeDown}
                        onClick={() => {
                            toggleList("hideRefusedOffer")
                        }}
                    />
                    <h2 class="textSections">Offres refusées</h2>
                </div>
                <div
                    id="refusedOffersList"
                    style="display: {hideListsStates.hideRefusedOffer
                        ? 'none'
                        : 'block'}"
                >
                    <TableDashboard
                        offers={isRefusedOffer}
                        {isModerator}
                        handleEditModalClick={handleShowEditJobOfferModal}
                        handleApproveModalClick={handleShowApproveModal}
                        handleArchiveModalClick={handleShowArchiveModal}
                        handleDeleteModalClick={handleDeleteClick}
                    />
                </div>
            {/if}
            {#if toBeApprovedOffer.length > 0}
                <div class="offersHeader">
                    <Button
                        cssId="btnHidetoBeApprovedOfferList"
                        text={hideListsStates.hideToBeApprovedOffer
                            ? iconeUp
                            : iconeDown}
                        onClick={() => {
                            toggleList("hideToBeApprovedOffer")
                        }}
                    />
                    <h2 class="textSections">
                        Offres en attente d'approbation
                    </h2>
                </div>
                <div
                    id="toBeApprovedOffersList"
                    style="display: {hideListsStates.hideToBeApprovedOffer
                        ? 'none'
                        : 'block'}"
                >
                    <TableDashboard
                        offers={toBeApprovedOffer}
                        {isModerator}
                        handleEditModalClick={handleShowEditJobOfferModal}
                        handleApproveModalClick={handleShowApproveModal}
                        handleArchiveModalClick={handleShowArchiveModal}
                        handleDeleteModalClick={handleDeleteClick}
                    />
                </div>
            {/if}
            {#if offerToCome.length > 0}
                <div class="offersHeader">
                    <Button
                        cssId="btnHideOfferToCome"
                        text={hideListsStates.hideOfferToCome
                            ? iconeUp
                            : iconeDown}
                        onClick={() => {
                            toggleList("hideOfferToCome")
                        }}
                    />
                    <h2 class="textSections">Offres bientôt affichées</h2>
                </div>
                <div
                    id="offersToComeList"
                    style="display: {hideListsStates.hideOfferToCome
                        ? 'none'
                        : 'block'}"
                >
                    <TableDashboard
                        offers={offerToCome}
                        {isModerator}
                        handleEditModalClick={handleShowEditJobOfferModal}
                        handleApproveModalClick={handleShowApproveModal}
                        handleArchiveModalClick={handleShowArchiveModal}
                        handleDeleteModalClick={handleDeleteClick}
                    />
                </div>
            {/if}
            {#if offerDisplayed.length > 0}
                <div class="offersHeader">
                    <Button
                        cssId="btnHideOfferDisplayed"
                        text={hideListsStates.hideOfferDisplayed
                            ? iconeUp
                            : iconeDown}
                        onClick={() => {
                            toggleList("hideOfferDisplayed")
                        }}
                    />
                    <h2 class="textSections">Offres affichées</h2>
                </div>
                <div
                    id="offerDisplayedList"
                    style="display: {hideListsStates.hideOfferDisplayed
                        ? 'none'
                        : 'block'}"
                >
                    <TableDashboard
                        offers={offerDisplayed}
                        {isModerator}
                        handleEditModalClick={handleShowEditJobOfferModal}
                        handleApproveModalClick={handleShowApproveModal}
                        handleArchiveModalClick={handleShowArchiveModal}
                        handleDeleteModalClick={handleDeleteClick}
                    />
                </div>
            {/if}
            {#if expiredOffer.length > 0}
                <div class="offersHeader">
                    <Button
                        cssId="btnHideExpiredOffer"
                        text={hideListsStates.hideExpiredOffer
                            ? iconeUp
                            : iconeDown}
                        onClick={() => {
                            toggleList("hideExpiredOffer")
                        }}
                    />
                    <h2 class="textSections">Offres expirées</h2>
                </div>
                <div
                    id="expiredOfferList"
                    style="display: {hideListsStates.hideExpiredOffer
                        ? 'none'
                        : 'block'}"
                >
                    <TableDashboard
                        offers={expiredOffer}
                        {isModerator}
                        handleEditModalClick={handleShowEditJobOfferModal}
                        handleApproveModalClick={handleShowApproveModal}
                        handleArchiveModalClick={handleShowArchiveModal}
                        handleDeleteModalClick={handleDeleteClick}
                    />
                </div>
            {/if}
        </section>
    {/if}

    {#if showApproveModal}
        <Modal handleCloseClick={handleCloseModalApprove}>
            <ApproveOffer
                offer={jobOfferSelected}
                handleApproveClick={handleCloseModalApprove}
            />
        </Modal>
    {/if}
    {#if showEditEnterprise}
        <Modal handleCloseClick={handleCloseEditModalEnterprise}>
            <CreateEditEnterprise
                enterpriseToEdit={currentEnterprise}
                onApproveClick={handleCloseEditModalEnterprise}
            />
        </Modal>
    {/if}
    {#if showCreateEditOfferModal}
        <Modal handleCloseClick={handleCloseModalCreateEdit}>
            <CreateEditJobOffer
                onJobOfferProcessed={handleCloseModalCreateEdit}
                jobOfferToEdit={jobOfferSelected}
            />
        </Modal>
    {/if}
    {#if showArchiveModal}
        <Modal handleCloseClick={handleCloseModalArchive}>
            <ArchiveConfirm
                offer={jobOfferSelected}
                handleApproveClick={handleCloseModalArchive}
            />
        </Modal>
    {/if}
    {#if showDeleteModal}
        <Modal handleCloseClick={handleCloseModalDelete}>
            <DeleteOffer
                offer={jobOfferSelected}
                {deleteOfferAndCloseModal}
                closeModalDelete={handleCloseModalDelete}
            />
        </Modal>
    {/if}
</main>

<style lang="scss">
    .Loading {
        height: 100%;
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        position: fixed;
    }

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
        width: 40%;

        :global(.button) {
            margin: 40px 10px 0 10px;
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
