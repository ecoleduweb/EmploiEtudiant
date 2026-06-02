<script lang="ts">
    import { page } from "$app/state"
    import { env } from "$env/dynamic/public"

    const measurementId: string | undefined = env.PUBLIC_PUBLIC_MEASUREMENT_ID

    $effect(() => {
        if (typeof gtag === "undefined") {
            console.warn("gtag is not defined")
            return
        }
        if (!measurementId) {
            console.warn("measurementId is not defined")
            return
        }
        gtag("config", measurementId, {
            page_title: document.title,
            page_path: $page.url.pathname,
        })
    })
</script>

<svelte:head>
    <script
        async
        src={`https://www.googletagmanager.com/gtag/js?id=${measurementId}`}
    >
    </script>
    <script>
        window.dataLayer = window.dataLayer || []

        function gtag() {
            dataLayer.push(arguments)
        }

        gtag("js", new Date())
    </script>
</svelte:head>
