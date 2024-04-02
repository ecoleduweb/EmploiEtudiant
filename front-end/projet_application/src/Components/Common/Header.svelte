<script lang="ts">
  import { goto } from "$app/navigation";

  const handleEmploi = () => {
    goto("/offre");
  };
</script>

<header class="">
  <div class="logo-img">
    <a href="/" class="image"><img src="logo.png" alt="Logo" /></a>
  </div>
  <div class="ul-group">
    <ul class="ul-menu">
      <div class="option dropdown">
        <button class="button dropbtn">
          <p class="textBusiness">Offrir un emploi</p>
          <img class="iconeBusiness" src="business.svg" alt="test" />
        </button>
        <div class="dropdown-content">
          <a href="/login">Connexion entreprise</a>
          <a href="/register">Créer un compte entreprise</a>
        </div>
      </div>
      <div class="option">
        <button class="button" on:click={handleEmploi}>
          <p class="textSearch">Trouver un emploi</p>
          <img class="iconeSearch" src="searchBar.svg" alt="test" />
        </button>
      </div>
    </ul>
  </div>
</header>

<style scoped>
  @import "../../styles/header.css";
</style>
