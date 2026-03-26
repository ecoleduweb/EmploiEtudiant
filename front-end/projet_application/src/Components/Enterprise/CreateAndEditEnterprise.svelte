<script lang="ts">
    import Button from "../Inputs/Button.svelte"
    import type { Enterprise } from "../../Models/Enterprise"
    import MultiSelect from "svelte-multiselect"
    import { onMount, untrack } from "svelte"
    import fetchCity from "../../Service/CityService"
    import { entrepriseSchema } from "../../FormValidations/JobOffer"
    import { ValidationError } from "yup"
    import { extractErrors } from "../../ts/utils"

    type Props = {
        enterprise?: Enterprise
        handleApproveClick: (enterprise: Enterprise | void) => void
    }

    let {
        enterprise: enterpriseProp = {
            name: "",
            id: -1,
            email: "",
            phone: "",
            address: "",
            cityId: 0,
            isTemporary: false,
        },
        handleApproveClick,
    }: Props = $props()

    let enterprise = $state({ ...enterpriseProp })
    let errorsEnterprise: any = $state([])
    let savedName = $state(enterpriseProp.name)
    let isNewEnterprise = $derived((enterprise.id ?? -1) <= 0)

    let selectedCity: { label: string; value: number } | null = $state(null)
    let cityFromSelectedEnterprise: { label: string; value: number }[] = $state(
        [],
    )
    let cityOptions: { label: string; value: number }[] = $state([])

    const getAllCities = async () => {
        try {
            cityOptions = await fetchCity()

            if (enterprise.cityId) {
                const found = cityOptions.find(
                    (c) => c.value === enterprise.cityId,
                )
                if (found) {
                    selectedCity = found
                    cityFromSelectedEnterprise = [found]
                }
            }
        } catch (error) {
            console.error("Error fetching cities:", error)
        }
    }

    $effect(() => {
        if (selectedCity) {
            enterprise.cityId = selectedCity.value
        }
    })

    const prepareAndVerifyIfValid = async () => {
        if (enterprise !== null) {
            try {
                enterprise.cityId =
                    selectedCity?.value !== undefined ? selectedCity.value : -1
                await entrepriseSchema.validate(enterprise, {
                    abortEarly: false,
                })
                return enterprise
            } catch (err) {
                if (err instanceof ValidationError) {
                    errorsEnterprise = extractErrors(err)
                }
            }
        }
    }

    const handleSubmit = async () => {
        const validatedData = await prepareAndVerifyIfValid()
        if (validatedData) {
            handleApproveClick(validatedData)
        }
    }

    onMount(getAllCities)
</script>

<div class="main-div">
    <div class="container">
        <h5 class="infoTitle">
            {isNewEnterprise
                ? "Veuillez choisir un nouveau nom pour la nouvelle entreprise"
                : "Veuillez choisir un nouveau nom pour l'entreprise suivante: " +
                  savedName}
        </h5>

        {#if enterprise && cityOptions}
            <div class="modalContent">
                <div class="form-group-vertical">
                    <label for="enterprise-name"> "Nom*" </label>
                    <input
                        id="enterprise-name"
                        type="text"
                        bind:value={enterprise.name}
                        class="form-control"
                    />
                    <p class="errors-input">
                        {#if errorsEnterprise.name}{errorsEnterprise.name}{/if}
                    </p>
                </div>

                <div class="form-group-vertical">
                    <label for="enterprise-address"> "Adresse*" </label>
                    <input
                        id="enterprise-address"
                        type="text"
                        bind:value={enterprise.address}
                        class="form-control"
                    />
                    <p class="errors-input">
                        {#if errorsEnterprise.address}{errorsEnterprise.address}{/if}
                    </p>
                </div>

                <div class="form-group-vertical">
                    <label for="enterprise-email"> "Courriel*" </label>
                    <input
                        id="enterprise-email"
                        type="text"
                        bind:value={enterprise.email}
                        class="form-control"
                    />
                    <p class="errors-input">
                        {#if errorsEnterprise.email}{errorsEnterprise.email}{/if}
                    </p>
                </div>

                <div class="form-group-vertical">
                    <label for="enterprise-phone"> "Téléphone*" </label>
                    <input
                        id="enterprise-phone"
                        type="text"
                        bind:value={enterprise.phone}
                        class="form-control"
                    />
                    <p class="errors-input">
                        {#if errorsEnterprise.phone}{errorsEnterprise.phone}{/if}
                    </p>
                </div>

                <div class="form-group-vertical">
                    <label for="enterprise-city"> "Ville*" </label>

                    {#if cityOptions.length === 0}
                        <p>Chargement des villes...</p>
                    {:else}
                        <MultiSelect
                            id="enterprise-city"
                            options={cityOptions}
                            bind:value={selectedCity}
                            bind:selected={cityFromSelectedEnterprise}
                            closeDropdownOnSelect={true}
                            maxSelect={1}
                            placeholder="Choisir ville..."
                        />
                    {/if}
                    <p class="errors-input">
                        {#if errorsEnterprise.cityId}{errorsEnterprise.cityId}{/if}
                    </p>
                </div>
            </div>
        {/if}

        <div class="button">
            <Button
                text={isNewEnterprise ? "Créer" : "Modifier"}
                onClick={handleSubmit}
            />

            <Button
                text="Annuler"
                onClick={() => handleApproveClick(undefined)}
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
        color: black;
        border-radius: 4px;
        transition: background-color 0.3s ease;
    }

    .modalContent {
        display: flex;
        flex-direction: column;
        align-items: center;
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

    .infoTitle {
        color: black;
    }

    .form-group-vertical {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        width: 55%;
        margin: 0.8vw;
    }

    .errors-input {
        color: red;
        font-size: 0.8em;
        margin-top: 0.2vw;
    }

    @media (max-width: 768px) {
        .infoTitle {
            font-size: 4vw;
        }
    }
</style>
