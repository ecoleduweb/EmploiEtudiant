<script lang="ts">
  import "../../styles/global.css";
  import Header from "../../Components/Common/Header.svelte";
  import Footer from "../../Components/Common/Footer.svelte";
  import Button from "../../Components/Inputs/Button.svelte";
  import { writable } from "svelte/store";
  import type { Emploi } from "../../Models/Emploi";
  import EmploiRow from "../../Components/OffreEmplois/EmploiRow.svelte";
  import OffreEmploi from "../../Components/OffreEmplois/OffreEmploi.svelte";
  import { goto } from "$app/navigation";
  import OfferRow from "../../Components/OffreEmplois/OfferRow.svelte";

  const handleOffreEmploi = () => {
    console.log("OFFRE")
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
  let emploi: Emploi = {
    id: 0,
    title: "",
    address: "",
    description: "",
    dateEntryOffice: "",
    deadlineApply: "",
    email: "",
    hoursPerWeek: 0,
    compliantEmployer: false, 
    internship: false,
    offerLink: "",
    offerStatus: 0,
    urgent: false,
    active: true,
    scheduleId: -1,
    employerId: 1,
  };

  let error: Emploi = {
    id: 0,
    title: "",
    address: "",
    description: "",
    dateEntryOffice: "",
    deadlineApply: "",
    email: "",
    hoursPerWeek: 0,
    compliantEmployer: false, 
    internship: false,
    offerLink: "",
    offerStatus: 0,
    urgent: false,
    active: true,
    scheduleId: 0,
    employerId: 0,
  };
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
    {#each data as offre}
      <OfferRow emploi={offre} handleModalClick={handleEmploiClick} />
    {/each}
  </section>
  {#if $modal}
    {#each data as emploi}
      {#if emploi.id === $selectedEmploiId}
        <OffreEmploi {emploi} handleEmploiClick={closeModal} />
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
    font-size: 2em;
    margin: 0;
    color: white;
  }
</style>
