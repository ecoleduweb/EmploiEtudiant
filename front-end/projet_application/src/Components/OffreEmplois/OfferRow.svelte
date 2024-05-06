<script lang="ts">
  import { redirect } from "@sveltejs/kit";
    import type { jobOffer } from "../../Models/Offre";
    import type { User } from "../../Models/User";
  import { goto } from "$app/navigation";
    export let user: User;
    export let offre: jobOffer;
    export let handleEditModalClick: (id: number) => void;
    export let handleApproveModalClick: (id: number) => void;
</script>


<div class="offreEmploi">
    <div class="emploi">
        <div class="info">
            <p class="text">{offre.title}</p>
            <p class="text">{offre.offerDebut}</p>
            <p class="text">{offre.description}</p>
        </div>
        {#if user.isModerator === true}
          <button class="button" on:click={() => handleApproveModalClick(offre.id)}>
              <img class="image" src="check.svg" alt="approve" />
          </button>
        {/if}
        <button class="button" on:click={() => handleEditModalClick(offre.id)}>
            <img class="image" src="edit.svg" alt="modifier" />
        </button>
        <button class="button">
            <img class="image" src="cancel.svg" alt="supprimer" />
        </button>
    </div>
</div>

<style scoped>
  .offreEmploi {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 55%;
    border-width: 0px;
    border-bottom: 1px solid #00ad9a;
    background-color: transparent;
  }
  .info {
    display: flex;
    width: 90%;
    font-size: 1.15rem;
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
    width: 100%;
    height: 100%;

    transition: background-color 0.1s ease;
  }
  .emploi:hover {
    background-color: #485163;
  }
  .image {
    width: 30px;
    height: 30px;
  }
  .button {
    background-color: transparent;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease;
    border-radius: 4px;
  }
  .button:hover {
    background-color: #455b66;
  }
</style>
