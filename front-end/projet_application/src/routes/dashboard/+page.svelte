<script lang="ts">
  import "../../styles/global.css";
  import Header from "../../Components/Common/Header.svelte";
  import Footer from "../../Components/Common/Footer.svelte";
  import Button from "../../Components/Inputs/Button.svelte";
  import { writable } from "svelte/store";
  import type { jobOffer } from "../../Models/Offre";
  import type { Entreprise } from "../../Models/Entreprise";
  import type { User } from "../../Models/User";
  import OfferRow from "../../Components/OffreEmplois/OfferRow.svelte";
  import CreateEditOffre from "../../Components/NewOffre/CreateEditOffre.svelte";
  import OffreEmploi from "../../Components/OffreEmplois/OffreEmploi.svelte";
  import ApprouveOffre from "../../Components/OffreEmplois/ApprouveOffre.svelte";
  import { GET } from "../../ts/server";
  import { onMount } from "svelte";
  import { jwtDecode } from "jwt-decode";
  import Modal from "../../Components/Common/Modal.svelte";
  import type Token from "../../Models/Token";

  let isJobOfferEdit = false;
  let isModerator = false;
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
  const handleEditEmploiClick = (offreId: number) => {
    isJobOfferEdit = true;
    const offre = $jobOffers.find((x) => x.id === offreId);
    if (offre) {
      offre.isApproved = null;
    }
    openModal(offreId);
  };

  const modalApprove = writable(false);
  const selectedEmploiIdApprove = writable(0);
  const openModalApprove = (id: number) => {
    modalApprove.set(true);
    selectedEmploiIdApprove.set(id);
  };
  const closeModalApprove = () => {
    modalApprove.set(false);
  };
  const handleApproveClick = (offreId: number) => {
    console.log(offreId);
    openModalApprove(offreId);
  };


  let user: User = {
    id: 0,
    email: "",
    password: "",
    firstName: "",
    lastName: "",
    phone: "",
    address: "",
    cityId: 0,
    roleId: 0,
    active: true,
    token: "",
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
    approbationMessage: "",
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
    approbationMessage: "",
  };

  let entreprise: Entreprise = {
    id: 0,
    name: "",
    address: "",
    email: "",
    phone: "",
    cityId: 0,
    isTemporary: false,
  };

  let errorEntreprise: Entreprise = {
    id: 0,
    name: "",
    address: "",
    email: "",
    phone: "",
    cityId: 0,
    isTemporary: false,
  };

  onMount(async () => {
    const token = localStorage.getItem("token");
    if (token) {
      user = jwtDecode(token);
      if (user.isModerator === true) {
        isModerator = true;
      }
      await getJobOffersEmployeur();
    }
  });

  const jobOffers = writable<jobOffer[]>([]);

  const getJobOffersEmployeur = async () => {
    try {
      const responseOffre = await GET<any>("/jobOffer/offresEmploiEmployeur");
      jobOffers.set(responseOffre);
    } catch (error) {
      console.error("Error fetching job offers:", error);
    }
  };
  let dateNow = new Date().toISOString().split('T')[0];

  $: toBeApprovedOffer = $jobOffers.filter((x) => x.isApproved === null);
  $: isRefusedOffer = $jobOffers.filter((x) => x.isApproved === false);
  $: offerToCome = $jobOffers.filter((x) => {
    if (!x.isApproved) return false;
    let dateDebut = new Date(x.offerDebut).toISOString().split('T')[0];
    return dateNow < dateDebut;
  });
  $: offerDisplayed = $jobOffers.filter((x) => {
    if (!x.isApproved) return false;
    let dateDebut = new Date(x.offerDebut).toISOString().split('T')[0];
    let dateFin = new Date(x.deadlineApply).toISOString().split('T')[0];
    return dateNow >= dateDebut && dateNow <= dateFin;
  });
  $: expiredOffer = $jobOffers.filter((x) => {
    if (!x.isApproved) return false;
    let dateFin = new Date(x.deadlineApply).toISOString().split('T')[0];
    return dateFin < dateNow;
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
    {#if isModerator === true}
      <p class="textOffre">Les offres d'emplois</p>
    {/if}
    {#if isModerator === false}
      <p class="textOffre">Mes offres d'emplois</p>
    {/if}
    <!-- {#if toBeApprovedOffer.length > 0}
      <h2 class="textSections">En attente d'approbation</h2>
      {#each toBeApprovedOffer as offre}
        <OfferRow user={user} offre={offre} handleEditModalClick={handleEditEmploiClick} handleApproveModalClick={handleApproveClick} />
     {/each}
    {/if} -->
    {#if isRefusedOffer.length > 0}
      <h2 class="textSections">Offres refusées</h2>
      {#each isRefusedOffer as offre}
        <OfferRow {user} {offre} handleEditModalClick={handleEditEmploiClick} handleApproveModalClick={handleApproveClick} />
      {/each}
    {/if}
    {#if toBeApprovedOffer.length > 0}
      <h2 class="textSections">Offres en attente d'approbation</h2>
      {#each toBeApprovedOffer as offre}
      <OfferRow {user} {offre} handleEditModalClick={handleEditEmploiClick} handleApproveModalClick={handleApproveClick} />
      {/each}
    {/if}
    {#if offerToCome.length > 0}
      <h2 class="textSections">Offres bientôt affichées</h2>
      {#each offerToCome as offre}
        <OfferRow user={user} offre={offre} handleEditModalClick={handleEditEmploiClick} handleApproveModalClick={handleApproveClick} />
      {/each}
    {/if}
    {#if offerDisplayed.length > 0}
      <h2 class="textSections">Offres affichées</h2>
      {#each offerDisplayed as offre}
        <OfferRow user={user} offre={offre} handleEditModalClick={handleEditEmploiClick} handleApproveModalClick={handleApproveClick}/>
      {/each}
    {/if}
    {#if expiredOffer.length > 0}
      <h2 class="textSections">Offres expirées</h2>
      {#each expiredOffer as offre}
        <OfferRow user={user} offre={offre} handleEditModalClick={handleEditEmploiClick} handleApproveModalClick={handleApproveClick}/>
    {/each}
    {/if}
  </section>
  {#if $modal}
    {#if isJobOfferEdit === false}
      <CreateEditOffre handleEmploiClick={closeModal} {isJobOfferEdit} />
    {/if}
    {#if isJobOfferEdit === true}
      {#each $jobOffers as offre}
        {#if offre.id === $selectedEmploiId}
          <CreateEditOffre
            {offre}
            handleEmploiClick={closeModal}
            {isJobOfferEdit}
          />
        {/if}
      {/each}
    {/if}
  {/if}
  {#if $modalApprove}
        {#each $jobOffers as emploi}
            {#if emploi.id === $selectedEmploiIdApprove}
              <Modal handleModalClick={closeModalApprove}>
                <ApprouveOffre offre={emploi} entreprise={entreprise} handleApproveClick={closeModalApprove}/>
              </Modal>
            {/if}
        {/each}
    {/if}
</main>
<Footer />

<style scoped>
  body {
    margin: 0;
    padding: 0;
  }
  main {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center; 
    padding: 2vh; 
    min-height: 77vh;
  }
  .haut {
    width: 100%;
    margin-bottom: 2vh; 
  }
  .haut-gauche {
    width: 30%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .divFlex {
    display: flex;
    margin-bottom: 2vh;
  }
  .offres {
    width: 100%;
    display: flex;
    flex-direction: column;
  }
  .textOffre {
    font-size: 2.5em;
    margin: 0;
    margin-bottom: 2vh;
    color: white;
  }
  .textSections {
    font-size: 1.8em;
    margin: 0;
    margin-top: 5vh;
    color: white;
  }
</style>

