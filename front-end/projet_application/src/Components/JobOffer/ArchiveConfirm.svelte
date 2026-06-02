<script lang="ts">
    import type { JobOffer } from "../../Models/Offre"
    import Button from "../Inputs/Button.svelte"
    import { toggleArchive } from "../../Service/JobOfferService"
    interface Props {
        offer: JobOffer
        onToggleArchiveClick: (jobOffer: JobOffer | undefined) => void
    }

    let { offer, onToggleArchiveClick }: Props = $props()

    const toggleArchiveStatus = async () => {
        {
            const updated = await toggleArchive(offer.id)
            onToggleArchiveClick(updated)
        }
    }
</script>

<div class="main-div">
    <div class="container">
        <div>
            <h5 class="infoTitle">
                Voulez-vous vraiment archiver cette offre?
            </h5>
        </div>
        <div class="button">
            <Button text="Confirmer" onClick={() => toggleArchiveStatus()} />

            <Button
                text="Refuser"
                onClick={() => onToggleArchiveClick(undefined)}
            />
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
