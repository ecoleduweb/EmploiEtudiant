<script>
    import "../styles/font.css"
    import Header from "../Components/Common/Header.svelte"
    import CookieBanner from "../Components/Common/CookieBanner.svelte"
    import Footer from "../Components/Common/Footer.svelte"
    import { ClientTelemetry } from "$lib/tracer"
    import { env } from "$env/dynamic/public"
    let { children } = $props();

    const ENABLED_TELEMETRY = env.PUBLIC_ENABLED_TELEMETRY

    if (ENABLED_TELEMETRY) {
        const telemetry = ClientTelemetry.getInstance()
        telemetry.start()
    }
</script>

<div class="container">
    <Header/>
    <CookieBanner />

    <main class="content">
        {@render children?.()}
    </main>

    <div class="footer-spacer"></div>
    <Footer/>
</div>

<style lang="scss" scoped>
    .container {
        display: flex;
        flex-direction: column;
    }
    .content {
        flex: 1;
    }
    .footer-spacer {
        height: 3.01vw;
    }
</style>
