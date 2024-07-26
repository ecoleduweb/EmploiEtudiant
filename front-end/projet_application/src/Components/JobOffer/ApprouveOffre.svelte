<script lang="ts">
    import Modal from "../Common/Modal.svelte"
    import type { JobOffer } from "../../Models/Offre"
    import type { Enterprise } from "../../Models/Enterprise"
    import Button from "../Inputs/Button.svelte"
    import { GET, POST, PUT } from "../../ts/server"
    export let offer: JobOffer
    import OfferDetail from "./OfferDetail.svelte"
    import EntrepriseDetails from "./EntrepriseDetails.svelte"
    import { onMount } from "svelte"
    import fetchCity from "../../Service/CityService"
    import { MultiSelect } from "svelte-multiselect"
    export let handleApproveClick: () => void

    let approbationMessage: string = ""

    let enterprises: { label: string; value: number; }[]
    let enterprise: Enterprise 

    let checked: boolean = false
    let selectedEnterprise: number | undefined;

    const handleClick = async () => 
    {
        checked = !checked
    }
    
    const getEnterprises = async () => {
        try {
            const response = await GET<any>("/enterprise/all")
            enterprises = response.map((x: any) => ({"label": x.name, "value": x.id}))
        } catch (error) {
            console.error("Error fetching job offers:", error)
        }
    }

    const getEnterprise = async (employerId: number) => {
        try {
            const response = await GET<any>(
                `/enterprise/employer/${employerId}`
            )
            enterprise = response
        } catch (error) {
            console.error("Error fetching enterprise:", error)
        }
    }

    const approveOffer = async (isApproved: boolean) => {
        try {
            if (checked) {
                const response = await PUT<any, any>(`/jobOffer/approve/${offer.id}`, 
                {
                    id: offer.id,
                    approbationMessage: approbationMessage,
                    isApproved: isApproved,
                })
            } else {
                const response = await PUT<any, any>('/user/linkToExisting',
                {
                    //Trouver quoi mettre comme paramètre
                })
            }

            window.location.reload()
        } catch (error) {
            console.error("Error approving job offer:", error)
        }
        handleApproveClick()
    }

    onMount(async () => 
    {
        await getEnterprise(offer.employerId)
        await getEnterprises()

        selectedEnterprise = enterprises.find((o) => o.label === enterprise.name)?.value;
    })

    //À faire:
    //Faire le back-end
    //Faire communiquer le front-end avec le back-end

    //Problème:
    //Trouver comment avoir l'utilisateur avec l'offre/emplois
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
                <input id="LierEmployer" type="checkbox" on:click={handleClick}/>
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