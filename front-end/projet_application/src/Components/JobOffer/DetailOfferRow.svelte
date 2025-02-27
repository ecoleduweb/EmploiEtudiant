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
    <!-- Section mobile-->
    <td class="mobile-content">{offer.title}</td>
    <td class="mobile-employer">{offer.enterprise?.name}</td>
    <td class="mobile-details"><img class="image" src="add.svg" alt="ajouter" /></td>

    <!-- Section desktop-->
    <td class="info">{offer.title}</td>
    <td class="info">{offer.schedules?.map(x => x.description).join(', ')}</td>
    <td class="info">{offer.deadlineApply}</td>
    <td class="info">{offer.studyPrograms?.map(x => x.name).join(', ')}</td>
    <td class="info">{offer.enterprise?.name}</td>
    <td><img class="info image" src="add.svg" alt="ajouter" /></td>
</tr>

<style scoped>
    .offreEmploi {
        align-items: center;
        color: white;
        width: 100%; 
        border-width: 0px;
        border-bottom: 1px solid #00ad9a;
        background-color: transparent;
        display: table-row; 
    }

    .image {
        width: 30px;
        height: 30px;
    }

    tr:hover {
        background-color: hsl(173, 100%, 34%, 50%); /* Effet survol optionnel */
        cursor: pointer;
    }

    .image:hover {
        background-color: hsl(185, 80%, 16%);
    }

    @media (max-width: 768px) {
        /* Si vous souhaitez que seules les 3 premières cellules soient visibles */
        .offreEmploi td:nth-child(n+4) {
            display: none;
        }
        
        /* Style pour les cellules mobiles */
        .mobile-content, .mobile-employer, .mobile-details {
            display: table-cell; /* Assure que les cellules sont traitées comme des cellules de tableau */
        }
        .image {
            width: 30px;
            height: 30px;
        }
    }

    @media (min-width: 769px) {
        /* En mode desktop, cachez les cellules mobiles */
        .mobile-content, .mobile-employer, .mobile-details {
            display: none;
        }
    }




</style>