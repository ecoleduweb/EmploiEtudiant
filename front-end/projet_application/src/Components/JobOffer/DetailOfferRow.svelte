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

<tr class="offreEmploi" on:click={() => handleModalClick(offer)}>
    <td>{offer.title}</td>
    <td class="desktop-only">{offer.schedules?.map(x => x.description).join(', ')}</td>
    <td class="desktop-only">{offer.deadlineApply}</td>
    <td class="desktop-only">{offer.studyPrograms?.map(x => x.name).join(', ')}</td>
    <td>{offer.enterprise?.name}</td>
    <td><img class="image" src="add.svg" alt="ajouter" /></td>
</tr>

<style scoped>
    .offreEmploi {
        align-items: center;
        color: white;
        width: 100%; 
        border-width: 0px;
        border-bottom: 1px solid #00ad9a;
        background-color: transparent;
        cursor: pointer;
        transition: background-color 0.3s ease;
        display: table-row; 
    }

    .image {
        width: 30px;
        height: 30px;
    }

    tr:hover {
        background-color: #555b66;
        cursor: pointer;
    }

    @media (max-width: 768px) {
        .desktop-only {
            display: none;
        }
        .image {
            width: 30px;
            height: 30px;
        }
    }

    @media (min-width: 769px) {
    }
</style>