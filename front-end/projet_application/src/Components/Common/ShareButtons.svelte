<script lang="ts">
    import {
        LinkedIn,
        WhatsApp,
        X,
        Email,
        //@ts-ignore
    } from "svelte-share-buttons-component"

    interface Props {
        shareUrl: string
        shareText: string
        title: string
    }

    let { shareUrl, shareText, title }: Props = $props()

    let isIOS = $derived(
        typeof navigator !== "undefined" &&
            /iPad|iPhone|iPod/.test(navigator.userAgent),
    )

    let smsHref = $derived(
        isIOS
            ? `sms:&body=${encodeURIComponent(shareText)}`
            : `sms:?body=${encodeURIComponent(shareText)}`,
    )

    let messengerShare = $derived(
        `fb-messenger://share?link=${encodeURIComponent(shareUrl)}`,
    )
</script>

<div class="shareInlineBlock">
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
    </div>
</div>

<style scoped>
    .infoTitle {
        font-size: 1.3rem;
        margin: 0px;
        margin-bottom: 0.5vw;
    }

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
        .infoTitle {
            margin-bottom: 0.5rem;
        }

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
