<script lang="ts">
    import type { JobOffer } from "../../Models/Offre"
    import type { Enterprise } from "../../Models/Enterprise"
    import { GET } from "../../ts/server"
    import { onMount } from "svelte"
    import LoadingSpinner from "../Common/LoadingSpinner.svelte";
    import { studyPrograms } from "$lib"
    import fetchCity from "../../Service/CityService"
    export let offer: JobOffer

    let hideURL = false;

    let cityOptions: any;
    let selectedCity: any;

    let enterprise: Enterprise 
    const getEnterprises = async (employerId: number) => {
        try {
            const response = await GET<any>(
                `/enterprise/employer/${employerId}`
            )
            enterprise = response
        } catch (error) {
            console.error("Error fetching enterprise:", error)
        }
    }

    let loaded = false;

    onMount(async () => {
        await getEnterprises(offer.employerId)
        cityOptions = await fetchCity()
        const response = await GET<any>(
            `/offerProgram/${offer.id}`,
        )
        try {
            programmeSelected = response
                .map((programId: number) => {
                    let program = programmesOption.find(
                        (p) => p.value === programId,
                    )
                    return program
                        ? { label: program.label, value: program.value }
                        : null
                })
                .filter((p: number) => p !== null) // Filtrer les éventuels null si aucun programme n'est trouvé

                if (offer.offerLink == "https://" || offer.offerLink == "http://") 
                {
                    hideURL = true;
                }

        } catch (error) {
            console.error("Error fetching program:", error)
        }

        await getScheduleByOfferId()
        
        loaded = true;
        
    })
    let programmeSelected = [] as any
    let programmesOption: { label: string; value: number; }[] = $studyPrograms.map((x: any) => ({"label": x.name, "value": x.id}))
    
    let scheduleSelected: { label: string; value: number }[] = [{
        label: "",
        value: 0,
    }]

    const getScheduleByOfferId = async () => {
        const response = await GET<any>(
            `/employmentSchedule/getByOfferId/${offer.id}`,
        )
        scheduleSelected = response.map((schedule: { id: number; description: string }) => ({
            label: schedule.description,
            value: schedule.id,
        }))
    }

    $: if (cityOptions) {
        const city = cityOptions.find(
            (ville: any) => ville.value === enterprise.cityId,
        )

        if (city) {
            selectedCity = [city]
        }
    }
</script>


<div class="container">

    {#if !loaded}
        <div class="Loading2">
            <LoadingSpinner />
        </div>
    {:else}
        <div class="titleContainer">
            <h3 class="title">{offer.title}</h3>
            {#if enterprise}
                <h4 class="subtitle">Chez {enterprise.name}</h4>
            {/if}
        </div>

        {#if enterprise && !enterprise?.isTemporary}
            <div class="info">
                <h2 class="infoTitle separator">Entreprise:</h2>
                <div class="form-group-vertical">
                    <label class="infoTitle" for="title">Nom*</label>
                    <p>{enterprise.name}</p>
                </div>
                <div class="form-group-vertical">
                    <label class="infoTitle" for="schedule">Adresse*</label>
                    <p>{enterprise.address}</p>
                </div>
                <div class="form-group-vertical">
                    <label class="infoTitle" for="lieu">Courriel*</label>
                    <p>{enterprise.email}</p>
                </div>
                <div class="form-group-vertical">
                    <label class="infoTitle" for="lieu">Téléphone*</label>
                    <p>{enterprise.phone}</p>
                </div>
                <div class="form-group-vertical">
                    <label class="infoTitle" for="lieu">Ville*</label>
                    <p>{selectedCity[0].label}</p>
                </div>
            </div>
            <br>
            {/if}
            
        <div class="info">
            <h2 class="infoTitle separator">Offre:</h2>
            <h5 class="infoTitle">Nom du poste</h5>
            <p class="text">{offer.title}</p>
            <h5 class="infoTitle">Adresse du lieu de travail</h5>
            <p class="text">{offer.address}</p>
            <h5 class="infoTitle">Date de début</h5>
            <p class="text">{offer.offerDebut}</p>
            <h5 class="infoTitle">Date d'entrée en fonction</h5>
            <p class="text">{offer.dateEntryOffice}</p>
            <h5 class="infoTitle">Date limite pour postuler</h5>
            <p class="text">{offer.deadlineApply}</p>
            <h5 class="infoTitle">Salaire</h5>
            <p class="text">{offer.salary}</p>
            <h5 class="infoTitle">Heure par semaine</h5>
            <p class="text">{offer.hoursPerWeek}</p>
            <h5 class="infoTitle">Programme</h5>
            <p class="text">{programmeSelected.map((p) => p.label).join(", ")}</p>
            <h5 class="infoTitle">Type du poste</h5>
            <p class="text">{scheduleSelected.map((s) => s.label).join(", ")}</p>
            <h5 class="infoTitle">Description du poste</h5>
            <p class="text">{offer.description}</p>
            <h5 class={hideURL ? "infoTitle CanBeHidden" : "infoTitle"}>Adresse URL vers l'offre d'emploi détaillé</h5>
            <p class={hideURL ? "text CanBeHidden" : "text"}>{offer.offerLink}</p>
            <h5 class="infoTitle">Où envoyer votre candidature</h5>
            <p class="text">{offer.email}</p>
    
            <style scoped>
                .CanBeHidden 
                {
                    display: none;
                }
    
                .container > .Loading2 
                {
                    display: flex !important;
                    justify-content: center !important;
                }
            </style>
        </div>
    {/if}

</div>

<style scoped>
    .titleContainer {
        display: flex;
        flex-direction: column;
    }
    .title {
        font-size: 2.5rem;
        color: #00ad9a;
        margin: 0px;
        margin-bottom: 1.5vw;
    }
    .subtitle {
        font-size: 1.5rem;
        margin: 0px;
        margin-bottom: 2.25vw;
        color: black;
    }
    .infoTitle {
        font-size: 1.3rem;
        margin: 0px;
        margin-bottom: 0.5vw;
    }
    .info {
        color: black;
    }
    .text {
        font-size: 1.1rem;
        margin: 0px;
        margin-bottom: 1.75vw;
        color: black;
    }
    .container {
        width: 95%;
        display: flex;
        flex-direction: column;
        text-align: left;
        justify-content: space-between;
        color: white;
        border-radius: 4px;
        transition: background-color 0.3s ease;
        max-height: 40vh;
        overflow-y: auto;
    }

    .separator {
        color: #00ad9a;
    }
</style>
