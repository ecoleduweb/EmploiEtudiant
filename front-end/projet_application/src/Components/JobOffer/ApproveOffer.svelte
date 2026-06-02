<script lang="ts">
    import Button from "../Inputs/Button.svelte"
    import OfferDetail from "./OfferDetail.svelte"
    import { onMount } from "svelte"
    import { fetchEnterprisesAsOptions } from "../../Service/EnterpriseService"
    import EntrepriseDetails from "./EntrepriseDetails.svelte"
    import type { JobOffer } from "../../Models/Offre"
    import type { Option } from "../../Models/Option"
    import MultiSelect from "svelte-multiselect"
    import { approveJobOffer } from "../../Service/JobOfferService"

    interface Props {
        onApprove: (jobOffer: JobOffer) => void
        offer: JobOffer
    }

    let { onApprove: handleApproveClick, offer }: Props = $props()
    let isFetchingOptions = $state(true)
    let isEnterpriseTemporary: boolean = $derived(
        offer.enterprise?.isTemporary ?? false,
    )
    let approbationMessage: string = $state("")
    let enterpriseOptions: Option[] = $state([])
    let selectedEnterprises: Option[] = $state([])

    const approveOffer = async (isApproved: boolean) => {
        const approved = await approveJobOffer(
            offer.id,
            isApproved,
            approbationMessage,
            selectedEnterprises.at(0)?.value ?? undefined,
        )
        handleApproveClick(approved)
    }

    onMount(async () => {
        isFetchingOptions = true
        if (isEnterpriseTemporary) {
            enterpriseOptions = await fetchEnterprisesAsOptions()
            // On met l'entreprise temporaire comme sélectionné par défaut
        }
        // On set l'entreprise temporaire comme sélectionné par défaut si elle existe pour pouvoir l'envoyer sur approbation
        if (offer.enterprise) {
            const index = enterpriseOptions.findIndex(
                (x) => x.value === offer.enterprise?.id,
            )
            const selectedEnterprise = {
                label: `***${offer.enterprise.name}***`,
                value: offer.enterprise.id,
            }
            selectedEnterprises = [selectedEnterprise]
            enterpriseOptions[index] = selectedEnterprise
        }
        isFetchingOptions = false
    })
</script>

<div class="main-div">
    <OfferDetail {offer} />
    {#if isEnterpriseTemporary}
        <div class="detail-enterprise">
            <h3>Détails de l'entreprise de l'utilisateur</h3>
            <EntrepriseDetails enterprise={offer.enterprise!} />
            <hr />
            <MultiSelect
                loading={isFetchingOptions}
                id="enterprise"
                name="enterprises"
                options={enterpriseOptions as any[]}
                closeDropdownOnSelect={true}
                maxSelect={1}
                placeholder="Choisir une entreprise..."
                bind:selected={selectedEnterprises}
            />
        </div>
    {/if}
    <div class="container">
        <div class="horitonzal">
            <div class="approval-section">
                <h5 class="infoTitle">Message d'approbation</h5>
                <textarea
                    bind:value={approbationMessage}
                    placeholder="Message d'approbation"
                    class="input"
                ></textarea>
            </div>
        </div>

        <div class="button">
            <Button text="Approuver" onClick={() => approveOffer(true)} />
            <Button text="Refuser" onClick={() => approveOffer(false)} />
        </div>
    </div>
</div>

<style scoped>
    .horitonzal {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }
    .approval-section,
    .detail-enterprise {
        flex: 1;
        text-align: left;
    }
    .detail-enterprise {
        margin-top: 3vh;
    }

    .infoTitle {
        font-size: 1.6vw;
    }

    h3,
    .infoTitle {
        color: black;
    }

    textarea {
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

    @media (max-width: 768px) {
        .button {
            margin-bottom: 10vw;
        }
    }
</style>
