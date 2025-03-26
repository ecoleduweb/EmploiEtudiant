<script lang="ts">
  import type { JobOfferDetails } from "../../Models/JobOfferDetails";
  import DetailOfferRow from "./DetailOfferRow.svelte";

  export let offers: JobOfferDetails[] = [];
  export let handleOfferClick: (offer : JobOfferDetails) => void;
</script>

<div class="table-container">
  <table>
      <thead>
          <tr>
              <th>Titre</th>
              <th>Entreprise</th>
              <th>Description</th>
              <th>Date</th>
              <th>Actions</th>
          </tr>
      </thead>
      <tbody>
          {#each offers as offer}
              <DetailOfferRow offer={offer} handleModalClick={() => handleOfferClick(offer)} />
          {/each}
      </tbody>
  </table>
</div>

<style>
  .table-container {
      width: 100%;
      overflow-x: auto;
  }
  table {
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
  }
  thead {
      color: white;
  }
  th {
      padding: 12px 12px 12px 0;
      text-align: left;
      border-bottom: 1px solid #ddd;
      font-weight: bold;
      color: #00ad9a;
  }
  /*
  @media (max-width: 768px) {
      .rowTitles {
          display: none;
      }
      th:nth-child(1) {
          width: 60%;
      }
      th:nth-child(5) {
          width: 30%;
      }
      th:nth-child(6) {
          width: 10%;
      }
  }*/
</style>