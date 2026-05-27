<script lang="ts">
    import Button from "../Inputs/Button.svelte"
    import RichTextEditor from "../Inputs/RichTextEditor.svelte"
    import MultiSelect from "svelte-multiselect"
    import {
        validateForm,
        jobOfferTemplate,
    } from "../../FormValidations/JobOffer"
    import type { JobOffer } from "../../Models/Offre"
    import { upsertJobOffer } from "../../Service/JobOfferService"
    import { toFormattedDateString } from "../../ts/utils"
    import { onMount } from "svelte"
    import LoadingSpinner from "../Common/LoadingSpinner.svelte"
    import { InvalidDataError } from "../../CustomError/invalidDataError"
    import { fetchEmploymentSchedulesAsOptions } from "../../Service/EmploymentScheduleService"
    import { fetchStudyProgramsAsOptions } from "../../Service/StudyProgramService"
    import type { Option } from "../../Models/Option"
    import EnterpriseSection from "./EnterpriseSection.svelte"

    interface Props {
        onJobOfferProcessed: (jobOffer: JobOffer) => Promise<void>
        jobOfferToEdit: JobOffer | null
    }
    let props: Props = $props()

    const isJobOfferEdit = $derived(!!props.jobOfferToEdit)
    const { onJobOfferProcessed: onFinished } = props

    const jobOffer = $state<JobOffer>(jobOfferTemplate.generate())

    let isSubmitting = $state(false)
    let isFetchingOptions = $state(true)
    let studyProgramOptions: Option[] = $state([])
    let selectedPrograms: Option[] = $state([])
    let employmentScheduleOptions: Option[] = $state([])
    let selectedEmploymentSchedules: Option[] = $state([])

    // Derived max date from offerDebut
    let maxDateString = $derived.by(() => {
        let offerDebut = new Date(jobOffer.offerDebut)
        let maxDate = new Date(
            offerDebut.setDate(offerDebut.getDate() + 15 * 7),
        )
        return toFormattedDateString(maxDate)
    })

    let minDateString = toFormattedDateString(new Date())

    // Met à jour le modèle quand une des valeur dans le $effect change. Ici ce sont les selected
    if (props.jobOfferToEdit) {
        Object.assign(jobOffer, props.jobOfferToEdit)
        jobOffer.offerDebut = toFormattedDateString(jobOffer.offerDebut)
        jobOffer.dateEntryOffice = toFormattedDateString(
            jobOffer.dateEntryOffice,
        )
        jobOffer.deadlineApply = toFormattedDateString(jobOffer.deadlineApply)
    }

    $effect(() => {
        if (isFetchingOptions) return
        const schedules = selectedEmploymentSchedules.map((opt) => ({
            id: opt.value as number,
            description: opt.label,
        }))
        jobOffer.employmentSchedules = schedules
        setFields("employmentSchedules", schedules)
        $errors.employmentSchedules = undefined
    })

    $effect(() => {
        if (isFetchingOptions) return
        jobOffer.enterpriseId = jobOffer.enterprise?.id
        setFields("enterpriseId", jobOffer.enterpriseId)
        $errors.enterpriseId = undefined
    })

    $effect(() => {
        if (isFetchingOptions) return
        const programs = selectedPrograms.map((opt) => ({
            id: opt.value as number,
            name: opt.label,
        }))
        jobOffer.studyPrograms = programs
        setFields("studyPrograms", programs)
        $errors.studyPrograms = undefined
    })

    onMount(async () => {
        isFetchingOptions = true
        ;[employmentScheduleOptions, studyProgramOptions] = await Promise.all([
            fetchEmploymentSchedulesAsOptions(),
            fetchStudyProgramsAsOptions(),
        ])
        if (isJobOfferEdit) {
            selectedEmploymentSchedules = jobOffer.employmentSchedules.map(
                (schedule) => ({
                    label: schedule.description,
                    value: schedule.id,
                }),
            )

            selectedPrograms = jobOffer.studyPrograms.map((program) => ({
                label: program.name,
                value: program.id,
            }))
        }
        isFetchingOptions = false
    })

    const handleSubmit = async () => {
        try {
            isSubmitting = true
            const [updated, errorResponse] = await upsertJobOffer(jobOffer)
            if (errorResponse) {
                errors.set(errorResponse)
            } else if (updated) {
                onFinished(updated)
            }
        } catch (err) {
            console.error(err)
        } finally {
            isSubmitting = false
        }
    }
    const { form, errors, setFields } = validateForm(handleSubmit, jobOffer)
</script>

<div class="content-form">
    <h1>
        {isJobOfferEdit ? "Modification d'une" : "Création d'une"}
        <span class="hightlight">offre d'emploi</span>
    </h1>
    <form use:form class="form-offre">
        <div class="content-form">
            {#if jobOffer.id !== 0 && jobOffer.approbationMessage}
                <h3 style="color: orange;">Offre en attente d'approbation</h3>
                {#if jobOffer.isApproved === true}
                    <h3 style="color: green;">
                        Message d'approbation: {jobOffer.approbationMessage}
                    </h3>
                {:else if jobOffer.isApproved === false}
                    <h3 style="color: red;">
                        Raison du refus: {jobOffer.approbationMessage}
                    </h3>
                {/if}
            {/if}

            <EnterpriseSection bind:enterprise={jobOffer.enterprise} {errors} />
            <div class="form-group-vertical">
                <label for="title">Poste visé*</label>
                <input
                    type="text"
                    bind:value={jobOffer.title}
                    name="title"
                    class="form-control"
                    id="title"
                />
            </div>
            <p class="errors-input">
                {#if $errors.title}{$errors.title}{/if}
            </p>

            <div class="form-group-vertical">
                <label for="schedule">Types d'emploi*</label>
                <MultiSelect
                    id="schedule"
                    name="employmentSchedules"
                    options={employmentScheduleOptions as any[]}
                    closeDropdownOnSelect={true}
                    loading={isFetchingOptions}
                    placeholder="Choisir période(s)..."
                    bind:selected={selectedEmploymentSchedules as any[]}
                />
            </div>
            <p class="errors-input">
                {#if $errors.employmentSchedules}{$errors.employmentSchedules}{/if}
            </p>

            <div class="form-group-vertical">
                <label for="address">Adresse du lieu de travail*</label>
                <input
                    type="text"
                    name="address"
                    bind:value={jobOffer.address}
                    class="form-control"
                    id="address"
                />
            </div>
            <p class="errors-input">
                {#if $errors.address}{$errors.address}{/if}
            </p>

            <div class="form-group-horizontal-date">
                <div class="form-group-vertical">
                    <label for="offerDebut"
                        >Date de publication de l'offre</label
                    >
                    <input
                        type="date"
                        bind:value={jobOffer.offerDebut}
                        name="offerDebut"
                        class="form-control"
                        id="offerDebut"
                        min={minDateString}
                    />
                </div>
                <p class="errors-input">
                    {#if $errors.offerDebut}{$errors.offerDebut}{/if}
                </p>

                <div class="form-group-vertical">
                    <label for="dateEntryOffice"
                        >Date d'entrée en fonction de l'emploi*</label
                    >
                    <input
                        type="date"
                        bind:value={jobOffer.dateEntryOffice}
                        class="form-control"
                        name="dateEntryOffice"
                        id="dateEntryOffice"
                        min={minDateString}
                    />
                </div>
                <p class="errors-input">
                    {#if $errors.dateEntryOffice}{$errors.dateEntryOffice}{/if}
                </p>

                <div class="form-group-vertical">
                    <label for="deadlineApply">Date limite pour postuler*</label
                    >
                    <input
                        type="date"
                        bind:value={jobOffer.deadlineApply}
                        class="form-control"
                        name="deadlineApply"
                        id="deadlineApply"
                        max={maxDateString}
                        min={jobOffer.offerDebut}
                    />
                </div>
                <p class="errors-input">
                    {#if $errors.deadlineApply}{$errors.deadlineApply}{/if}
                </p>
            </div>

            <div class="form-group-vertical">
                <label for="programme">Programme visé*</label>
                <MultiSelect
                    loading={isFetchingOptions}
                    id="programme"
                    name="studyPrograms"
                    options={studyProgramOptions as any[]}
                    closeDropdownOnSelect={true}
                    placeholder="Choisir programme(s)..."
                    bind:selected={selectedPrograms}
                />
            </div>
            <p class="errors-input">
                {#if $errors.studyPrograms}{$errors.studyPrograms}{/if}
            </p>

            <div class="form-group-vertical">
                <label for="salary">Salaire horaire</label>
                <input
                    type="text"
                    bind:value={jobOffer.salary}
                    class="form-control"
                    id="salary"
                    name="salary"
                />
            </div>
            <p class="errors-input">
                {#if $errors.salary}{$errors.salary}{/if}
            </p>

            <div class="form-group-vertical">
                <label for="hoursPerWeek">Heures/semaine*</label>
                <input
                    type="text"
                    bind:value={jobOffer.hoursPerWeek}
                    class="form-control"
                    id="hoursPerWeek"
                    name="hoursPerWeek"
                />
            </div>
            <p class="errors-input">
                {#if $errors.hoursPerWeek}{$errors.hoursPerWeek}{/if}
            </p>

            <div class="form-group-vertical">
                <label for="offerLink"
                    >Lien vers l'offre d'emploi détaillée</label
                >
                <input
                    type="text"
                    bind:value={jobOffer.offerLink}
                    class="form-control"
                    id="offerLink"
                    name="offerLink"
                    placeholder="https://www.exemple.com/"
                />
            </div>
            <p class="errors-input">
                {#if $errors.offerLink}{$errors.offerLink}{/if}
            </p>

            <div class="form-group-vertical">
                <label for="email">Courriel contact*</label>
                <input
                    type="text"
                    bind:value={jobOffer.email}
                    class="form-control"
                    id="email"
                    name="email"
                />
            </div>
            <p class="errors-input">
                {#if $errors.email}{$errors.email}{/if}
            </p>

            <div class="form-group-vertical">
                <label for="description">Description du poste*</label>
                <RichTextEditor
                    name="description"
                    content={jobOffer.description}
                />
            </div>
            <p class="errors-input">
                {#if $errors.description}{$errors.description}{/if}
            </p>

            <div class="accept-Condition">
                <div class="accept-horiz">
                    <input
                        type="checkbox"
                        bind:checked={jobOffer.acceptCondition}
                        class="form-control-acceptCondition"
                        id="acceptCondition"
                        name="acceptCondition"
                    />
                    <label for="acceptCondition"
                        >J'accepte les conditions*</label
                    >
                </div>
                <p class="errors-input">
                    {#if $errors.acceptCondition}{$errors.acceptCondition}{/if}
                </p>

                {#if isSubmitting}
                    <LoadingSpinner />
                {:else}
                    <div class="send">
                        <Button
                            submit={true}
                            text="Envoyer"
                            onClick={() => handleSubmit()}
                        />
                    </div>
                {/if}
            </div>

            <div>
                <p class="condition">
                    *Je consens à ce que les coordonnées inscrites dans le
                    formulaire soient diffusées sur le site d'offre d'emploi du
                    Cégep de Rivière-du-Loup afin que des personnes intéressées
                    par mes offres d'emploi puissent me contacter.
                </p>
            </div>
        </div>
    </form>
</div>

<!-- styles unchanged -->
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
        flex-direction: column;
        justify-content: center;
        width: 100%;
    }
    .accept-horiz {
        display: flex;
        flex-direction: row;
        justify-content: center;
        width: 100%;
    }
    .form-control-acceptCondition {
        margin-right: 0.8vw;
        margin-bottom: 0.5vw;
    }
    .condition {
        font-size: 12px;
        width: 20vw;
    }
    @media (max-width: 768px) {
        .form-offre {
            max-height: 100%;
        }
        .form-group-vertical {
            width: 70%;
        }
        .form-group-horizontal-date {
            flex-direction: column;
            align-items: center;
            width: 100%;
        }
        .accept-Condition {
            flex-direction: column;
            align-items: center;
            width: 100%;
        }
        .accept-horiz {
            flex-direction: row;
            align-items: center;
            width: 30vw;
        }
        .form-control-acceptCondition {
            margin-right: 0;
            margin-bottom: 0.5vw;
        }
        .send {
            margin-bottom: 0vw;
        }
        .condition {
            margin-top: 2vh;
            font-size: 12px;
            width: 60vw;
        }
    }
</style>
