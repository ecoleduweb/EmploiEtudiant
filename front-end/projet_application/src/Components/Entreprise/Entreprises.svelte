<script lang="ts">
    import Modal from "../Common/Modal.svelte";
    import type { Entreprise } from "../../Models/Entreprise";
    import { GET } from "../../ts/server";
    import { onMount } from "svelte";
    import type { City } from "../../Models/City";
    export let entreprise: Entreprise;
    export let handleEntrepriseClick: () => void;

    let ville: City;
    let nomVille: string;

    const getCity = async (id: number) => {
        try {
            ville = await GET<any>(`/city/${id}`);
            nomVille = ville.city;
        } catch (error) {
            console.error("Error fetching city:", error);
        }
    };

    onMount(() => {
        getCity(entreprise.cityId);
    });


</script>

<Modal handleModalClick={handleEntrepriseClick}>
    <div class="container">
        <div class="titleContainer">
            <h3 class="title">{entreprise.name}</h3>
        </div>
        <div class="info">
            <h5 class="infoTitle">Adresse courriel</h5>
            <p class="text">{entreprise.email}</p>
            <h5 class="infoTitle">Numéro de téléphone</h5>
            <p class="text">{entreprise.phone}</p>
            <h5 class="infoTitle">Adresse de l'entreprise</h5>
            <p class="text">{entreprise.address}</p>
            <h5 class="infoTitle">Ville</h5>
            <p class="text">{nomVille}</p>
        </div>
    </div>
</Modal>

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
    /* .subtitle {
        font-size: 1.5rem;
        margin: 0px;
        margin-bottom: 2.25vw;
        color: black;
    } */
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
