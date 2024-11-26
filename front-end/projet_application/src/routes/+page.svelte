<script lang="ts">
    import "../styles/global.css"
    import Button from "../Components/Inputs/Button.svelte"
    import { goto } from "$app/navigation"
    import LoadingSpinner from "../Components/Common/LoadingSpinner.svelte"
    import DetailOfferRow from "../Components/JobOffer/DetailOfferRow.svelte"
    import { GET } from "../ts/server"
    import { onMount } from "svelte"
    import type { JobOfferDetails } from "../Models/JobOfferDetails"

    let loaded = false
    let latestJobOffers: JobOfferDetails[] = []
    
    onMount(async () => {
        try 
        {
            latestJobOffers = await GET<JobOfferDetails[]>("/jobOffer/approved?getRecentOnly=true&entrepriseDetails=true&employmentScheduleDetails=true&studyProgramDetails=true")
        }
        catch (error) 
        {
            console.error("Error while loading the page", error)
        }
        finally
        {
            loaded = true
        }
    })

    const handleEmploi = () => {
        goto("/emplois")
    }

    const handleEmploiWithId = (id: number) => {
        goto(`/emplois?id=${id}`)
    }
</script>

<main>
    <section class="haut">
        <div class="haut-gauche">
            <h1 class="title">
                <span class="text">PORTAIL D'</span><span class="text"
                    >OFFRES D'EMPLOI</span
                >
            </h1>
            <h2 class="text mb">DU CÉGEP DE RIVIÈRE-DU-LOUP</h2>
            <p class="text-welcome">Bienvenue sur le portail d'offres d'emploi du Cégep!
                 En collaboration avec des étudiants en Techniques de l'informatique et sous la responsabilité de l'enseignant Antoine Chagnon-Michaud,
                  le Cégep de Rivière-du-Loup a développé un nouveau Portail d'offres d'emploi. Celui-ci a pour objectif d'afficher 
                  les offres d'emploi destinées à nos élèves actuels ou qui ont obtenu leur diplôme récemment.
                  Veuillez noter que les entreprises sont responsables de la qualité du français dans leurs offres d'emploi respectives.</p>
            <span class="radiant"></span>
        </div>

        <!-- ------------SECTION MOBILE DEBUT ----------- -->
        <div class="haut-mobile">
            <h1 class="title">
                <span class="text">PORTAIL D'</span><span class="text"
                    >OFFRES D'EMPLOI</span
                >
            </h1>
            <h2 class="text mb">DU CÉGEP DE RIVIÈRE-DU-LOUP</h2>
            <p class="text-welcome">Bienvenue sur le portail d'offres d'emploi du Cégep!
                En collaboration avec des étudiants en Techniques de l'informatique et sous la responsabilité de l'enseignant Antoine Chagnon-Michaud,
                 le Cégep de Rivière-du-Loup a développé un nouveau Portail d'offres d'emploi. Celui-ci a pour objectif d'afficher 
                 les offres d'emploi destinées à nos élèves actuels ou qui ont obtenu leur diplôme récemment.
                 Veuillez noter que les entreprises sont responsables de la qualité du français dans leurs offres d'emploi respectives.</p>

            <span class="radiant"></span>
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <!-- svelte-ignore a11y-no-static-element-interactions -->
                <div class="divButton" on:click={handleEmploi}>
                    <Button
                        
                        text="Consulter toutes les offres"
                        onClick={() => ""}
                    />
                </div>
        </div>
        <!-- ---------SECTION MOBILE FIN ------------ -->

        <div class="haut-droite">
            <div class="buttonDiv">
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <!-- svelte-ignore a11y-no-static-element-interactions -->
                <div class="divFlex" on:click={handleEmploi}>
                    <Button
                        text="Consulter toutes les offres"
                        onClick={() => ""}
                    />
                </div>
            </div>
        </div>
    </section>

    {#if !loaded}
        <section class="Loading">
            <LoadingSpinner />
        </section>
    {:else}
        <section class="offres">
            {#each latestJobOffers as offer}
                <DetailOfferRow {offer} 
                handleModalClick={(function() {handleEmploiWithId(offer.id)})}/>
            {/each}
        </section>
    {/if}
    
    <style scoped>
        .Loading 
        {
            height: 100%;
            width: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
            position: fixed;
        }
    </style>

</main>

<style scoped>
    main {
        height: 80%;
    }
    h2 {
        color: white;
    }
    .title {
        left: 7.2%;
        margin: 0;
        margin-top: 30px;
    }
    .title span:first-child {
        color: white;
        margin: 0;
    }
    .title span:last-child {
        color: #00ad9a;
        margin: 0;
    }
    .text {
        font-size: 2.5vw;
        margin: 0;
    }
    .mb {
        margin-bottom: 30px;
    }
    main {
        display: flex;
        flex-direction: column;
        width: 100%;
    }
    .haut {
        display: flex;
        widows: 85%;
    }
    .haut-gauche {
        display: flex;
        flex-direction: column;
        width: 100%;
        margin-left: 5.2%;
    }
    .haut-mobile {
        display: none;
    }
    .haut-droite {
        width: 60%;
        display: flex;
        justify-content: flex-end;
        align-items: flex-end;
    }
    .buttonDiv {
        display: flex;
        width: 50%;
        height: 40%;
        justify-content: flex-end;
        margin-right: 7.2%;
    }
    .radiant {
        width: 100%;
        height: 16px;
        background: linear-gradient(270deg, #bb2534, #b2243d, #a72348, #a02250);
    }
    .divFlex {
        display: flex;
    }

    .text-welcome
    {
        color: white;
        font-size: 0.9rem;
        margin-top: 20px;
        text-align: justify;
    }

    @media (max-width: 768px) {
        .haut-gauche {
            display: none;
        }
        .haut-droite {
            display: none;
        }
        .haut-mobile {
            display: flex;
            flex-direction: column;
            width: 100%;
            margin-left: 1vw;
        }
        .text {
            font-size: 7vw;
        }
        .radiant {
            width: 98vw;
        }
        .divButton {
            display: flex;
            justify-content: center;
            margin: 20px;
            width : 80vw;
            height: 12vh;
        }

        .text-welcome
        {
            font-size: 0.8rem;
            margin-top: 20px;
            text-align: justify;
            padding-left: 2vw;
            padding-right: 2vw;
        }

    }
</style>
