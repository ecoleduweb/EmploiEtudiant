<script lang="ts">
  import "../../styles/global.css";
  import Header from "../../Components/Common/Header.svelte";
  import Footer from "../../Components/Common/Footer.svelte";
  import Button from "../../Components/Inputs/Button.svelte";
  import { writable } from "svelte/store";
  import type { jobOffer } from "../../Models/Offre";
  import EmploiRow from "../../Components/OffreEmplois/EmploiRow.svelte";
  import OffreEmploi from "../../Components/OffreEmplois/OffreEmploi.svelte";
  import CreateEditOffre from "../../Components/NewOffre/CreateEditOffre.svelte";
  import { goto } from "$app/navigation";
  import OfferRow from "../../Components/OffreEmplois/OfferRow.svelte";
  import { GET } from "../../ts/server";
  import { onMount } from "svelte";

  const handleOffreEmploi = () => {
    goto("/offre");
  };

  const modal = writable(false);
  const selectedEmploiId = writable(0);
  const openModal = (id: number) => {
    modal.set(true);
    selectedEmploiId.set(id);
  };
  const closeModal = () => {
    modal.set(false);
  };
  const handleEmploiClick = (offreId: number) => {
    openModal(offreId);
  };

  const jobOffers = writable<jobOffer[]>([]);
  const getJobOffersEmployeur = async () => {
    try {
      const response = await GET<any>("jobOffer/offresEmploiEmployeur");
      jobOffers.set(response);
    } catch (error) {
      console.error("Error fetching job offers:", error);
    }
  };
  onMount(getJobOffersEmployeur);

  const notApprovedOffer = $jobOffers.filter((x) => !x.isApproved);
  const offerToCome = $jobOffers.filter((x) => {
    let dateDebut = new Date(x.offerDebut);
    let dateNow = new Date();
    return dateNow < dateDebut;
  });
  const offerDisplayed = $jobOffers.filter((x) => {
    let dateDebut = new Date(x.offerDebut);
    let dateFin = new Date(x.deadlineApply);
    let dateNow = new Date();
    return x.isApproved && dateNow >= dateDebut && dateNow <= dateFin;
  });
  const expiredOffer = $jobOffers.filter((x) => {
    let dateFin = new Date(x.deadlineApply);
    let dateNow = new Date();
    return dateNow > dateFin;
  });
  console.log(notApprovedOffer.length, offerToCome.length, offerDisplayed.length, expiredOffer.length);
</script>

<Header />
<main>
  <section class="haut">
    <div class="haut-gauche">
      <div class="divFlex">
        <Button onClick={handleOffreEmploi} text="Créer une nouvelle offre" />
      </div>
    </div>
  </section>
  <section class="offres">
    <p class="textOffre">Mes offres d'emplois</p>
    {#if notApprovedOffer.length > 0}
      <h2 class="textSections">En attente d'approbation</h2>
      {#each notApprovedOffer as offre}
        <OfferRow offre={offre} handleModalClick={handleEmploiClick} />
      {/each}
    {/if}
    {#if offerToCome.length > 0}
      <h2 class="textSections">Offres bientôt affichées</h2>
      {#each offerToCome as offre}
        <OfferRow offre={offre} handleModalClick={handleEmploiClick} />
      {/each}
    {/if}
    {#if offerDisplayed.length > 0}
      <h2 class="textSections">Offres affichées</h2>
      {#each offerDisplayed as offre}
        <OfferRow offre={offre} handleModalClick={handleEmploiClick} />
      {/each}
    {/if}
    {#if expiredOffer.length > 0}
      <h2 class="textSections">Offres expirées</h2>
      {#each expiredOffer as offre}
        <OfferRow offre={offre} handleModalClick={handleEmploiClick} />
      {/each}
    {/if}
  </section>
  {#if $modal}
    {#each $jobOffers as offre}
      {#if offre.id === $selectedEmploiId}
        <CreateEditOffre offre={offre} handleEmploiClick={closeModal} />
      {/if}
    {/each}
  {/if}
</main>
<Footer />

<style scoped>
  main {
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 100%;
    min-height: 81vh;
  }
  .haut {
    display: flex;
    widows: 85%;
  }
  .haut-gauche {
    display: flex;
    width: 30%;
    justify-content: center;
    align-items: center;
  }
  .divFlex {
    display: flex;
    margin-bottom: 40px;
  }
  .offres {
    display: flex;
    flex-direction: column;
    margin-left: 10%;
  }
  .textOffre {
    font-size: 2.5em;
    margin: 0;
    margin-bottom: 1%;
    color: white;
  }
  .textSections {
    font-size: 1.8em;
    margin: 0;
    margin-top: 15px;
    margin-bottom: 5;
    color: white;
  }
</style>
