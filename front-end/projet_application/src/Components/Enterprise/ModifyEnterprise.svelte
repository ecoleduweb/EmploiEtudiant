<script lang="ts">
    import Modal from "../Common/Modal.svelte"
    import { MultiSelect } from "svelte-multiselect";
    import CreateEditEnterprise from "../JobOffer/CreateEditEnterprise.svelte"
    import type { Enterprise } from "../../Models/Enterprise"
    import { getCurrentUserEnterprise } from "../../Service/EnterpriseService"
    import { onMount } from "svelte"
    import { entrepriseSchema } from "../../FormValidations/JobOffer"
    import { ValidationError } from "yup"
    import { extractErrors } from "../../ts/utils"
    import Button from "../Inputs/Button.svelte"
    import { PUT } from "../../ts/server"
    import fetchCity from "../../Service/CityService"
    
    export let handleCloseClick: () => void
    let enterprise: Enterprise
    let errorsEnterprise: any = [];
    let cityOptions: { label: string; value: number }[] = [];
    let selectedCity: any
    let cityFromEnterprise: any = []

    function formatPhoneNumber() {
        let phone = enterprise.phone.replace(/\D/g, ''); // Supprime tous les caractères non numériques

        if (phone.length === 10) {
            // Format pour les numéros à 10 chiffres
            enterprise.phone = `(${phone.slice(0, 3)}) ${phone.slice(3, 6)}-${phone.slice(6)}`;
        } else if (phone.length === 7) {
            // Format pour les numéros à 7 chiffres
            enterprise.phone = `${phone.slice(0, 3)}-${phone.slice(3)}`;
        }
    }

    let prepareAndVerifyIfValid = async () => {
        if (enterprise !== null) {
            try {
                enterprise.cityId = selectedCity?.value != undefined ? selectedCity?.value : -1
                await entrepriseSchema.validate(enterprise, {abortEarly: false})

                return enterprise
            }
            catch (err) {
                if (err instanceof ValidationError) {
                    errorsEnterprise = extractErrors(err)
                }
            }
        }
    }

    let handleSubmit = async () => 
    {
        const validatedData = await prepareAndVerifyIfValid()
        if (validatedData != undefined) {
            const response = await PUT<any, any>(`/enterprise/${validatedData?.id}`, {...enterprise, cityId: selectedCity.value})

            if (response) {
                enterprise.cityId = selectedCity.value
                handleCloseClick()
            } 
        }
    }

    const setOwnEnterprise = async () => {
        selectedCity = cityOptions.find(
            (ville) => ville.value === enterprise.cityId,
        )
    }
            
     
    onMount(async () => 
    {
        enterprise = await getCurrentUserEnterprise()
        cityOptions = await fetchCity()

        setOwnEnterprise()
    })
</script>

<Modal widthFix={true} {handleCloseClick}>
    {#if enterprise != undefined && cityOptions != undefined}
        <div class="modalContent">
            <div class="form-group-vertical">
                <label for="title">Nom*</label>
                <br>
                <input
                    type="text"
                    bind:value={enterprise.name}
                    class="form-control"
                    id="titre"
                    readonly={false}
                />
            </div>
            <p class="errors-input">
                {#if errorsEnterprise.name}{errorsEnterprise.name}{/if}
            </p>
            <div class="form-group-vertical">
                <label for="schedule">Adresse*</label>
                <br>
                <input
                    type="text"
                    bind:value={enterprise.address}
                    class="form-control"
                    id="address"
                    readonly={false}
                />
            </div>
            <p class="errors-input">
                {#if errorsEnterprise.address}{errorsEnterprise.address}{/if}
            </p>
            <div class="form-group-vertical">
                <label for="lieu">Courriel*</label>
                <br>
                <input
                    type="text"
                    bind:value={enterprise.email}
                    class="form-control"
                    id="email"
                    readonly={false}
                />
            </div>
            <p class="errors-input">
                {#if errorsEnterprise.email}{errorsEnterprise.email}{/if}
            </p>
            <div class="form-group-vertical">
                <label for="lieu">Téléphone*</label>
                <br>
                <input
                    type="text"
                    bind:value={enterprise.phone}
                    on:blur={formatPhoneNumber}
                    class="form-control"
                    id="phone"
                    readonly={false}
                />
            </div>
            <p class="errors-input">
                {#if errorsEnterprise.phone}{errorsEnterprise.phone}{/if}
            </p>
            <div class="form-group-vertical">
                <label for="lieu">Ville*</label>
                <br>
                {#if cityOptions.length === 0 && selectedCity}
                    <p>Chargement des villes...</p>
                {:else}
                    <MultiSelect
                        id="ville"
                        options={cityOptions}
                        closeDropdownOnSelect={true}
                        maxSelect={1}
                        placeholder="Choisir ville..."
                        bind:value={selectedCity}
                        bind:selected={cityFromEnterprise}
                    />
                {/if}
            </div>

            <div class="accept-Condition">
                <div class="send">
                    <Button
                        text="Envoyer"
                        onClick={handleSubmit}
                    />
                </div>
            </div>
        </div>
    {/if}
</Modal>


<style>
    .modalContent {
        display: flex;
        flex-direction: column;

        justify-content: center;
        justify-items: center;

        align-items: center;
        align-self: center;
    }
    label {
        display: block;
        margin-bottom: 0.26vw;
    }
    .form-group-vertical {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        width: 80%;
        margin: 0.8vw;
    }
    .errors-input {
        color: red;
        font-size: 0.8em;
    }
    .accept-Condition {
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        width: 100%;
    }
</style>
