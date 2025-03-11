<script>
  import DetailOfferRow from "../JobOffer/DetailOfferRow.svelte";

  // Définition des propriétés du composant
  export let columns = []; // Tableau contenant la définition des colonnes
  export let data = [];    // Données à afficher
  export let title = "";   // Titre du tableau (optionnel)
  export let showActions = true; // Afficher les actions ou non
  export let rowComponent = null; // Ajout d'un composant personnalisé pour les lignes
  export let handleModalClick = undefined; // Fonction pour gérer le clic sur un élément
</script>

<div class="table-container">
  {#if title}
    <h3 class="table-title">{title}</h3>
  {/if}
  
  <table>
    <thead>
      <tr>
        {#each columns as column}
          <th class={column.class || ""}>{column.label}</th>
        {/each}
      </tr>
    </thead>
    <tbody>
      {#if rowComponent}
        <!-- Utilisation d'un composant personnalisé pour les lignes -->
        {#each data as offer}
          <svelte:component this={rowComponent} {offer} handleModalClick={handleModalClick} />
        {/each}
      {:else}
        <!-- Rendu standard des lignes -->
        {#each data as offer}
          <tr>
            {#each columns as column}
              <td class={column.class || ""}>
                {#if column.key === 'posteVise'}
                  {offer.title || 'Non spécifié'}
                {:else if column.key === 'typeEmploi'}
                  {offer.employmentSchedule?.name || 'Non spécifié'}
                {:else if column.key === 'dateLimite'}
                  {new Date(offer.deadlineApply).toLocaleDateString('fr-CA') || 'Non spécifié'}
                {:else if column.key === 'programmesVises'}
                  {#if offer.studyPrograms && offer.studyPrograms.length}
                    {offer.studyPrograms.map(p => p.name).join(', ')}
                  {:else}
                    Tous les programmes
                  {/if}
                {:else if column.key === 'employeur'}
                  {offer.enterprise?.name || 'Entreprise inconnue'}
                {:else if column.key === 'details'}
                  <button class="details-btn" on:click={() => handleModalClick(offer)}>
                    Détails
                  </button>
                {:else if column.formatter}
                  {@html column.formatter(offer)}
                {:else}
                  {offer[column.key] || ''}
                {/if}
              </td>
            {/each}
          </tr>
        {/each}
      {/if}
      
      {#if data.length === 0}
        <tr>
          <td colspan={columns.length} class="no-data">Aucune donnée disponible</td>
        </tr>
      {/if}
    </tbody>
  </table>
</div>

<style>
  .table-container {
    margin-bottom: 2rem;
    width: 100%;
    overflow-x: auto;
  }
  
  .table-title {
    margin-bottom: 1rem;
    font-size: 1.2rem;
    font-weight: bold;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    border-spacing: 0;
    table-layout: fixed;
  }
  
  th, td {
    padding: 0.5rem 0 0.5rem 0;
    text-align: left;
    border-bottom: 1px solid #00ad9a;
  }
  
  th {
    font-weight: bold;
    color: #00ad9a;
  }

  td {
    color: white;
  }
  
  tbody tr:hover {
    background-color: #555b66;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  
  .details-btn {
    padding: 0.25rem 0.5rem;
    background-color: transparent;
    border: none;
    cursor: pointer;
    color: #00ad9a;
    font-weight: bold;
  }
  
  .no-data {
    text-align: center;
    padding: 2rem;
    color: #888;
  }
  
  @media (max-width: 768px) {
    .rowTitles {
      display: none;
    }
  }
</style>