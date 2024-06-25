<script lang="ts">
    import "../styles/global.css"
    import Button from "../Components/Inputs/Button.svelte"
    import { goto } from "$app/navigation"
    import LoadingSpinner from "../Components/Common/LoadingSpinner.svelte"
    import DetailOfferRow from "../Components/JobOffer/DetailOfferRow.svelte"
    import { writable } from "svelte/store"
    import type { JobOffer } from "../Models/Offre"
    import { GET } from "../ts/server"
    import { onMount } from "svelte"
    import { error } from "@sveltejs/kit"

    let loaded = false

    const jobOffers = writable<JobOffer[]>([])
    let LatestJobOffers: JobOffer[] = []
    const getJobOffers = async () => {
        try {
            const response = await GET<any>("/jobOffer/approved")
            jobOffers.set(response)

            let JobOffersLen = $jobOffers.length

            if (JobOffersLen > 0) //Vérifie s'il y a des éléments dans l'array
            {
                if (JobOffersLen > 5) //Il y a plus que 5
                {
                    //Cherche le dernier job offer et recupère ça date et vérifie s'il est plus que 7 jours (s'il est plus grand que 7, ça vas être 7)
                    let OldestJobOfferDate = new Date($jobOffers[ ((JobOffersLen >= 7 ? 7 : 6) - 1) ].approvedDate).getTime()
                        < new Date().getTime()

                    if (JobOffersLen > 7 && OldestJobOfferDate) //S'il y en à plus que 7 et que la date, donne juste 7 offers
                    {
                        LatestJobOffers = ($jobOffers).slice(0, 7)
                    }
                    else if (JobOffersLen <= 7 && OldestJobOfferDate) //S'il y a 6
                    {
                        LatestJobOffers = ($jobOffers).slice(0, JobOffersLen)
                    }
                    else //Si la date est plus grand que 7 jour donc 5
                    {
                        LatestJobOffers = ($jobOffers).slice(0, 5)
                    }
                }
                else //Il n'y a pas plus que 5
                {
                    LatestJobOffers = ($jobOffers).slice(0, JobOffersLen)
                }
            }
        } catch (error) {
            console.error("Error fetching job offers:", error)
        }
    }
    onMount(async () => {
        try 
        {
            await getJobOffers()
        }

        catch (error) 
        {
            console.error("Error while loading the page", error)
        }

        finally
        {
            $jobOffers.forEach(element => {
                console.log("Offer Name:" + element.title + " Approbation Date:" + new Date(element.approvedDate))
            });
            
            loaded = true
        }
    })

    const handleEmploi = () => {
        goto("/emplois")
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
            <span class="radiant"></span>
        </div>
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
            {#each LatestJobOffers as offer}
                <DetailOfferRow {offer} 
                handleModalClick={(function() {})}/>
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
        width: 50%;
        margin-left: 5.2%;
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
        width: 210px;
        height: 16px;
        background: linear-gradient(270deg, #bb2534, #b2243d, #a72348, #a02250);
    }
    .divFlex {
        display: flex;
    }
    @media screen and (max-width: 900px) and (min-width: 300px) {
        .divFlex {
            display: flex;
        }

        .buttonDiv 
        {
            height: unset;
        }

        .radiant 
        {
            width: 110%;
            height: 22px;
        }

        .text 
        {
            font-size: 3.3vw;
        }
    }
</style>
