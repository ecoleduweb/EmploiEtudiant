<script>
    import "../styles/font.css"
    import Header from "../Components/Common/Header.svelte"
    import CookieBanner from "../Components/Common/CookieBanner.svelte"
    import Footer from "../Components/Common/Footer.svelte"
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