<script lang="ts">
    import { onMount } from "svelte"
    import LoadingSpinner from "../Common/LoadingSpinner.svelte"
    import fetchCity from "../../Service/CityService"
    import type { JobOfferDetails } from "../../Models/JobOfferDetails"
    import Button from "../Inputs/Button.svelte"
    import { copy } from "svelte-copy"
    import { formatPhoneNumber, getShortURL } from "../../ts/utils"

    // import { WhatsApp } from "svelte-share-buttons-component"
    export let offer: JobOfferDetails

    let hideURL = offer.offerLink == "https://" || offer.offerLink == "http://"
    let cityOptions: any
    let selectedCity: any
    let loaded = false
    let formattedPhone: string

    let url = ""
    let fullUrl = ""
    let title = ""
    let desc = ""
    let showShareModal = false

    const openShareModal = async () => {
        showShareModal = true
    }

    const closeShareModal = async () => {
        showShareModal = false
    }

    onMount(async () => {
        cityOptions = await fetchCity()
        if (offer && offer.enterprise && offer.enterprise.phone) {
            formattedPhone = formatPhoneNumber(offer.enterprise.phone)
        }
        if (offer && offer.offerLink) {
            fullUrl = offer.offerLink
            url = getShortURL(offer.offerLink)
        }
        title = offer.title
        desc = offer.description
        loaded = true
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
                    <h5 class="infoTitle">Nom*</h5>
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
            <br />
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
            <p class="text">
                {offer.studyPrograms?.map((p) => p.name).join(", ")}
            </p>
            <h5 class="infoTitle">Poste visé</h5>
            <p class="text">
                {offer.schedules?.map((s) => s.description).join(", ")}
            </p>
            <h5 class="infoTitle">Description du poste</h5>
            <div class="description">{@html offer.description}</div>
            <h5 class={hideURL ? "infoTitle CanBeHidden" : "infoTitle"}>
                Lien vers l'offre d'emploi détaillée
            </h5>
            <div class="row-copy">
                {#if !hideURL}
                    <div class="link_padding">
                        <a href={offer.offerLink} class="text_link">{url}</a>
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
                <div class="share-button-wrapper">
                    <Button text="Partager" onClick={openShareModal} />
                </div>
            </div>
        </div>
    {/if}
</div>

<!-- Modal de partage -->
{#if showShareModal}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <div class="modal-overlay" on:click={closeShareModal}>
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <div class="modal-content" on:click|stopPropagation>
            <div class="modal-header">
                <h3>Partager l'offre</h3>
                <button
                    class="close-btn"
                    on:click={closeShareModal}
                    aria-label="Fermer">&times;</button
                >
            </div>
          
            </div>
        </div>

{/if}

<style scoped>
    .CanBeHidden {
        display: none;
    }

    .container > .Loading2 {
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
    .description {
        border-left: 1px solid #555;
        padding-left: 1vw;
    }
    .text_link {
        font-size: 1.1rem;
        bottom: 2vh;
        color: #00ad9a;
        margin-bottom: 1.75vw;
    }
    .container {
        width: 100%;
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

    /* Styles de la modale */
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }

    .modal-content {
        background-color: white;
        border-radius: 8px;
        padding: 2rem;
        max-width: 500px;
        width: 90%;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .modal-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
        color: #00ad9a;
    }

    .modal-header h3 {
        margin: 0;
        font-size: 1.5rem;
    }

    .close-btn {
        background: none;
        border: none;
        font-size: 2rem;
        cursor: pointer;
        color: #555;
        padding: 0;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .close-btn:hover {
        color: #00ad9a;
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
        .modal-content {
            padding: 1.5rem;
            width: 95%;
        }
        .modal-header h3 {
            font-size: 1.2rem;
        }
     
        .share-button-wrapper :global(.button) {
            padding: 8px 12px;
            font-size: 14px;
        }
    }
</style>
