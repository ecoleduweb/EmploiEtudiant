<script lang="ts">
    import "../../styles/global.css"
    import DetailOfferRow from "../../Components/JobOffer/DetailOfferRow.svelte"
    import OfferDetail from "../../Components/JobOffer/OfferDetail.svelte"
    import { writable } from "svelte/store"
    import { GET } from "../../ts/server"
    import { onMount } from "svelte"
    import Modal from "../../Components/Common/Modal.svelte"
    import LoadingSpinner from "../../Components/Common/LoadingSpinner.svelte"
    import TableEmplois from "../../Components/JobOffer/TableOffer.svelte"
    import { pushState } from "$app/navigation"
    import { page } from '$app/stores'
    import type { JobOfferDetails } from "../../Models/JobOfferDetails"
    import { studyPrograms } from "$lib"
    import MultiSelect from "svelte-multiselect"
    import Button from "../../Components/Inputs/Button.svelte"

    let showModal = false
    let loaded = false
    let selectedOffer: JobOfferDetails = undefined as any
    let showFilterOffer = false

    const handleFilterOffer = () => {
        showFilterOffer = true
    }

    const closeFilterModal = () => {
        showFilterOffer = false
    }

    const handleAddJobOfferClick = (offer: JobOfferDetails) => {
        showModal = true
        selectedOffer = offer
        pushState("?id=" + offer.id, {})
    }
    
    const closeModal = () => {
        showModal = false
        pushState("/emplois", {})
    }

    let jobOffers: JobOfferDetails[] = []
    let filteredOffers: JobOfferDetails[] = []

    let programOptions: { label: string; value: number; }[] = []
    let selectedPrograms: { label: string; value: number; }[] = []

    let scheduleOption: { label: string; value: number }[] = []
    let selectedSchedule: { label: string; value: number }[] = []

    const getSchedule = async () => {
        try {
            const response = await GET<any>(
                `/employmentSchedule/all`,
            )
            scheduleOption = response.map((schedule: { id: number; description: string }) => ({
            label: schedule.description,
            value: schedule.id,
        })) 
        } catch (error) {
            console.error("Error fetching schedules:", error)
        }
    }

    const confirmModalFilter = () => {
        showFilterOffer = false;
        // En attente de la tache qui va ajouter une colonne a la bd pour tous les programmes
        const allProgramsId = selectedPrograms.find(x => x.label === "Tous les programmes")?.value || 0;

        filteredOffers = jobOffers.filter(offer => {
            if (selectedPrograms.length === 0 && selectedSchedule.length === 0) {
                return true;
            }

            const progToFilterId = selectedPrograms.at(0)?.value
            const matchesPrograms = selectedPrograms.length === 0 || 
            offer.studyPrograms?.some(prog => prog.id === progToFilterId || prog.id === allProgramsId);

            const schedulesToFilterId = selectedSchedule.at(0)?.value
            const matchesSchedules = selectedSchedule.length === 0 ||
            offer.schedules?.some(schedule => parseInt(schedule.id) === schedulesToFilterId);
        
            return matchesPrograms && matchesSchedules;
        });
    };

    const onRemoveProgramFilterClick = (program: { label: string; value: number }) => {
        selectedPrograms = selectedPrograms.filter((x) => x.value !== program.value)
        confirmModalFilter()
    }
    const onRemoveScheduleFilterClick = (schedule: { label: string; value: number }) => {
        selectedSchedule = selectedSchedule.filter((x) => x.value !== schedule.value)
        confirmModalFilter()
    }

    onMount(async () => {
        try {
            getSchedule()
            const response = await GET<JobOfferDetails[]>("/jobOffer/approved?entrepriseDetails=true&employmentScheduleDetails=true&studyProgramDetails=true")
            jobOffers = response
            filteredOffers = jobOffers

        programOptions = $studyPrograms
            .map((x: any) => ({ "label": x.name, "value": x.id }))
            .sort((a, b) => a.label.localeCompare(b.label, 'fr', { sensitivity: 'base' }));
            
        } catch (error) {
            console.error("Error fetching job offers:", error)
        }
        finally
        {
            loaded = true

            const id = $page.url.searchParams.get('id')

            if (id !== '') 
            {
                let jobOffer = jobOffers.find((offer) => offer.id.toString() == id)
                
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
                <span class="text">OFFRES D'EMPLOI </span><span class="text">
                    DISPONIBLES</span
                >
            </h1>
            {#if loaded}
                <div class="filtre">
                    <Button
                        onClick={handleFilterOffer}
                        text="Filtrer"
                    />
                </div>
                <div>
                    {#if selectedPrograms.length > 0 || selectedSchedule.length > 0}
                        <div class="badge-container">
                            {#if selectedPrograms.length > 0}
                                <div class="badge">
                                    {selectedPrograms[0].label}
                                    <button type="button" class="badge-close" on:click={() => onRemoveProgramFilterClick (selectedPrograms[0])}>x</button>
                                </div>
                            {/if}
                            {#if selectedSchedule.length > 0}
                                <div class="badge">
                                    {selectedSchedule[0].label}
                                    <button type="button" class="badge-close" on:click={() => onRemoveScheduleFilterClick (selectedSchedule[0])}>x</button>
                                </div>
                            {/if}
                        </div>
                    {/if}
                </div>
            {:else}
                <div />
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
                <TableEmplois offers={filteredOffers} handleOfferClick={handleAddJobOfferClick}/>
            {/if}
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

    {#if showFilterOffer}
        <Modal handleCloseClick={closeFilterModal}>               
            <div class="filtre-modal">
                <h1 class="title-filtre">Filtrer les offres</h1>
                <p class="text-filtre">Programme visé:</p>
                <MultiSelect
                    id="programme"
                    options={programOptions}
                    closeDropdownOnSelect={true}
                    maxSelect={1}
                    placeholder="Choisir un programme visé..."
                    bind:selected={selectedPrograms}
                    bind:value={selectedPrograms}
                />
                <p class="text-filtre">Type d'emploi:</p>
                <MultiSelect
                    id="schedule"
                    options={scheduleOption}
                    closeDropdownOnSelect={true}
                    maxSelect={1}
                    placeholder="Choisir un type d'emploi..."
                    bind:selected={selectedSchedule}
                    bind:value={selectedSchedule}
                />
                <Button
                    onClick={confirmModalFilter}
                    text="Confirmer"
                />
            </div>
        </Modal>
    {/if}

    {#if showModal}
        <Modal handleCloseClick={closeModal}>
            <OfferDetail offer={selectedOffer} />
        </Modal>
    {/if}
</main>

<style scoped>
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
        margin: 0;
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
    @media (max-width: 768px)
    {
        .text{
            font-size: 6vw;
            width: 100%;
        }
        .title
        {
            width: 100vw;
        }
    }
</style>
