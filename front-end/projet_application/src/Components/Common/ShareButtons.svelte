<script lang="ts">
    import {
        LinkedIn,
        WhatsApp,
        X,
        Email,
        //@ts-ignore
    } from "svelte-share-buttons-component"
    import { env } from "$env/dynamic/public"

    interface Props {
        title: string
    }

    const appId = env.PUBLIC_MESSENGER_APP_ID

    let { title }: Props = $props()

    const shareUrl = $derived(
        typeof window !== "undefined" ? window.location.href : ""
    )

    let isIOS = $derived(
        typeof navigator !== "undefined" &&
            /iPad|iPhone|iPod/.test(navigator.userAgent),
    )

    let smsHref = $derived(
        isIOS
            ? `sms:&body=${encodeURIComponent(title)}`
            : `sms:?body=${encodeURIComponent(title)}`,
    )
    const isOnMobile = $derived(
        typeof navigator !== "undefined" &&
            /Mobi|Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
                navigator.userAgent,
            ),
    )

    let messengerShareLink = $derived(
        isOnMobile
            ? `fb-messenger://share?link=${encodeURIComponent(shareUrl)}`
            : `https://www.facebook.com/share_as_message/?link=${encodeURIComponent(shareUrl)}&app_id=${appId}`,
    )

    const text = $derived(
        `J'ai trouvé cette offre sur le site d'emploi étudiant : ${title}.`,
    )
    const textWithUrl = $derived(
        `${text} Voici le lien pour t'y rendre : ${shareUrl}`,
    )
</script>

<div class="shareInlineBlock">
    <div class="shareGrid">
        <div class="shareCell">
            <WhatsApp url={shareUrl} {text} />
        </div>

        <div class="shareCell">
            <LinkedIn url={shareUrl} />
        </div>

        <div class="shareCell">
            <X url={shareUrl} {text} />
        </div>

        <div class="shareCell">
            <Email subject={title} body={textWithUrl} />
        </div>

        <a
            class="shareCell messengerItem"
            href={messengerShareLink}
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

        {#if isOnMobile}
            <a
                class="shareCell smsItem"
                href={smsHref}
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
        {/if}
    </div>
</div>

<style scoped>
    .shareInlineBlock {
        margin-top: 1rem;
        width: 100%;
    }

    .shareGrid {
        display: grid;
        grid-template-columns: repeat(3, 4em);
        gap: 10px;
        justify-content: center;
        margin: 0 auto;
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
        .shareInlineBlock {
            width: 100%;
            margin-top: 1.25rem;
        }

        .shareGrid {
            grid-template-columns: repeat(3, 4em);
            justify-content: center;
        }
    }
</style>
