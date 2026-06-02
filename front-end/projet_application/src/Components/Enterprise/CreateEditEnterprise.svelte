<script lang="ts">
    import Button from "../Inputs/Button.svelte"
    import type { Enterprise } from "../../Models/Enterprise"
    import MultiSelect from "svelte-multiselect"
    import { onMount } from "svelte"
    import {
        enterpriseTemplate,
        validateForm,
    } from "../../FormValidations/Enterprise"
    import type { Option } from "../../Models/Option"
    import { fetchCitiesAsOptions } from "../../Service/CityService"
    import { upsertEnterprise } from "../../Service/EnterpriseService"
    import { fetchUsersAsOptions } from "../../Service/UserService"
    import LoadingSpinner from "../Common/LoadingSpinner.svelte"
    import { currentUser } from "$lib"

    type Props = {
        enterpriseToEdit?: Enterprise
        onApproveClick: (enterprise: Enterprise) => void
    }

    let props: Props = $props()
    const isModerator = $currentUser?.isModerator ?? false
    const isEnterpriseEdit = $derived(!!props.enterpriseToEdit)
    const { onApproveClick } = props

    let enterprise = $state(enterpriseTemplate.generate())
    if (props.enterpriseToEdit) {
        Object.assign(enterprise, props.enterpriseToEdit)
    }

    let selectedCities: Option[] = $state([])
    let cityOptions: Option[] = $state([])
    let selectedUsers: Option[] = $state([])
    let userOptions: Option[] = $state([])
    let isFetchingOptions = $state(true)

    $effect(() => {
        if (isFetchingOptions || selectedCities.length === 0) return
        enterprise.cityId = selectedCities[0].value
        setFields("cityId", enterprise.cityId)
        $errors["cityId"] = undefined
    })

    const handleSubmit = async () => {
        try {
            const upsertedEnterprise = await upsertEnterprise(enterprise)
            onApproveClick(upsertedEnterprise)
        } catch (error) {
            console.error("Error occurred while upserting enterprise:", error)
        }
    }

    onMount(async () => {
        isFetchingOptions = true
        cityOptions = await fetchCitiesAsOptions()
        if (isEnterpriseEdit && enterprise.city) {
            selectedCities = [
                {
                    label: enterprise.city.city,
                    value: enterprise.city.id,
                },
            ]
        }
        if (isModerator) {
            userOptions = await fetchUsersAsOptions()
            selectedUsers =
                enterprise.users?.map((user) => ({
                    label: `${user.firstName} ${user.lastName} (${user.email})`,
                    value: user.id,
                })) ?? []
        }
        isFetchingOptions = false
    })

    const { form, errors, setFields, isSubmitting } = validateForm(
        handleSubmit,
        enterprise,
    )
</script>

<div class="main-div">
    <div class="container">
        <h5 class="infoTitle">
            {isEnterpriseEdit
                ? "Modification de l'entreprise"
                : "Nouvelle entreprise"}
        </h5>
        <form use:form class="form">
            <div class="modalContent">
                <div class="form-group-vertical">
                    <label for="enterprise-name"> Nom* </label>
                    <input
                        id="enterprise-name"
                        type="text"
                        name="name"
                        bind:value={enterprise.name}
                        class="form-control"
                    />
                    <p class="errors-input">
                        {#if $errors.name}{$errors.name}{/if}
                    </p>
                </div>

                <div class="form-group-vertical">
                    <label for="enterprise-address"> Adresse* </label>
                    <input
                        id="enterprise-address"
                        type="text"
                        name="address"
                        bind:value={enterprise.address}
                        class="form-control"
                    />
                    <p class="errors-input">
                        {#if $errors.address}{$errors.address}{/if}
                    </p>
                </div>

                <div class="form-group-vertical">
                    <label for="enterprise-email"> Courriel* </label>
                    <input
                        id="enterprise-email"
                        type="text"
                        name="email"
                        bind:value={enterprise.email}
                        class="form-control"
                    />
                    <p class="errors-input">
                        {#if $errors.email}{$errors.email}{/if}
                    </p>
                </div>

                <div class="form-group-vertical">
                    <label for="enterprise-phone"> Téléphone* </label>
                    <input
                        id="enterprise-phone"
                        type="text"
                        name="phone"
                        bind:value={enterprise.phone}
                        class="form-control"
                    />
                    <p class="errors-input">
                        {#if $errors.phone}{$errors.phone}{/if}
                    </p>
                </div>

                <div class="form-group-vertical">
                    <label for="enterprise-city"> Ville* </label>

                    <MultiSelect
                        loading={isFetchingOptions}
                        id="enterprise-city"
                        options={cityOptions as any[]}
                        bind:selected={selectedCities as any[]}
                        closeDropdownOnSelect={true}
                        name="cityId"
                        maxSelect={1}
                        placeholder="Choisir ville..."
                    />
                    <p class="errors-input">
                        {#if $errors.cityId}{$errors.cityId}{/if}
                    </p>
                </div>
                {#if isModerator}
                    <div class="form-group-vertical">
                        <label for="enterprise-city"> Utilisateurs </label>

                        <MultiSelect
                            loading={isFetchingOptions}
                            id="enterprise-city"
                            options={userOptions as any[]}
                            bind:selected={selectedUsers as any[]}
                            closeDropdownOnSelect={true}
                            name="selectedUsers"
                            placeholder="Choisir les utilsateurs de l'entreprise..."
                        />
                        <p class="errors-input">
                            {#if $errors.cityId}{$errors.cityId}{/if}
                        </p>
                    </div>
                {/if}
            </div>

            <div class="button">
                <div class="send">
                    {#if $isSubmitting}
                        <LoadingSpinner />
                    {:else}
                        <Button
                            submit={true}
                            text="Envoyer"
                            onClick={() => handleSubmit()}
                        />
                    {/if}
                </div>
            </div>
        </form>
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
