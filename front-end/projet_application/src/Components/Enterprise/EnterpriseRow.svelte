<script lang="ts">
    import type { Enterprise } from "../../Models/Enterprise"
    export let enterprise: Enterprise
    import type { City } from "../../Models/City"
    import { GET } from "../../ts/server"
    import { onMount } from "svelte"
    export let handleModalClick: (id: number) => void
    let ville: City
    let nomVille: string

    const getCity = async (id: number) => {
        try {
            ville = await GET<any>(`/city/${id}`)
            nomVille = ville.city
        } catch (error) {
            console.error("Error fetching city:", error)
        }
    }

    onMount(async () => {
        await getCity(enterprise.cityId)
    })
</script>

<button class="enterprise" on:click={() => handleModalClick(enterprise.id)}>
    <div class="emploi">
        <div class="info">
            <p class="textTitre">{enterprise.name}</p>
            <p class="text">{enterprise.email}</p>
            <p class="text">{enterprise.phone}</p>
            <p class="text">{enterprise.address}</p>
            <p class="text">{nomVille}</p>
        </div>
        <div class="info-mobile">
            <p class="textTitre">{enterprise.name}</p>
            <p class="text">{enterprise.email}</p>
        </div>
        <img class="image" src="searchBar.svg" alt="ajouter" />
    </div>
</button>

<style scoped>
    .enterprise {
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

    .info-mobile {
        display: none;
    }

    @media (max-width: 768px) {
        .info {
            display: none;
        }
        .info-mobile {
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: center;
            width: 60%;
        }

        .text {
            font-size: 3.5vw;
        }
    }
</style>
