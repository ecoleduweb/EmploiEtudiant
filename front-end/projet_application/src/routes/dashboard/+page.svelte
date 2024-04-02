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

  const handleEmploi = () => {
    goto("/emplois");
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
    const data: Emploi[] = [
        {
            id: 1,
            titre: "Titre du poste 1",
            dateDebut: "2021-10-10",
            dateFin: "2021-10-11",
            description: "Description du poste 1",
            entreprise: "Entreprise 1",
            poste: "Developpeur",
            ville: "Squatec",
        },
        {
            id: 2,
            titre: "Titre du poste 2",
            dateDebut: "2021-10-10",
            dateFin: "2021-10-11",
            description: "Description du poste 2",
            entreprise: "Entreprise 2",
            poste: "Developpeur",
            ville: "Squatec",
        },
        {
            id: 3,
            titre: "Titre du poste 3",
            dateDebut: "2021-10-10",
            dateFin: "2021-10-11",
            description: "Description du poste 3",
            entreprise: "Entreprise 3",
            poste: "Developpeur",
            ville: "Squatec",
        },
    ];
</script>

<Header />
<main>
  <section class="haut">
    <div class="haut-gauche">
        <div class="divFlex" on:click={handleEmploi}>
            <Button text="Créer une nouvelle offre" />
          </div>
    </div>
    <div class="haut-droite">
      <div class="buttonDiv">
      </div>
    </div>
  </section>
  <section class="offres">
    {#each data as offre}
        <EmploiRow emploi={offre} handleModalClick={handleEmploiClick}
        ></EmploiRow>
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
</style>
