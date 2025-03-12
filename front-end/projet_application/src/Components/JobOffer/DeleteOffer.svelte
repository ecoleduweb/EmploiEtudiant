<script lang="ts">
    import Modal from "../Common/Modal.svelte"
    import type { JobOffer } from "../../Models/Offre"
    import type { Enterprise } from "../../Models/Enterprise"
    import Button from "../Inputs/Button.svelte"
    import { DELETE, GET, POST, PUT } from "../../ts/server"
    export let offer: JobOffer
    export let handleDeleteClick: () => void

    let approbationMessage: string = ""

    const deleteOffer = async (tobeDeleted: boolean) => {
        if (tobeDeleted) 
        {
            try {
            const response = await DELETE(`/jobOffer/delete/${offer.id}`)
            window.location.reload()
            } catch (error) {
                console.log(error)
            }
        }

        handleDeleteClick()
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
