<script lang="ts">
    import "../../styles/global.css";
    import Header from "../../Components/Common/Header.svelte";
    import Footer from "../../Components/Common/Footer.svelte";
    import MultiSelect from 'svelte-multiselect';
    import type {Entreprise} from "../../Models/Entreprise";
    import { onMount } from 'svelte';
    import { goto } from "$app/navigation";
    import { GET } from "../../utils/api";
  
    const handleOffreEmploi = () => {
      console.log("OFFRE")
      goto("/offre");
    };





  </script>
  
  <Header />
  <main>
    <section class="emplois">
        <div class="multiSelect">
            <MultiSelect
            id="entreprise"
            options={entrepriseOption}
            placeholder="Choisir entreprise(s)..."
            bind:value={entrepriseSelected}
            maxSelect={1}
            closeDropdownOnSelect={true}
            inputClass="dropdpwn"
            --sms-bg="white"
            ></MultiSelect>
        </div>
      <p class="textEntreprise">Employeur</p>
    </section>
    
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
    .emplois {
      display: flex;
      flex-direction: row;
      margin-left: 10%;
      justify-content: center;
      gap: 10%;
    }
    .textEntreprise {
      font-size: 2em;
      margin: 0;
      color: white;
    }
    .dropdown {
      display: flex;
      flex-direction: column;
      margin-left: 10%;
      background-color: white;
    }
  </style>
  