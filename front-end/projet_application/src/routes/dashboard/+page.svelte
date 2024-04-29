<script lang="ts">
  import "../../styles/global.css";
  import Header from "../../Components/Common/Header.svelte";
  import Footer from "../../Components/Common/Footer.svelte";
  import Button from "../../Components/Inputs/Button.svelte";
  import { writable } from "svelte/store";
  import type { jobOffer } from "../../Models/Offre";
  import type { Entreprise } from "../../Models/Entreprise";
  import OfferRow from "../../Components/OffreEmplois/OfferRow.svelte";
  import CreateEditOffre from "../../Components/NewOffre/CreateEditOffre.svelte";
  import { GET } from "../../ts/server";
  import { onMount } from "svelte";

  let isJobOfferEdit = false;

  const handleOffreEmploi = () => {
    isJobOfferEdit = false;
    openModal(0);
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
    isJobOfferEdit = true;
    openModal(offreId);
  };
  let offre: jobOffer = {
    id: 0,
    title: "",
    address: "",
    description: "",
    offerDebut: "",
    dateEntryOffice: "",
    deadlineApply: "",
    email: "",
    hoursPerWeek: 0,
    compliantEmployer: false, 
    internship: false,
    offerLink: "",
    offerStatus: 0,
    active: true,
    salary: "",
    scheduleId: -1,
    employerId: 1,
    isApproved: false,
  };

  let error: jobOffer = {
    id: 0,
    title: "",
    address: "",
    description: "",
    offerDebut: "",
    dateEntryOffice: "",
    deadlineApply: "",
    email: "",
    hoursPerWeek: 0,
    compliantEmployer: false, 
    internship: false,
    offerLink: "",
    offerStatus: 0,
    active: true,
    salary: "",
    scheduleId: 0,
    employerId: 0,
    isApproved: false,
  };

  let entreprise: Entreprise = {
    id: 0,
    name: "",
    address: "",
    email: "",
    phone: "",
    cityId: 0,
    isTemporary: false,
  }

  let errorEntreprise: Entreprise = {
    id: 0,
    name: "",
    address: "",
    email: "",
    phone: "",
    cityId: 0,
    isTemporary: false,
  }

  const jobOffers = writable<jobOffer[]>([]);
  const getJobOffersEmployeur = async () => {
    try {
      const responseOffre = await GET<any>("/jobOffer/offresEmploiEmployeur");
      jobOffers.set(responseOffre);
    } catch (error) {
      console.error("Error fetching job offers:", error);
    }
  };
  onMount(getJobOffersEmployeur);

  const getEntreprise = async () => {
    try {
      const responseEntreprise = await GET<any>("/enterprise/getEnterpriseByEmployer?id=" + offre.employerId);
      entreprise = responseEntreprise;
    } catch (error) {
      console.error("Error fetching entreprise:", error);
    }
  };
  onMount(getEntreprise);

  $: notApprovedOffer = $jobOffers.filter((x) => !x.isApproved);
  $: offerToCome = $jobOffers.filter((x) => {
    if (!x.isApproved) return false;
    let dateDebut = new Date(x.offerDebut);
    let dateNow = new Date();
    return dateNow < dateDebut;
  });
  $: offerDisplayed = $jobOffers.filter((x) => {
    if (!x.isApproved) return false;
    let dateDebut = new Date(x.offerDebut);
    let dateFin = new Date(x.deadlineApply);
    let dateNow = new Date();
    return dateNow >= dateDebut && dateNow <= dateFin;
  });
  $: expiredOffer = $jobOffers.filter((x) => {
    if (!x.isApproved) return false;
    let dateFin = new Date(x.deadlineApply);
    let dateNow = new Date();
    return dateNow > dateFin;
  });

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
    {#if isJobOfferEdit === false}
        <CreateEditOffre handleEmploiClick={closeModal} isJobOfferEdit={isJobOfferEdit} />
    {/if}
    {#if isJobOfferEdit === true}
      {#each $jobOffers as offre}
        {#if offre.id === $selectedEmploiId}
          <CreateEditOffre offre={offre} entreprise={entreprise} handleEmploiClick={closeModal} isJobOfferEdit={isJobOfferEdit} />
        {/if}
      {/each}
    {/if}
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
