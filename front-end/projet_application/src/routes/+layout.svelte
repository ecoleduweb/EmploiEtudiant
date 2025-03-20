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

<div class="container">
    <Header/>
    <CookieBanner />

    <main class="content">
        <slot />
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
