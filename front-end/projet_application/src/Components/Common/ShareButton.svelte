<script lang="ts">
    import type { HTMLAnchorAttributes } from "svelte/elements"

    interface Props
        extends Omit<
            HTMLAnchorAttributes,
            "class" | "href" | "target" | "rel" | "aria-label"
        > {
        href: string
        label?: string
        fill?: boolean
        ariaLabel?: string
        class?: string
    }

    export let href: string
    export let label: string = ""
    export let fill: boolean = true
    export let ariaLabel: string = ""
    let classes: string = ""
    export { classes as class }
</script>

<a
    class="ssbc-button__link"
    {href}
    target="_blank"
    rel="noopener noreferrer"
    aria-label={ariaLabel}
>
    <div class="ssbc-button {classes}">
        <div
            aria-hidden="true"
            class="ssbc-button__icon"
            class:ssbc-button__icon--fill={fill}
            class:ssbc-button__icon--outline={!fill}
        >
            <slot />
        </div>
        {label}
    </div>
</a>

<style>
    .ssbc-button__link,
    .ssbc-button__icon {
        display: inline-block;
    }

    .ssbc-button__link {
        text-decoration: none;
        color: #fff;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }

    .ssbc-button__link:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }

    .ssbc-button__link:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    .ssbc-button {
        transition: all 0.3s ease;
        padding: 0.75em;
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 48px;
        min-height: 48px;
    }

    .ssbc-button__icon :global(svg) {
        width: 1.5em;
        height: 1.5em;
        margin: 0;
        vertical-align: middle;
        filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
    }

    .ssbc-button__icon :global(img) {
        width: 1.5em;
        height: 1.5em;
        margin: 0;
        vertical-align: middle;
        filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
    }

    .ssbc-button__icon--fill {
        fill: #fff;
        stroke: none;
    }

    .ssbc-button__icon--outline {
        fill: none;
        stroke: #fff;
    }
</style>
