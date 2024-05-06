<script lang="ts">
  import type { jobOffer } from "../../Models/Offre";
  import { GET } from "../../ts/server";
  import { onMount } from "svelte";
  import { writable } from "svelte/store";

  export let offre: jobOffer;
  export let handleModalClick: (id: number) => void;

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

<button class="offreEmploi" on:click={() => handleModalClick(offre.id)}>
  <div class="emploi">
    <div class="info">
      <p class="text">{offre.title}</p>
      <p class="text">{$entreprise}</p>
      <p class="text">{offre.deadlineApply}</p>
      <p class="description">{offre.description}</p>
    </div>
    <img class="image" src="add.svg" alt="ajouter" />
  </div>
</button>

<style scoped>
  .offreEmploi {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 90%;
    border-width: 0px;
    border-bottom: 1px solid #00ad9a;
    margin-left: 5.2%;
    background-color: transparent;
  }
  .info {
    display: flex;
    width: 90%;
    font-size: 1.2rem;
    flex-direction: row;
    justify-content: space-around;
  }
  .description {
    display: flex;
    width: 50%;
    font-size: 1rem;
    flex-direction: row;
    justify-content: space-around;
  }
  .text {
    width: 20%;
  }
  .emploi {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    color: white;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    width: 100%;
    height: 100%;
    padding: 5px 0px 5px 0px;
  }
  .emploi:hover {
    background-color: #555b66;
  }
  .image {
    width: 30px;
    height: 30px;
  }
</style>
