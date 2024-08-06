<script lang="ts">
    import Modal from "../Common/Modal.svelte"
    import type { JobOffer } from "../../Models/Offre"
    import type { Enterprise } from "../../Models/Enterprise"
    import Button from "../Inputs/Button.svelte"
    import { GET, POST, PUT } from "../../ts/server"
    export let offer: JobOffer
    export let enterprise: Enterprise
    import OfferDetail from "./OfferDetail.svelte"
    export let handleApproveClick: () => void

    let approbationMessage: string = ""

    const approveOffer = async (isApproved: boolean) => {
        try {
            const response = await PUT<any, any>(`/jobOffer/approve/${offer.id}`, 
            {
                id: offer.id,
                approbationMessage: approbationMessage,
                isApproved: isApproved,
            })
        } catch (error) {
            console.error("Error approving job offer:", error)
        }
        handleApproveClick()
    }
</script>

<div class="main-div">
    <OfferDetail {offer} {enterprise} />
    <div class="container">
        <div>
            <h5 class="infoTitle">Message d'approbation</h5>
            <textarea
                bind:value={approbationMessage}
                placeholder="Message d'approbation"
                class="input"
            />
        </div>
        <div class="button">
            <Button text="Approuver" onClick={() => approveOffer(true)} />

            <Button text="Refuser" onClick={() => approveOffer(false)} />
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

    .input {
        width: 80%;
        height: 7vw;
        border-radius: 4px;
        border: 1px solid #00ad9a;
        background-color: transparent;
        margin-bottom: 1.5vw;
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
