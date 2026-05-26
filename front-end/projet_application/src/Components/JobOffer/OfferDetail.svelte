<script lang="ts">
    import { onMount } from "svelte"
    import LoadingSpinner from "../Common/LoadingSpinner.svelte"
    import fetchCity from "../../Service/CityService"
    import type { JobOfferDetails } from "../../Models/JobOfferDetails"
    import Button from "../Inputs/Button.svelte"
    import { copy } from "svelte-copy"
    import {
        formatPhoneNumber,
        getShortURL,
        toFormattedDateString,
    } from "../../ts/utils"
    import { page } from "$app/state"
    import ShareButtons from "../Common/ShareButtons.svelte"

    interface Props {
        offer: JobOfferDetails
        showShareButtons?: boolean
    }

    let { offer, showShareButtons = false }: Props = $props()

    let hideURL = $derived(
        !offer.offerLink ||
            offer.offerLink === "https://" ||
            offer.offerLink === "http://",
    )

    let cityOptions: any = $state()
    let selectedCity: any = $state()
    let loaded = $state(false)

    let formattedPhone: string = $state("")
    let url = $state("")

    let shareUrl = page.url.href

    let title = $derived(offer.title)
    let shareText = $derived(` ${shareUrl} ${title}`.trim())

    onMount(async () => {
        cityOptions = await fetchCity()

        if (offer.enterprise?.phone) {
            formattedPhone = formatPhoneNumber(offer.enterprise.phone)
        }
        url = await getShortURL(offer.offerLink)

        loaded = true
    })

    $effect(() => {
        if (!cityOptions) return

        const city = cityOptions.find(
            (ville: any) => ville.value === offer?.enterprise?.cityId,
        )

        if (city) selectedCity = [city]
    })
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
                    <p>{selectedCity?.[0]?.label ?? ""}</p>
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
            <p class="text">{toFormattedDateString(offer.offerDebut)}</p>

            <h5 class="infoTitle">Date d'entrée en fonction</h5>
            <p class="text">{toFormattedDateString(offer.dateEntryOffice)}</p>

            <h5 class="infoTitle">Date limite pour postuler</h5>
            <p class="text">{toFormattedDateString(offer.deadlineApply)}</p>
            <h5 class="infoTitle">Types d'emploi</h5>
            <p class="text">
                {offer.employmentSchedules
                    ?.map((s) => s.description)
                    .join(", ")}
            </p>
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
                    <img
                        class="iconeCopy"
                        src="copy.svg"
                        alt="Copier le lien"
                    />
                </div>
            </div>

            <h5 class="infoTitle">Où envoyer votre candidature</h5>
            <div class="row">
                <p class="text">{offer.email}</p>
                <a href="mailto:{offer.email}">
                    <Button text="Postuler par courriel" />
                </a>
            </div>
            {#if showShareButtons && !hideURL}
                <ShareButtons {shareUrl} {shareText} {title} />
            {/if}
        </div>
    {/if}
</div>

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
        gap: 0.75rem;
        align-items: center;
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

    :global(.shareCell .ssbc-button__link),
    :global(.shareCell .ssbc-button__icon) {
        display: inline-block;
    }

    :global(.shareGrid .shareCell .ssbc-button__link) {
        display: flex;
        width: 100%;
        height: 100%;
        text-decoration: none;
        color: #fff;
    }

    :global(.shareGrid .shareCell .ssbc-button) {
        transition: 25ms ease-out;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 100%;
        box-sizing: border-box;

        margin: 0;
        border-radius: 0;
    }

    :global(.shareCell .ssbc-button__icon svg) {
        width: 1em;
        height: 1em;
        margin: 0;
        vertical-align: middle;
    }

    :global(.shareCell .ssbc-button__icon--fill) {
        fill: #fff;
        stroke: none;
    }

    :global(.shareCell .ssbc-button__icon--outline) {
        fill: none;
        stroke: #fff;
    }

    @media (max-width: 768px) {
        .row {
            flex-direction: column;
            height: auto;
            width: 100%;
            gap: 0.75rem;
            align-items: flex-start;
        }

        .container {
            max-height: 60vh;
        }

        .infoTitle {
            margin-bottom: 0.5rem;
        }

        .text {
            margin-bottom: 0.75rem;
        }

        .iconeCopy {
            width: 5vw;
            height: 5vw;
        }

        .row-copy {
            flex-direction: row;
            height: auto;
            width: 100%;
            align-items: center;
        }
    }
</style>
