<script lang="ts">
    import type { Entreprise } from "../../Models/Entreprise"
    export let entreprise: Entreprise
    import type { City } from "../../Models/City"
    import { GET } from "../../ts/server"
    import { onMount } from "svelte"
    export let handleModalClick: (id: number) => void
    let ville: City
    let nomVille: string

    const getCity = async (id: number) => {
        try {
            ville = await GET<any>(`/city/oneCity?id=${id}`)
            nomVille = ville.city
        } catch (error) {
            console.error("Error fetching city:", error)
        }
    }

    onMount(() => {
        getCity(entreprise.cityId)
    })
</script>

<button class="entreprise" on:click={() => handleModalClick(entreprise.id)}>
    <div class="emploi">
        <div class="info">
            <p class="textTitre">{entreprise.name}</p>
            <p class="text">{entreprise.email}</p>
            <p class="text">{entreprise.phone}</p>
            <p class="text">{entreprise.address}</p>
            <p class="text">{nomVille}</p>
        </div>
        <img class="image" src="add.svg" alt="ajouter" />
    </div>
</button>

<style scoped>
    .entreprise {
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
        align-items: center;
    }
    .text {
        width: 20%;
    }
    .textTitre {
        width: 20%;
        font-weight: bold;
        font-size: 1.8rem;
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
