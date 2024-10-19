<script lang="ts">
    import { onMount } from "svelte"
    import LoadingSpinner from "../Common/LoadingSpinner.svelte";
    import fetchCity from "../../Service/CityService"
    import type { JobOfferDetails } from "../../Models/JobOfferDetails"
    import Button from "../Inputs/Button.svelte"
    import { copy } from 'svelte-copy';
    import { formatPhoneNumber, getShortURL } from "../../ts/utils"
    
    export let offer: JobOfferDetails

    let hideURL = offer.offerLink == "https://" || offer.offerLink == "http://";
    let cityOptions: any;
    let selectedCity: any;
    let loaded = false;
    let formattedPhone: string;
    let url = '';

    onMount(async () => {
        cityOptions = await fetchCity()
        if (offer && offer.enterprise && offer.enterprise.phone) {
            formattedPhone = formatPhoneNumber(offer.enterprise.phone);
        }
        if (offer && offer.offerLink) {
            // Vérifiez si l'utilisateur est sur un appareil mobile
                url = getShortURL(offer.offerLink);
        }
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
            <h5 class="infoTitle">Numéro de téléphone</h5>
            <p class="text">{formattedPhone}</p>
            <h5 class="infoTitle">Date de publication</h5>
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
            <h5 class={hideURL ? "infoTitle CanBeHidden" : "infoTitle"}>Lien vers l'offre d'emploi détaillée</h5>
            <div class="row-copy">
                {#if !hideURL}
                    <div class="link_padding">
                        <a href="{offer.offerLink}" class="text_link">{url}</a>
                    </div>
                {:else}
                    <p class="text CanBeHidden">{url}</p>
                {/if} 
                <div use:copy={offer.offerLink}>
                    <img class="iconeCopy" src="copy.svg" alt="Edit icon" />
                </div>
            </div>
            <h5 class="infoTitle">Où envoyer votre candidature</h5>
            <div class="row">
                <p class="text">{offer.email}</p> 
                    <a href="mailto:{offer.email}">
                        <Button text="Postuler par courriel" />
                    </a>
            </div>
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
    .text_link
    {
        font-size: 1.1rem;
        bottom: 2vh;
        color: #00ad9a;
        margin-bottom: 1.75vw;
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
    .row {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        width: 90%;
    }
    .row-copy {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        width: 90%;
    }
    .link_padding {
        display: flex;
        flex-direction: row;
    }
    .iconeCopy {
        width: 1.5vw;
        height: 1.5vw;
        cursor: pointer;
    }

    .iconeCopy:hover {
        filter: invert(0.05);
    }

    @media (max-width: 768px) {
        .row {
            flex-direction: column;
            height: 9vh;
        }
        .container {
            max-height: 60vh;
        }
        .iconeCopy {
            width: 5vw;
            height: 5vw;
        }
        .row-copy {
            flex-direction: row;
            height: 4vh;
        }
    }
</style>
