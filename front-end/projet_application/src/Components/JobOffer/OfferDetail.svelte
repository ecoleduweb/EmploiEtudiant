<script lang="ts">
    import { onMount } from "svelte"
    import LoadingSpinner from "../Common/LoadingSpinner.svelte"
    import fetchCity from "../../Service/CityService"
    import type { JobOfferDetails } from "../../Models/JobOfferDetails"
    import Button from "../Inputs/Button.svelte"
    import { copy } from "svelte-copy"
    import { formatPhoneNumber, getShortURL } from "../../ts/utils"
    // @ts-ignore
    import { WhatsApp } from "svelte-share-buttons-component"
    // @ts-ignore
    import { LinkedIn } from "svelte-share-buttons-component"
    // @ts-ignore
    import { X } from "svelte-share-buttons-component"
    // @ts-ignore
    import { Email } from "svelte-share-buttons-component"

    interface Props {
        offer: JobOfferDetails
    }

    let { offer }: Props = $props()

    let hideURL = $derived(
        offer.offerLink === "https://" || offer.offerLink === "http://",
    )

    let cityOptions: any = $state()
    let selectedCity: any = $state()
    let loaded = $state(false)

    let formattedPhone: string = $state("")

    let url = $state("")

    let shareUrl = $derived((offer?.offerLink ?? "").trim())
    let title = $derived(offer?.title ?? "Offre d’emploi")
    let shareText = $derived(`${title} ${shareUrl}`.trim())
    let messengerShare = $derived(
        `fb-messenger://share?link=${encodeURIComponent(shareUrl)}`,
    )

    onMount(async () => {
        cityOptions = await fetchCity()

        if (offer?.enterprise?.phone) {
            formattedPhone = formatPhoneNumber(offer.enterprise.phone)
        }

        if (offer?.offerLink) {
            url = getShortURL(offer.offerLink)
        }

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
            {#if !hideURL}
                <div class="shareInlineBlock">
                    <h5 class="infoTitle">Partager cette offre</h5>
                    <div class="shareGrid">
                        <div class="shareCell">
                            <WhatsApp url={shareUrl} text={shareText} />
                        </div>

                        <div class="shareCell">
                            <LinkedIn url={shareUrl} />
                        </div>

                        <div class="shareCell">
                            <X url={shareUrl} text={shareText} />
                        </div>

                        <div class="shareCell">
                            <Email subject={title} body={shareText} />
                        </div>

                        <a
                            class="shareCell messengerItem"
                            href={messengerShare}
                            aria-label="Partager sur Messenger"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="2em"
                                height="2em"
                                viewBox="0 0 24 24"
                                fill="white"
                            >
                                <path
                                    d="M12 2C6.477 2 2 6.145 2 11.259c0 2.821 1.323 5.338 3.405 7.01V21l2.933-1.608C9.234 19.783 10.594 20 12 20c5.523 0 10-4.145 10-9.259S17.523 2 12 2zm1.006 12.57l-2.545-2.716-4.97 2.716 5.472-5.81 2.602 2.716 4.913-2.716-5.472 5.81z"
                                />
                            </svg>
                        </a>

                        <a
                            class="shareCell smsItem"
                            href={`sms:?body=${encodeURIComponent(shareText)}`}
                            aria-label="Partager par SMS"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="2em"
                                height="2em"
                                viewBox="0 0 24 24"
                                fill="white"
                            >
                                <path
                                    d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm0 14H6l-2 2V4h16v12z"
                                />
                            </svg>
                        </a>
                    </div>
                </div>
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

    .shareInlineBlock {
        margin-top: 1rem;
        width: fit-content;
    }

    .shareGrid {
        display: grid;
        grid-template-columns: repeat(3, 4em);
        gap: 10px;
    }

    .shareCell {
        width: 4em;
        height: 4em;
        border-radius: 10px;
        overflow: hidden;
        transition: transform 0.15s ease;
        display: flex;
        justify-content: center;
        align-items: center;
        text-decoration: none;
        flex-shrink: 0;
    }

    .shareCell:hover {
        transform: scale(1.05);
    }

    .messengerItem {
        background: linear-gradient(135deg, #c026d3, #7c3aed, #2563eb);
    }
    .smsItem {
        background: #4caf50;
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

        .shareInlineBlock {
            width: 100%;
            margin-top: 1.25rem;
        }

        .shareGrid {
            grid-template-columns: repeat(3, 4em);
            justify-content: start;
        }
    }
</style>
