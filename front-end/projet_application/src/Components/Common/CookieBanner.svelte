<script>
    import { onMount } from "svelte"
    import { env } from "$env/dynamic/public"

    let accepted = false

    function initializeGoogleAnalytics() {
        const measurementId = env.PUBLIC_MEASUREMENT_ID
        if (!measurementId) {
            return
        }
        // @ts-ignore
        window.dataLayer = window.dataLayer || []
        function gtag() {
            // @ts-ignore
            dataLayer.push(arguments)
        }
        gtag("js", new Date())
        gtag("config", measurementId)
    }

    function acceptCookies() {
        accepted = true
        localStorage.setItem("cookieConsent", "accepted")
        initializeGoogleAnalytics()
    }

    onMount(() => {
        if (localStorage.getItem("cookieConsent") === "accepted") {
            initializeGoogleAnalytics()
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
        <button on:click={acceptCookies}>J'ai compris</button>
    </div>
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
