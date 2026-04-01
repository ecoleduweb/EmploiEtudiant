<script lang="ts">
    import type { Enterprise } from "../../Models/Enterprise"
    import Button from "../Inputs/Button.svelte"
    import { PUT } from "../../ts/server"
    import OfferDetail from "./OfferDetail.svelte"
    import { onMount } from "svelte"
    import fetchAllEnterprises, {
        fetchEnterpriseWithId,
    } from "../../Service/EnterpriseService"
    import EntrepriseDetails from "./EntrepriseDetails.svelte"
    import type { Option } from "$lib/interfaces"
    import type { JobOfferDetails } from "../../Models/JobOfferDetails"
    import fetchCity from "../../Service/CityService"

    interface Props {
        handleApproveClick: () => void
        offer: JobOfferDetails
    }

    let { handleApproveClick, offer }: Props = $props()
    let approbationMessage: string = $state("")

    let enterprises: { label: string; value: number }[] = $state([])
    let enterprise: Enterprise | undefined = $state()

    let selectedEnterpriseId: number | undefined = $state()
    let cities: Option[] | null = $state(null)

    const getEnterprises = async () => {
        try {
            enterprises = await fetchAllEnterprises()
        } catch (error) {
            console.error(error)
        }
    }

    const getEnterprise = async (employerId: number) => {
        try {
            enterprise = await fetchEnterpriseWithId(employerId)
        } catch (error) {
            console.error(error)
        }
    }

    const approveOffer = async (isApproved: boolean) => {
        try {
            const payload = {
                id: offer.id,
                selectedEnterpriseId: isApproved ? selectedEnterpriseId : null,
                approbationMessage: approbationMessage,
                isApproved: isApproved,
            }

            await PUT<any, any>(`/jobOffer/approve/${offer.id}`, payload)

            window.location.reload()
        } catch (error) {
            console.error("Erreur lors de l'approbation", error)
        }
        handleApproveClick()
    }

    onMount(async () => {
        cities = await fetchCity()
        await getEnterprise(offer.employerId)
        await getEnterprises()
        if (enterprise) {
            selectedEnterpriseId = enterprise.id
        }
    })
</script>

<div class="main-div">
    <OfferDetail {offer} />
    <div class="container">
        <div class="horitonzal">
            <div>
                <h5 class="infoTitle">Message d'approbation</h5>
                <textarea
                    bind:value={approbationMessage}
                    placeholder="Message d'approbation"
                    class="input"
                ></textarea>
            </div>
            {#if enterprise && enterprise.isTemporary && cities}
                <div class="detail-enterprise">
                    <h3>Détails de l'entreprise de l'utilisateur</h3>
                    <EntrepriseDetails
                        {enterprise}
                        selectedCity={cities.filter(
                            (x) => x.value == enterprise!.cityId,
                        )}
                    />
                    <hr />
                    <br />
                    {#if enterprises}
                        <select
                            id="entreprise-select"
                            bind:value={selectedEnterpriseId}
                            class="form-control"
                        >
                            {#each enterprises as { label, value }}
                                <option {value}>
                                    {#if value == enterprise.id}
                                        *Ajouter*
                                    {/if}
                                    {label}
                                </option>
                            {/each}
                        </select>
                        <br />
                        <br />
                    {/if}
                </div>
            {/if}
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

    .horitonzal {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
    }

    .detail-enterprise {
        margin-top: 5vh;
    }

    .infoTitle {
        font-size: 1.6vw;
    }

    h3,
    .infoTitle {
        color: black;
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

    @media (max-width: 768px) {
        .button {
            margin-bottom: 10vw;
        }
    }
</style>
