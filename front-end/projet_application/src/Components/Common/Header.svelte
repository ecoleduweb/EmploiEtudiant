<script lang="ts">
  import { goto } from "$app/navigation";

  // Variable pour suivre l'état de connexion de l'utilisateur
  let isLoggedIn = false;

  const handleEmploi = () => {
    goto('/emplois')
  };

  const handleLogout = () => {
    isLoggedIn = false; // Mettre à jour lors de la déconnexion
    goto('/')
    console.log('Logout clicked');
  };
</script>

<header>
  <div class="logo-img">
    <a href="/" class="image"><img src="logo.png" alt="Logo" /></a>
  </div>
  <div class="ul-group">
    <ul class="ul-menu">
      <div class="option dropdown">
        <button class="button dropbtn">
          <p class="textBusiness">Offrir un emploi</p>
          <img class="iconeBusiness" src="business.svg" alt="Business icon" />
        </button>
        <div class="dropdown-content">
          <a href="/login">Connexion entreprise</a>
          <a href="/register">Créer un compte entreprise</a>
        </div>
      </div>
      {#if isLoggedIn}
        <div class="option">
          <button class="button logout-button" on:click={handleLogout}>
            <p class="textLogout">Déconnexion</p>
            <img class="iconeLogout" src="logout.svg" alt="Logout icon" />
          </button>
        </div>
      {/if}
      <div class="option">
        <button class="button" on:click={handleEmploi}>
          <p class="textSearch">Trouver un emploi</p>
          <img class="iconeSearch" src="searchBar.svg" alt="Search icon" />
        </button>
      </div>
    </ul>
  </div>
</header>


<style scoped>
  @import "../../styles/header.css";

  .logout-button {
    background-color: transparent; /* Match style to other buttons */
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
  }

  .textLogout {
    margin-right: 8px; /* Spacing between text and icon */
  }

  .iconeLogout {
    width: 24px; /* Adjust size as necessary */
  }
</style>
