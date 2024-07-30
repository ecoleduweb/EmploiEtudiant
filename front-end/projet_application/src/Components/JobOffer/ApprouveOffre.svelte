<script lang="ts">
    import type { JobOffer } from "../../Models/Offre"
    import type { Enterprise } from "../../Models/Enterprise"
    import Button from "../Inputs/Button.svelte"
    import { PUT } from "../../ts/server"
    export let offer: JobOffer
    import OfferDetail from "./OfferDetail.svelte"
    import { onMount } from "svelte"
    import fetchAllEnterprises, { fetchEnterpriseWithId } from "../../Service/EnterpriseService"
    export let handleApproveClick: () => void

    let approbationMessage: string = ""

    let enterprises: { label: string; value: number; }[]
    let enterprise: Enterprise 

    let checked: boolean = false
    let selectedEnterprise: number | undefined;

    const getEnterprises = async () => {
        try {
            enterprises = await fetchAllEnterprises()
        } catch (error) {
        }
    }

    const getEnterprise = async (employerId: number) => {
        try {
            enterprise = await fetchEnterpriseWithId(employerId)
        } catch (error) {
        }
    }

    const approveOffer = async (isApproved: boolean) => {
        try {
            if (!checked) {
                const response = await PUT<any, any>(`/jobOffer/approve/${offer.id}`, 
                {
                    id: offer.id,
                    approbationMessage: approbationMessage,
                    isApproved: isApproved,
                })
            } else {
                const response = await PUT<any, any>(`/jobOffer/approve/${offer.id}?linking=true`,
                {
                    selectedEnterpriseId: selectedEnterprise,
                    approbationMessage: approbationMessage,
                    isApproved: isApproved,
                })
            }

            window.location.reload()
        } catch (error) {
        }
        handleApproveClick()
    }
    
    onMount(async () => 
    {
        await getEnterprise(offer.employerId)
        await getEnterprises()

        selectedEnterprise = enterprises.find((o) => o.label === enterprise.name)?.value;
    })
</script>

<div class="main-div">
    <OfferDetail {offer} />
    <div class="container">
        <div>
            <h5 class="infoTitle">Message d'approbation</h5>
            <textarea
                bind:value={approbationMessage}
                placeholder="Message d'approbation"
                class="input"
            />
        </div>
        {#if enterprise && enterprise.isTemporary}
            <div>
                <input id="LierEmployer" type="checkbox" bind:checked={checked}/>
                <label class="infoChbk" for="LierEmployer">Lier l'employer à une entreprise existante</label>
                <br>
                <br>
                {#if enterprises}
                    <select id="ville" bind:value={selectedEnterprise} class="form-control">
                        {#each enterprises as { label, value }}
                            <option value={value}>{label}</option>
                        {/each}
                    </select>
                    <br>
                    <br>
                {/if}
            </div>
        {/if}
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

    .infoChbk {
        color: black;
        font-size: 1.2vw;
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