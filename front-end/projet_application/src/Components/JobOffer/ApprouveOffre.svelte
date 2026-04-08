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
            alert(
                "Une erreur est survenue lors de l'approbation de l'offre.Veuillez réessayer.",
            )
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
    <OfferDetail {offer} showShareButtons={false} />
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

                    {#if enterprises}
                        <select
                            id="entreprise-select"
                            bind:value={selectedEnterpriseId}
                            class="form-control enterprise-select"
                        >
                            {#each enterprises as { label, value }}
                                <option
                                    {value}
                                    class={value == enterprise.id
                                        ? "option-new"
                                        : "option-existing"}
                                    style={value == enterprise.id
                                        ? "color: #00ad9a; font-weight: bold;"
                                        : "color: #555;"}
                                >
                                    {#if value == enterprise.id}
                                        + [Nouvelle entreprise] {label}
                                    {:else}
                                        {label}
                                    {/if}
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

    .enterprise-select {
        width: 100%;
        border: 2px solid #00ad9a;
        border-radius: 6px;
        background-color: white;
        color: #333;
        font-size: 0.875rem;
        cursor: pointer;
        outline: none;
        transition: box-shadow 0.2s;
    }

    .enterprise-select:focus {
        box-shadow: 0 0 8px rgba(0, 173, 154, 0.3);
    }

    .option-new {
        background-color: #e6f7f5;
        color: #00ad9a;
        font-weight: bold;
    }

    .option-existing {
        color: #444;
    }

    @media (max-width: 768px) {
        .button {
            margin-bottom: 10vw;
        }
    }
</style>
