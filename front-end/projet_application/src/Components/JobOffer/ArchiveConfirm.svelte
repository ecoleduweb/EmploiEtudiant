<script lang="ts">
    import Modal from "../Common/Modal.svelte"
    import type { JobOffer } from "../../Models/Offre"
    import type { Enterprise } from "../../Models/Enterprise"
    import Button from "../Inputs/Button.svelte"
    import { GET, POST, PUT } from "../../ts/server"
    export let offer: JobOffer
    import OffreEmploi from "./OffreEmploi.svelte"
    export let handleApproveClick: () => void

    let approbationMessage: string = ""

    const approveArchive = async (isApproved: boolean) => {
        if (isApproved) 
        {
            try {
            const response = await PUT<any, any>(`/jobOffer/archive/${offer.id}`)

            // TODO ajouter l'offre à la page sans recharger.
            window.location.reload()
            } catch (error) {
                //console.error("Error approving job offer:", error)
            }
        }

        handleApproveClick()
    }
</script>

<div class="main-div">
    <div class="container">
        <div>
            <h5 class="infoTitle">Voulez-vous vraiment archiver cette offre?</h5>
        </div>
        <div class="button">
            <Button text="Confirmer" onClick={() => approveArchive(true)} />

            <Button text="Refuser" onClick={() => approveArchive(false)} />
        </div>
    </div>
</div>

<style scoped>
    .container {
        width: 100%;
        display: flex;
        flex-direction: column;
        text-align: center;
        justify-content: space-between;
        color: white;
        border-radius: 4px;
        transition: background-color 0.3s ease;
    }

    .infoTitle {
        color: black;
        font-size: 1.6vw;
    }
    
    .button {
        display: flex;
        flex-direction: row;
        justify-content: center;
        gap: 1vw;
    }
    .main-div {
        flex-direction: column;
        margin: auto;
    }
</style>
