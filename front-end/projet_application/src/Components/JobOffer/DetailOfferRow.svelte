<script lang="ts">
    import type { JobOfferDetails } from "../../Models/JobOfferDetails"
    import type { JobOffer } from "../../Models/Offre"
    import { GET } from "../../ts/server"
    import { onMount } from "svelte"
    import { writable } from "svelte/store"

    export let offer: JobOfferDetails
    export let handleModalClick: (offer: JobOfferDetails) => void

    const enterprise = writable<string>()
    const getEnterprises = async () => {
        try {
            const response = await GET<any>(
                `/enterprise/employer/${offer.employerId}`
            )
            enterprise.set(response.name)
        } catch (error) {
            console.error("Error fetching enterprise:", error)
        }
    }

    onMount(async () => {
        if (offer) 
        {
            await getEnterprises(); 
        }
    })
</script>

<button class="offreEmploi" on:click={() => handleModalClick(offer)}>
    <div class="emploi">
        <div class="info-mobile">
            <p class="text">{offer.title}</p>
            <p class="text">{offer.enterprise?.name}</p>
        </div>
        <div class="info">
            <p class="text">{offer.title}</p>
            <p class="text">{offer.schedules?.map(x => x.description).join(', ')}</p>
            <p class="text">{offer.deadlineApply}</p>
            <p class="text">{offer.studyPrograms?.map(x => x.name).join(', ')}</p>
            <p class="text">{offer.enterprise?.name}</p>
        </div>
        <img class="image" src="add.svg" alt="ajouter" />
    </div>
</button>

<style scoped>
    .offreEmploi {
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
    }
    .text {
        width: 22%;
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
            width: 90%;
            font-size: 1.2rem;
            flex-direction: row;
            justify-content: space-around;
        }
        .offreEmploi {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            width: 90%;
            border-width: 0px;
            border-bottom: 1px solid #00ad9a;
            margin-left: 5.2%;
            background-color: transparent;
        }
        .text {
            width: 100%;
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

    }

</style>