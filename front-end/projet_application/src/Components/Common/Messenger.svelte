<script lang="ts">
    import ShareButton from "./ShareButton.svelte"
    import type { HTMLAnchorAttributes } from "svelte/elements"

    interface Props
        extends Omit<
            HTMLAnchorAttributes,
            "class" | "href" | "target" | "rel" | "aria-label"
        > {
        url: string
        ariaLabel?: string
        class?: string
    }

    export let url: string
    export let ariaLabel: string = "Share on Messenger"
    let classes: string = ""
    export { classes as class }

    // Use native Messenger deep link on mobile, otherwise fall back to Facebook share dialog
    $: href = encodeURI(
        typeof navigator !== "undefined" &&
            /Android|iPhone|iPad|iPod|IEMobile|Opera Mini/i.test(
                navigator.userAgent,
            )
            ? `fb-messenger://share/?link=${url}`
            : `https://www.facebook.com/dialog/send?link=${url}&app_id=&redirect_uri=${url}`,
    )
</script>

<div class="ssbc-button--messenger {classes}">
    <ShareButton {ariaLabel} {href}>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path
                d="M12 0C5.373 0 0 4.975 0 11.111c0 3.497 1.745 6.616 4.472 8.652V24l4.086-2.242c1.09.301 2.246.464 3.442.464 6.627 0 12-4.974 12-11.111C24 4.975 18.627 0 12 0zm1.193 14.963l-3.056-3.259-5.963 3.259L10.732 8l3.13 3.259L19.752 8l-6.559 6.963z"
            />
        </svg>
    </ShareButton>
</div>

<style>
    :global(.ssbc-button--messenger) {
        background-color: #0084ff;
    }

    :global(.ssbc-button--messenger:active),
    :global(.ssbc-button--messenger:hover) {
        background-color: #0066cc;
    }
</style>
