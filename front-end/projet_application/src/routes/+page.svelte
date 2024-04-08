<script lang="ts">
  import "../styles/global.css";
  import Header from "../Components/Common/Header.svelte";
  import Footer from "../Components/Common/Footer.svelte";
  import Button from "../Components/Inputs/Button.svelte";
  import { goto } from "$app/navigation";

  const handleEmploi = () => {
    goto("/emplois");
  };
</script>

<Header />
<main>
  <section class="haut">
    <div class="haut-gauche">
      <h1 class="title">
        <span class="text">PORTAIL D'</span><span class="text"
          >OFFRES D'EMPLOI</span
        >
      </h1>
      <h2 class="text mb">DU CÉGEP DE RIVIÈRE-DU-LOUP</h2>
      <span class="radiant"></span>
    </div>
    <div class="haut-droite">
      <div class="buttonDiv">
        <div class="divFlex" on:click={handleEmploi}>
          <Button text="Consulter toutes les offres" />
        </div>
      </div>
    </div>
  </section>
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
