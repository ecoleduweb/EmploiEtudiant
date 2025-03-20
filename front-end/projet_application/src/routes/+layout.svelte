<script>
    import "../styles/font.css"
    import Header from "../Components/Common/Header.svelte"
    import CookieBanner from "../Components/Common/CookieBanner.svelte"
    import Footer from "../Components/Common/Footer.svelte"
    import { ClientTelemetry } from "$lib/tracer"
    const ENABLED_TELEMETRY = import.meta.env.VITE_ENABLED_TELEMETRY || true //Garder à false en développement local

    if (ENABLED_TELEMETRY) {
        const telemetry = ClientTelemetry.getInstance()
        telemetry.start()
    }
</script>

<Header />
<CookieBanner />

<slot />

<div class="FooterDiv">
    <Footer />
</div>

<style lang="scss" scoped>
    .FooterDiv {
        position: fixed;
        bottom: 0;
        min-width: 100%;
    }
</style>
