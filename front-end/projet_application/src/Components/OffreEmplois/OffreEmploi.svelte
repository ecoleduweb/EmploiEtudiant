<script lang="ts">
  import Modal from "../Common/Modal.svelte";
  import type { jobOffer } from "../../Models/Offre";
  import type { Entreprise } from "../../Models/Entreprise";
  import { GET } from "../../ts/server";
  import { onMount } from "svelte";
  import { writable } from "svelte/store";
  export let offre: jobOffer;
  let currentPage = window.location.pathname;

  const entreprise = writable<string>();
  const getEnterprises = async (employerId: number) => {
    try {
      const response = await GET<any>(
        "/enterprise/getEnterpriseByEmployer?id=" + employerId
      );
      entreprise.set(response.name);
    } catch (error) {
      console.error("Error fetching entreprise:", error);
    }
  };
  onMount(() => {
    getEnterprises(offre.employerId);
  });
</script>

<div class="container">
  <div class="titleContainer">
    <h3 class="title">{offre.title}</h3>
    <h4 class="subtitle">Chez {$entreprise}</h4>
  </div>
  <div class="info">
    <h5 class="infoTitle">Type de poste</h5>
    <p class="text">{offre.title}</p>
    <h5 class="infoTitle">Adresse du lieu de travail</h5>
    <p class="text">{offre.address}</p>
    <h5 class="infoTitle">Description du poste</h5>
    <p class="text">{offre.description}</p>
    <h5 class="infoTitle">Date de début</h5>
    <p class="text">{offre.offerDebut}</p>
    <h5 class="infoTitle">Date limite pour postuler</h5>
    <p class="text">{offre.deadlineApply}</p>
    <h5 class="infoTitle">Où envoyer votre candidature</h5>
    <p class="text">{offre.email}</p>
  </div>
</div>

<style scoped>
  .titleContainer {
    display: flex;
    flex-direction: column;
  }
  .title {
    font-size: 2.5rem;
    color: #00ad9a;
    margin: 0px;
    margin-bottom: 1.5vw;
  }
  .subtitle {
    font-size: 1.5rem;
    margin: 0px;
    margin-bottom: 2.25vw;
    color: black;
  }
  .infoTitle {
    font-size: 1.3rem;
    margin: 0px;
    margin-bottom: 0.5vw;
  }
  .info {
    color: black;
  }
  .text {
    font-size: 1.1rem;
    margin: 0px;
    margin-bottom: 1.75vw;
    color: black;
  }
  .container {
    width: 95%;
    display: flex;
    flex-direction: column;
    text-align: left;
    justify-content: space-between;
    color: white;
    border-radius: 4px;
    transition: background-color 0.3s ease;
  }
</style>
