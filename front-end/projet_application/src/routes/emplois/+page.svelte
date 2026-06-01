<script lang="ts">
    import "../../styles/global.css"
    import OfferDetail from "../../Components/JobOffer/OfferDetail.svelte"
    import { onMount } from "svelte"
    import Modal from "../../Components/Common/Modal.svelte"
    import LoadingSpinner from "../../Components/Common/LoadingSpinner.svelte"
    import TableOffer from "../../Components/JobOffer/TableOffer.svelte"
    import { pushState } from "$app/navigation"
    import { page } from "$app/stores"
    import type { JobOffer } from "../../Models/Offre"
    import MultiSelect from "svelte-multiselect"
    import Button from "../../Components/Inputs/Button.svelte"
    import { fetchEmploymentSchedulesAsOptions } from "../../Service/EmploymentScheduleService"
    import { fetchApprovedJobOffers } from "../../Service/JobOfferService"
    import { fetchStudyProgramsAsOptions } from "../../Service/StudyProgramService"
    import type { Option } from "../../Models/Option"

    let showModal = $state(false)
    let loaded = $state(false)
    let selectedOffer: JobOffer = $state(undefined as any)
    let showFilterModal = $state(false)
    const allProgramsId = 16 // Gros fix super sale qui retourne le id du "programme" générique "Tous les programmes" pour le comparer lors du filtrage. C'est le id en prod :S

    const handleFilterOffer = () => {
        showFilterModal = true
    }

    const closeFilterModal = () => {
        showFilterModal = false
    }

    const handleShowJobOfferModal = (offer: JobOffer) => {
        showModal = true
        selectedOffer = offer
        pushState("?id=" + offer.id, {})
    }

    const handleCloseJobOfferModal = () => {
        showModal = false
        pushState("/emplois", {})
    }

    let jobOffers: JobOffer[] = $state([])
    let filteredOffers: JobOffer[] = $state([])

    let programOptions: Option[] = $state([])
    let selectedPrograms: Option[] = $state([])

    let scheduleOption: Option[] = $state([])
    let selectedSchedule: Option[] = $state([])

    $effect(() => {
        filteredOffers = jobOffers.filter((offer) => {
            const progToFilterId = selectedPrograms[0]?.value
            const matchesPrograms =
                selectedPrograms.length === 0 ||
                offer.studyPrograms?.some(
                    (x) => x.id === progToFilterId || x.id === allProgramsId,
                )

            const schedulesToFilterId = selectedSchedule[0]?.value
            const matchesSchedules =
                selectedSchedule.length === 0 ||
                offer.employmentSchedules?.some(
                    (x) => x.id === schedulesToFilterId,
                )
            // retourne la combinaison des deux filtres, si les deux sont appliqués, sinon retourne le filtre qui est appliqué
            return matchesPrograms && matchesSchedules
        })
    })

    const handleRemoveProgramFilterClick = () => {
        selectedPrograms = []
    }

    const handleRemoveScheduleFilterClick = () => {
        selectedSchedule = []
    }

    onMount(async () => {
        try {
            scheduleOption = await fetchEmploymentSchedulesAsOptions()
            programOptions = await fetchStudyProgramsAsOptions()
            jobOffers = await fetchApprovedJobOffers()
            filteredOffers = jobOffers
            // affiche l'offre d'emploi si un id est présent dans les query params
            const id = $page.url.searchParams.get("id")
            if (id) {
                let jobOffer = jobOffers.find(
                    (offer) => offer.id.toString() == id,
                )
                if (jobOffer) {
                    showModal = true
                    selectedOffer = jobOffer
                }
            }
        } catch (error) {
            console.error("Error fetching job offers:", error)
            alert(
                "Une erreur est survenue lors du chargement des offres d'emploi.",
            )
        } finally {
            loaded = true
        }
    })
</script>

<main>
    <section class="haut">
        <div class="haut-gauche">
            <h1 class="title">
                <span class="text">OFFRES D'EMPLOI </span><span class="text">
                    DISPONIBLES</span
                >
            </h1>
            {#if loaded}
                <div class="filtre">
                    <Button onClick={handleFilterOffer} text="Filtrer" />
                </div>
                <div>
                    {#if selectedPrograms.length > 0 || selectedSchedule.length > 0}
                        <div class="badge-container">
                            {#if selectedPrograms.length > 0}
                                <div class="badge">
                                    {selectedPrograms[0].label}
                                    <button
                                        type="button"
                                        class="badge-close"
                                        onclick={handleRemoveProgramFilterClick}
                                        >x</button
                                    >
                                </div>
                            {/if}
                            {#if selectedSchedule.length > 0}
                                <div class="badge">
                                    {selectedSchedule[0].label}
                                    <button
                                        type="button"
                                        class="badge-close"
                                        onclick={handleRemoveScheduleFilterClick}
                                        >x</button
                                    >
                                </div>
                            {/if}
                        </div>
                    {/if}
                </div>
            {:else}
                <div></div>
            {/if}
        </div>
    </section>

    <section>
        {#if loaded}
            {#if filteredOffers.length <= 0}
                <div class="text">
                    <p>Aucune offre trouvée</p>
                </div>
            {:else}
                <TableOffer
                    offers={filteredOffers}
                    handleOfferClick={handleShowJobOfferModal}
                />
            {/if}
        {:else}
            <div class="loading">
                <LoadingSpinner />
            </div>
        {/if}
    </section>

    {#if showFilterModal}
        <Modal handleCloseClick={closeFilterModal}>
            <div class="filtre-modal">
                <h1 class="title-filtre">Filtrer les offres</h1>
                <p class="text-filtre">Programme visé:</p>
                <MultiSelect
                    id="programme"
                    options={programOptions as any}
                    closeDropdownOnSelect={true}
                    maxSelect={1}
                    placeholder="Choisir un programme visé..."
                    bind:selected={selectedPrograms as any}
                />
                <p class="text-filtre">Type d'emploi:</p>
                <MultiSelect
                    id="schedule"
                    options={scheduleOption as any}
                    closeDropdownOnSelect={true}
                    maxSelect={1}
                    placeholder="Choisir un type d'emploi..."
                    bind:selected={selectedSchedule as any}
                />
                <Button
                    onClick={() => (showFilterModal = false)}
                    text="Confirmer"
                />
            </div>
        </Modal>
    {/if}

    {#if showModal}
        <Modal handleCloseClick={handleCloseJobOfferModal}>
            <OfferDetail offer={selectedOffer} />
        </Modal>
    {/if}
</main>

<style scoped>
    .loading {
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
        margin: 12px;
    }

    .title {
        left: 7.2%;
        margin: 0;
        margin-top: 30px;
    }

    .title span:first-child {
        color: white;
        margin-right: 10px;
    }

    .title span:last-child {
        color: #00ad9a;
        margin: 0;
    }

    .filtre {
        margin-top: 20px;
    }

    .title-filtre {
        color: #00ad9a;
        font-size: 28px;
        margin: 0;
    }

    .filtre-modal {
        display: flex;
        flex-direction: column;
        gap: 20px;
        text-align: left;
    }

    .text-filtre {
        color: black;
        font-size: 20px;
        margin: 0;
    }

    .badge-container {
        display: flex;
        flex-wrap: wrap;
        margin-top: 20px;
    }

    .badge {
        display: inline-flex;
        align-items: center;
        background-color: #252a35;
        border: 1px solid #1d2029;
        border-radius: 20px;
        padding: 4px 12px;
        font-family: Arial, sans-serif;
        font-size: 14px;
        color: white;
        margin-right: 8px;
        margin-bottom: 8px;
    }

    .badge-close {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-left: 8px;
        cursor: pointer;
        font-size: 12px;
        font-weight: bold;
        background-color: #252a35;
        color: #00bfaa;
        border: none;
        border-radius: 50%;
        width: 18px;
        height: 18px;
        padding: 0;
        line-height: 1;
        transition: background-color 0.2s;
    }

    .badge-close:hover {
        background-color: #1a1e26;
    }

    .text {
        font-size: 2.5vw;
        color: white;
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
    }

    @media (max-width: 768px) {
        .text {
            font-size: 6vw;
            width: 100%;
        }
        .title {
            width: 100vw;
        }
    }
</style>
