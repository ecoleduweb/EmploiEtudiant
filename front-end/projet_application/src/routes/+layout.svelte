<script>
    import "../styles/font.css"
    import Header from "../Components/Common/Header.svelte"
    import CookieBanner from "../Components/Common/CookieBanner.svelte"
    import Footer from "../Components/Common/Footer.svelte"
</script>



<Header/>
<CookieBanner />

<slot />

<div class="FooterDiv">
    <Footer/>
</div>

<style lang="scss" scoped>
    .FooterDiv 
    {
        position: fixed;
        bottom: 0;
        min-width: 100%;
    }
</style>