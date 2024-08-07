<script lang="ts">
    import { onMount } from "svelte"
    import LoadingSpinner from "../Common/LoadingSpinner.svelte";
    import fetchCity from "../../Service/CityService"
    import type { JobOfferDetails } from "../../Models/JobOfferDetails"
    
    export let offer: JobOfferDetails

    let hideURL = offer.offerLink == "https://" || offer.offerLink == "http://";
    let cityOptions: any;
    let selectedCity: any;
    let loaded = false;

    onMount(async () => {
        cityOptions = await fetchCity()
        loaded = true;
    })


    $: if (cityOptions) {
        const city = cityOptions.find(
            (ville: any) => ville.value === offer?.enterprise?.cityId,
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
            {#if offer.enterprise}
                <h4 class="subtitle">Chez {offer.enterprise.name}</h4>
            {/if}
        </div>

        {#if offer.enterprise && offer.enterprise?.isTemporary}
            <div class="info">
                <h2 class="infoTitle separator">Entreprise:</h2>
                <div class="form-group-vertical">
                    <h5 class="infoTitle" >Nom*</h5>
                    <p>{offer.enterprise.name}</p>
                </div>
                <div class="form-group-vertical">
                    <h5 class="infoTitle">Adresse*</h5>
                    <p>{offer.enterprise.address}</p>
                </div>
                <div class="form-group-vertical">
                    <h5 class="infoTitle">Courriel*</h5>
                    <p>{offer.enterprise.email}</p>
                </div>
                <div class="form-group-vertical">
                    <h5 class="infoTitle">Téléphone*</h5>
                    <p>{offer.enterprise.phone}</p>
                </div>
                <div class="form-group-vertical">
                    <h5 class="infoTitle">Ville*</h5>
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
            <p class="text">{offer.studyPrograms?.map((p) => p.name).join(", ")}</p>
            <h5 class="infoTitle">Type du poste</h5>
            <p class="text">{offer.schedules?.map((s) => s.description).join(", ")}</p>
            <h5 class="infoTitle">Description du poste</h5>
            <p class="text">{offer.description}</p>
            <h5 class={hideURL ? "infoTitle CanBeHidden" : "infoTitle"}>Adresse URL vers l'offre d'emploi détaillé</h5>
            <p class={hideURL ? "text CanBeHidden" : "text"}>{offer.offerLink}</p>
            <h5 class="infoTitle">Où envoyer votre candidature</h5>
            <p class="text">{offer.email}</p>
    
        </div>
    {/if}

</div>

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
        margin-bottom: 2vw;
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
