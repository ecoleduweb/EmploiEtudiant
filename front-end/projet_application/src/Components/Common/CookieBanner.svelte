<script>
    import { onMount } from "svelte"
    import Analytic from "../../lib/analytic.svelte"
    import { env } from "$env/dynamic/public"
    import { GoogleAnalytics } from '@beyonk/svelte-google-analytics'

    let accepted = false
    const measurementId = env.PUBLIC_PUBLIC_MEASUREMENT_ID;

    function acceptCookies() {
        accepted = true
        localStorage.setItem("cookieConsent", "accepted")
    }

    onMount(() => {
        if (localStorage.getItem("cookieConsent") === "accepted") {
            accepted = true
        }
    })
</script>

{#if !accepted}
    <div class="cookie-banner">
        <p>
            Nous utilisons les témoins de connexion (cookies) à des fins
            statistiques et promotionnelles en vue d'améliorer l'expérience de
            navigation. Nous sommes engagés à protéger votre vie privée avec la
            même rigueur que celle avec laquelle nous nous acquittons de notre
            mission d’enseignement. En utilisant le site web du Cégep de
            Rivière-du-Loup, vous acceptez que celui-ci dépose des témoins sur
            votre appareil. <a
                href="https://www.cegeprdl.ca/grand-public/confidentialite-et-vie-privee"
                >En savoir plus</a
            >.
        </p>
        <button id="cookieBannerOk" on:click={acceptCookies}>J'ai compris</button>
    </div>
{/if}

{#if accepted}

    <Analytic />
    <GoogleAnalytics properties={[measurementId]} />
{/if}

<style>
    .cookie-banner {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 99%;
        background-color: #333;
        color: #fff;
        padding: 10px;
        text-align: center;
        z-index: 1;
    }

    .cookie-banner a {
        color: #fff;
        text-decoration: underline;
    }

    .cookie-banner button {
        background-color: #fff;
        color: #333;
        border: none;
        padding: 8px 16px;
        cursor: pointer;
        margin-left: 10px;
    }
</style>
