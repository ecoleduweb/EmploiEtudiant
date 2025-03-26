<script lang="ts">
    import type { JobOffer } from "../../Models/Offre"
    import Button from "../Inputs/Button.svelte"
    import { DELETE } from "../../ts/server"
    export let offer: JobOffer
    export const isDeleted = false;
    export let handleDeleteClick: (idJobOffer: number | null) => void

    const deleteOffer = async (isDeleted: boolean) => {
        if (isDeleted) 
        {
            try {
            await DELETE(`/jobOffer/delete/${offer.id}`)
            handleDeleteClick(offer.id)
            } catch (error) {
                console.error("Erreur lors de la suppression :",error)
            }
        }
        handleDeleteClick(null)
    }
</script>

<div class="main-div">
    <div class="container">
        <div>
            <h5 class="infoTitle">Voulez-vous vraiment supprimer cette offre?</h5>
        </div>
        <div class="button">
            <Button text="Confirmer" onClick={() => deleteOffer(true)} />

            <Button text="Refuser" onClick={() => deleteOffer(false)} />
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

    @media (max-width: 768px) {
        .infoTitle {
            font-size: 4vw;
        }
    }


</style>
