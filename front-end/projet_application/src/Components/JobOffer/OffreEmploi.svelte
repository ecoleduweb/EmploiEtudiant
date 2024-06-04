<script lang="ts">
    import type { JobOffer } from "../../Models/Offre"
    import type { Enterprise } from "../../Models/Enterprise"
    import { GET } from "../../ts/server"
    import { onMount } from "svelte"
    export let offer: JobOffer

    let enterprise: Enterprise 
    const getEnterprises = async (employerId: number) => {
        try {
            const response = await GET<any>(
                `/enterprise/employer/${employerId}`
            )
            enterprise = response
        } catch (error) {
            console.error("Error fetching enterprise:", error)
        }
    }
    onMount(async () => {
        getEnterprises(offer.employerId)
        const response = await GET<any>(
            `/offerProgram/${offer.id}`,
        )
        try {
            programmeSelected = response
                .map((programId: number) => {
                    let program = programmesOption.find(
                        (p) => p.value === programId,
                    )
                    return program
                        ? { label: program.label, value: program.value }
                        : null
                })
                .filter((p: number) => p !== null) // Filtrer les éventuels null si aucun programme n'est trouvé
        } catch (error) {
            console.error("Error fetching program:", error)
        }
    })
    let programmeSelected = [] as any
    let programmesOption = [
        { label: "Design d'intérieur", value: 1 },
        { label: "Éducation à l'enfance", value: 2 },
        { label: "Gestion et intervention en loisir", value: 3 },
        { label: "Graphisme", value: 4 },
        { label: "Informatique", value: 5 },
        { label: "Inhalothérapie", value: 6 },
        { label: "Pharmacie", value: 7 },
        { label: "Soins infirmiers", value: 8 },
        { label: "Arts visuels", value: 9 },
        { label: "Sciences de la nature", value: 10 },
        { label: "Sciences humaines", value: 11 },
        { label: "Tous les programmes", value: 12 },
    ]
</script>

<div class="container">
    <div class="titleContainer">
        <h3 class="title">{offer.title}</h3>
        {#if enterprise}
            <h4 class="subtitle">Chez {enterprise.name}</h4>
        {/if}
    </div>
    <div class="info">
        <h5 class="infoTitle">Type de poste</h5>
        <p class="text">{offer.title}</p>
        <h5 class="infoTitle">Adresse du lieu de travail</h5>
        <p class="text">{offer.address}</p>
        <h5 class="infoTitle">Date de début</h5>
        <p class="text">{offer.offerDebut}</p>
        <h5 class="infoTitle">Date d'entrée en fonction</h5>
        <p class="text">{offer.dateEntryOffice}</p>
        <h5 class="infoTitle">Date limite pour postuler</h5>
        <p class="text">{offer.deadlineApply}</p>
        <h5 class="infoTitle">Salaire</h5>
        <p class="text">{offer.salary}</p>
        <h5 class="infoTitle">Heure par semaine</h5>
        <p class="text">{offer.hoursPerWeek}</p>
        <h5 class="infoTitle">Stage ?</h5>
        <p class="text">{offer.internship ? "Oui" : "Non"}</p>
        <h5 class="infoTitle">Programme</h5>
        <p class="text">{programmeSelected.map((p) => p.label).join(", ")}</p>
        <h5 class="infoTitle">Description du poste</h5>
        <p class="text">{offer.description}</p>
        <h5 class="infoTitle">Adresse URL vers l'offre d'emploi détaillé</h5>
        <p class="text">{offer.offerLink}</p>
        <h5 class="infoTitle">Où envoyer votre candidature</h5>
        <p class="text">{offer.email}</p>
    </div>
</div>

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
    .subtitle {
        font-size: 1.5rem;
        margin: 0px;
        margin-bottom: 2.25vw;
        color: black;
    }
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
        max-height: 700px;
        overflow-y: auto;
    }
</style>
