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
<!--
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
</button>-->


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
    
    .image {
        width: 30px;
        height: 30px;
    }

    .info-mobile {
        display: none;
    }

    tr:hover {
        background-color: hsl(173, 100%, 34%, 50%); /* Effet survol optionnel */
        cursor: pointer;
    }

    .image:hover {
        background-color: hsl(185, 80%, 16%);
    }
/*
    @media (max-width: 768px) {
        .info {
            display: none;
        }
        .info-mobile {
            display: flex;
            flex-direction: row;
            
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
        .image {
            width: 30px;
            height: 30px;
        }*/

    @media (max-width: 768px) {
        .desktop-only {
            display: none;
        }
        
        /* Si vous souhaitez que seules les 3 premières cellules soient visibles */
        .offreEmploi td:nth-child(n+4) {
            display: none;
        }
        
        /* Style pour les cellules mobiles */
        .mobile-content, .mobile-employer, .mobile-details {
            display: table-cell; /* Assure que les cellules sont traitées comme des cellules de tableau */
        }
        
        .mobile-content {
            width: 60%; /* Ajustez selon vos besoins */
        }
        
        .mobile-employer {
            width: 30%; /* Ajustez selon vos besoins */
        }
        
        .mobile-details {
            width: 10%; /* Ajustez selon vos besoins */
            text-align: left;
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