<script lang="ts">
    import getAllEnterprise from "../../Service/EnterpriseService"
    import Button from "../Inputs/Button.svelte"
    import MultiSelect from "svelte-multiselect"
    import ValidationSchema, { entrepriseSchema } from "../../FormValidations/JobOffer"
    import {ValidationError} from "yup"
    import type { JobOffer } from "../../Models/Offre"
    import type { Enterprise } from "../../Models/Enterprise"
    import { GET, POST, PUT } from "../../ts/server"
    import { extractErrors } from "../../ts/utils"
    import { onMount } from "svelte"
    import { currentUser, isLoggedIn, studyPrograms } from "$lib"
    import fetchCity from "../../Service/CityService"
    import EntrepriseDetails from "./EntrepriseDetails.svelte"
    import CreateEditEnterprise from "./CreateEditEnterprise.svelte"
    import { writable } from "svelte/store"
    import LoadingSpinner from "../Common/LoadingSpinner.svelte"
    export let onFinished: () => Promise<void>
    export let isJobOfferEdit: boolean

    // valeur par défaut de l'offer utilisée pour le create.
    export let jobOffer: JobOffer = {
        id: 0,
        title: "",
        address: "",
        description: "",
        offerDebut: new Date().toISOString().split("T")[0],
        dateEntryOffice: new Date().toISOString().split("T")[0],
        deadlineApply: new Date().toISOString().split("T")[0],
        email: "",
        hoursPerWeek: 0,
        internship: false,
        offerLink: "https://",
        offerStatus: 0,
        active: true,
        salary: "",
        employerId: -1,
        isApproved: false,
        approbationMessage: "",
        acceptCondition: false,
    }
    export let enterprise: Enterprise = {
        id: 0,
        name: "",
        address: "",
        email: "",
        phone: "",
        cityId: 0,
        isTemporary: false,
    }

    let errors: any = {}
    let errorsEnterprise: any = {}
    let isModerator: boolean = false
    let enterpriseSelected: { label: string; value: number }[] = []
    let enterpriseFromSelectedEnterprise: [] = [] // valeur de l'offre actuel (lorsque l'on editera une offre existante)
    let enterpriseOption: { label: string; value: number }[] = []
    let isEnterpriseSelected: boolean = false
    let selectedCity: { label: string; value: number }[] = []
    let cityFromEnterprise: [] = []
    let cityOptions: { label: string; value: number }[] = []
    let scheduleIds: number[] = []
    let selectedCityWritable = writable<any>()

    $: selectedCity = $selectedCityWritable

    const fetchEnterprise = async () => {
        let response = undefined
        if (isJobOfferEdit === true) {
            response = await GET<any>(
                `/enterprise/employer/${jobOffer.employerId}`
            )
        } else if (!isModerator) {
            const employer = await GET<any>("/employer/currentEmployer")

            jobOffer.employerId = employer?.id
            if (employer)
                response = await GET<any>(
                    `/enterprise/employer/${employer.id}`
                )
        }
        if (response !== undefined) {
            enterprise = response
            selectedCityWritable.set(cityOptions.filter((x) => x.value === enterprise.cityId))
            isEnterpriseSelected = true
        } else {
            isEnterpriseSelected = false
        }
    }

    const fetchEmploymentSchedule = async () => {
    const response = await GET<any>(`/employmentSchedule/getByOfferId/${jobOffer.id}`)

    scheduleSelected = scheduleOption.filter((option: { label: string; value: number }) => 
        response.some((schedule: { id: number }) => schedule.id === option.value)
        )
    }

    onMount(async () => {
        cityOptions = await fetchCity()
        if ($isLoggedIn) {
            isModerator = ($currentUser as any).isModerator
        }
        if (isModerator === true) {
            enterpriseOption = await getAllEnterprise()
        }
        await fetchEnterprise()
        await getSchedule()
        if (isJobOfferEdit) {
            await getScheduleByOfferId()
        }
        if (isJobOfferEdit === true) {
        const schedules = scheduleOption.filter(
            (s) => scheduleIds.includes(s.value),
        )
        if (schedules.length > 0) {
            scheduleSelected = schedules.map(schedule => ({
                label: schedule.label,
                value: schedule.value,
            }));
        }
            const programs = await GET<any>(
                `/offerProgram/${jobOffer.id}`,
            )
            selectedPrograms = programs
                .map((programId: number) => {
                    let program = programOptions.find(
                        (p) => p.value === programId,
                    )
                    return program
                        ? { label: program.label, value: program.value }
                        : null
                })
                .filter((p: number) => p !== null) // Filtrer les éventuels null si aucun programme n'est trouvé
        }
        if (isJobOfferEdit) {
            await fetchEmploymentSchedule()
        }
    })

    const setEnterpriseIfSelected = async (enterpriseId: number) => {
        const response = await GET<any>(
            `/enterprise/${enterpriseId}`,
        )
        enterprise = response
        const city = cityOptions.find(
            (ville) => ville.value === response.cityId,
        )
        if (city) {
            selectedCityWritable.set([city])
        }
        if (enterprise === undefined) {
            isEnterpriseSelected = false
        } else {
            isEnterpriseSelected = true
        }
    }

    //--------------------------------------------------

    let selectedPrograms = [{ label: "", value: 0 }]
    let programmeFromSelectedOffer: [] = [] // valeur de l'offre actuel (lorsque l'on editera une offre existante)
    let programOptions: { label: string; value: number; }[] = $studyPrograms.map((x: any) => ({"label": x.name, "value": x.id}))

    const getSchedule = async () => {
        const response = await GET<any>(
            `/employmentSchedule/all`,
        )
        scheduleOption = response.map((schedule: { id: number; description: string }) => ({
            label: schedule.description,
            value: schedule.id,
        }))
    }

    const getScheduleByOfferId = async () => {
        const response = await GET<any>(
            `/employmentSchedule/getByOfferId/${jobOffer.id}`,
        )
        scheduleSelected = response.map((schedule: { id: number; description: string }) => ({
            label: schedule.description,
            value: schedule.id,
        }))
    }

    let scheduleSelected: { label: string; value: number }[] = [{
        label: "",
        value: 0,
    }]
    let scheduleFromExistingOffer: [] = [] // valeur de l'offre actuel (lorsque l'on editera une offre existante)
    let scheduleOption: { label: string; value: number }[] = []

    //--------------------------------------------------

    let errorsProgramme: string = "" // Define a variable to hold the error message for selected program
    let errorsSchedule: string = "" // Define a variable to hold the error message for schedules
    let errorsAcceptCondition: string = "" // Define a variable to hold the error message for accepting condition

    const handleSubmit = async () => {
        if (isJobOfferEdit) {
            await updateJobOffer()
        } else {
            await createJobOffer()
        }
    }

    const handleEnterprise = () => {
        window.open("/enterprise", "_blank");
    }

    
    const prepareAndJobOfferIsValid = async () => {
        let validatingjobOffer = false
        if (jobOffer?.approbationMessage === null) 
        {
            jobOffer.approbationMessage = jobOffer?.approbationMessage  ? jobOffer.approbationMessage : ''
        }

        try {
            scheduleIds = Array.isArray(scheduleSelected) && scheduleSelected.length !== 0 ? scheduleSelected.map(schedule => schedule.value) : [];
            enterprise.cityId = selectedCity[0]?.value ? selectedCity[0]?.value : -1

            const jobOfferToValidate = {
                ...jobOffer,  
                studyPrograms: selectedPrograms, 
                scheduleIds
            }

            await entrepriseSchema.validate(enterprise, {abortEarly: false})

            validatingjobOffer = true
            await ValidationSchema.validate(jobOfferToValidate, { abortEarly: false })

            return {
                    enterprise: {
                        ...enterprise,
                    }, 
                    jobOffer: {
                        ...((({ acceptCondition, ...rest }) => rest)(jobOffer)),
                    },
                    studyPrograms: selectedPrograms.map((p) => p.value),
                    scheduleIds: scheduleIds,
                }
        }
        catch(err) {
            if (err instanceof ValidationError && validatingjobOffer === true) {
                errors = extractErrors(err)
                errorsEnterprise = {}
            }
            else if (err instanceof ValidationError && validatingjobOffer === false) 
            {
                errorsEnterprise = extractErrors(err)
            }
        }
    }

    async function createJobOffer() {
        try {
            const requestData = await prepareAndJobOfferIsValid()
            const response = await POST<any, any>(
                "/jobOffer/new",
                requestData, false)
            if (response) {
                onFinished()
            }
        } catch (err) {

        }
    }

    async function updateJobOffer() {
        try {
            const requestData = await prepareAndJobOfferIsValid()
            const response = await PUT<any, any>(
                `/jobOffer/${jobOffer.id}`,
                requestData, false)
            if (response) {
                onFinished()
            }
        } catch (err) {

            
        }
    }

    let maxDateString: any
    $: {
        let offerDebut = new Date(jobOffer.offerDebut)
        let maxDate = new Date(
            offerDebut.setDate(offerDebut.getDate() + 15 * 7),
        )
        maxDateString = maxDate.toISOString().split("T")[0] // format as yyyy-mm-dd
    }

    let todayMin = new Date()
    let minDateString = todayMin.toISOString().split("T")[0] // format as yyyy-mm-dd
</script>

<form on:submit|preventDefault={handleSubmit} class="form-offre">
    <div class="content-form">
        {#if jobOffer.id !== 0}
            {#if jobOffer.isApproved === true}
                <h3 style="color: green;">
                Raison d'acceptation: {jobOffer.approbationMessage}
                </h3>
            {:else if jobOffer.isApproved === false}
                <h3 style="color: red;">
                    Raison du refus: {jobOffer.approbationMessage}
                </h3>
            {/if}
        {/if}

        {#if !isJobOfferEdit}
            {#if isModerator}
                <h1>Sélectionner une entreprise existante</h1>
                <div class="form-group-horizontal">
                    {#if enterpriseOption.length}
                        <MultiSelect
                            id="enterprise"
                            options={enterpriseOption}
                            closeDropdownOnSelect={true}
                            maxSelect={1}
                            placeholder="Choisir une enterprise..."
                            bind:value={enterpriseSelected}
                            bind:selected={enterpriseFromSelectedEnterprise}
                            on:add={(event) => setEnterpriseIfSelected(event.detail.option.value)}
                        />
                    {:else}
                        <LoadingSpinner />
                    {/if}
                    <Button
                        submit={false}
                        text="Ajouter"
                        onClick={() => handleEnterprise()}
                    />
                </div>
                {#if enterprise.id !== 0 && selectedCity.length !== 0}
                    <EntrepriseDetails {enterprise} {selectedCity} ></EntrepriseDetails>
                {/if}
            {:else}
                {#if isEnterpriseSelected}
                    <h1>Création d'une nouvelle entreprise</h1>
                    <EntrepriseDetails {enterprise} {selectedCity}></EntrepriseDetails>
                {:else}
                    <h1>Création d'une nouvelle entreprise</h1>
                    <CreateEditEnterprise {enterprise} {errorsEnterprise} {cityOptions} selectedCity={selectedCityWritable} {cityFromEnterprise} ></CreateEditEnterprise>
                {/if}
            {/if}

            <h1>Création d'une nouvelle offre d'emploi</h1>
        {:else}
            <h1>Mon entreprise</h1>
            <EntrepriseDetails {enterprise} {selectedCity}></EntrepriseDetails>

            <h1>Modification d'une offre d'emploi</h1>
        {/if}

        <div class="form-group-vertical">
            <label for="title">Titre du poste*</label>
            <input
                type="text"
                bind:value={jobOffer.title}
                class="form-control"
                id="titre"
            />
        </div>
        <p class="errors-input">
            {#if errors.title}{errors.title}{/if}
        </p>
        <div class="form-group-vertical">
            <label for="schedule">Type d'emplois*</label>
            {#if scheduleOption.length}
                <MultiSelect
                    id="schedule"
                    options={scheduleOption}
                    closeDropdownOnSelect={true}
                    placeholder="Choisir période(s)..."
                    bind:value={scheduleSelected}
                    bind:selected={scheduleFromExistingOffer}
                />
            {:else}
                <LoadingSpinner />
            {/if}
        </div>
        <p class="errors-input">
            {#if errors.scheduleIds}{errors.scheduleIds}{/if}
        </p>
        <div class="form-group-vertical">
            <label for="lieu">Adresse du lieu de travail*</label>
            <input
                type="text"
                bind:value={jobOffer.address}
                class="form-control"
                id="address"
            />
        </div>
        <p class="errors-input">
            {#if errors.address}{errors.address}{/if}
        </p>
        <div class="form-group-horizontal-date">
            <div class="form-group-vertical">
                <label for="offerDebut"
                    >Date de publication de l'offre</label
                >
                <input
                    type="date"
                    bind:value={jobOffer.offerDebut}
                    class="form-control"
                    id="offerDebut"
                    min={minDateString}
                />
            </div>
            <p class="errors-input">
                {#if errors.offerDebut}{errors.offerDebut}{/if}
            </p>
            <div class="form-group-vertical">
                <label for="dateEntryOffice"
                    >Date d'entrée en fonction de l'emploi*</label
                >
                <input
                    type="date"
                    bind:value={jobOffer.dateEntryOffice}
                    class="form-control"
                    id="dateEntryOffice"
                    min={minDateString}
                />
            </div>
            <p class="errors-input">
                {#if errors.dateEntryOffice}{errors.dateEntryOffice}{/if}
            </p>
            <div class="form-group-vertical">
                <label for="deadlineApply">Date limite pour postuler*</label
                >
                <input
                    type="date"
                    bind:value={jobOffer.deadlineApply}
                    class="form-control"
                    id="deadlineApply"
                    max={maxDateString}
                    min={jobOffer.offerDebut}
                />
            </div>
            <p class="errors-input">
                {#if errors.deadlineApply}{errors.deadlineApply}{/if}
            </p>
        </div>
        <div class="form-group-vertical">
            <label for="duree">Programme visé*</label>
            {#if programOptions.length}
                <MultiSelect
                    id="programme"
                    options={programOptions}
                    closeDropdownOnSelect={true}
                    placeholder="Choisir programme(s)..."
                    bind:value={selectedPrograms}
                    bind:selected={programmeFromSelectedOffer}
                ></MultiSelect>
            {:else}
                <LoadingSpinner />
            {/if}
        </div>
        <p class="errors-input">
            {#if errors.studyPrograms}{errors.studyPrograms}{/if}
        </p>
        <div class="form-group-vertical">
            <label for="salary">Salaire/H</label>
            <input
                type="text"
                bind:value={jobOffer.salary}
                class="form-control"
                id="salary"
            />
        </div>
        <p class="errors-input">
            {#if errors.salary}{errors.salary}{/if}
        </p>
        <div class="form-group-vertical">
            <label for="hoursPerWeek">Heure/Semaine*</label>
            <input
                type="text"
                bind:value={jobOffer.hoursPerWeek}
                class="form-control"
                id="hoursPerWeek"
            />
        </div>
        <p class="errors-input">
            {#if errors.hoursPerWeek}{errors.hoursPerWeek}{/if}
        </p>
        <div class="form-group-vertical">
            <label for="offerLink"
                >Adresse URL vers l'offre d'emploi détaillé</label
            >
            <input
                type="text"
                bind:value={jobOffer.offerLink}
                class="form-control"
                id="offerLink"
            />
        </div>
        <p class="errors-input">
            {#if errors.offerLink}{errors.offerLink}{/if}
        </p>
        <div class="form-group-vertical">
            <label for="courriel-contact">Courriel contact*</label>
            <input
                type="text"
                bind:value={jobOffer.email}
                class="form-control"
                id="email"
            />
        </div>
        <p class="errors-input">
            {#if errors.email}{errors.email}{/if}
        </p>
        <div class="form-group-vertical">
            <label for="description">Description du poste*</label>
            <textarea
                rows="15"
                cols="50"
                bind:value={jobOffer.description}
                class="form-control"
                id="description"
            />
        </div>
        <p class="errors-input">
            {#if errors.description}{errors.description}{/if}
        </p>
        <div class="accept-Condition">
            <div class="accept-horiz">
                <input
                    type="checkbox"
                    bind:checked={jobOffer.acceptCondition}
                    class="form-control-acceptCondition"
                    id="acceptCondition"
                />
                <label for="acceptCondition"
                    >J'acceptes les condtions
                </label>
            </div>
            <p class="errors-input">
                {#if errors.acceptCondition}{errors.acceptCondition}{/if}
            </p>
            <div class="send">
                <Button
                    submit={true}
                    text="Envoyer"
                    on:click={() => handleSubmit()}
                    onClick={() => ""}
                />
            </div>
        </div>
    </div>
</form>

<style>
    label {
        display: block;
        margin-bottom: 0.26vw;
    }
    h1 {
        margin: 0;
    }

    .form-offre {
        display: flex;
        flex-direction: column;
        overflow-y: scroll;
        max-height: 700px;
        border: 0.3vw solid #ccc;
        background-color: #ffff;
        box-shadow: 0 0.104vw 0.208vw rgba(0, 0, 0, 0.1);
        border-radius: 0.781vw;
    }

    .content-form {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }

    .form-group-horizontal {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        width: 80%;
        margin: 1vh 0;
    }

    .form-group-vertical {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        width: 80%;
        margin: 0.8vw;
    }
    .form-group-horizontal-date {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        width: 83.25%;
    }

    .errors-input {
        color: red;
        font-size: 0.8em;
    }
    .accept-Condition {
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        width: 100%;
    }
    .accept-horiz {
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        width: 100%;
    }
    .accept-horiz {
        display: flex;
        flex-direction: row;
        margin: 0.8vw;
    }
    .form-control-acceptCondition {
        margin-right: 0.8vw;
        margin-bottom: 0.5vw;
    }
</style>
