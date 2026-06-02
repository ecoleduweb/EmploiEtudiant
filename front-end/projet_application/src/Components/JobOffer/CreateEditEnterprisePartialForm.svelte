<script lang="ts">
    import { MultiSelect } from "svelte-multiselect"
    import { onMount } from "svelte"
    import { fetchCitiesAsOptions } from "../../Service/CityService"
    import type { Option } from "../../Models/Option"
    import { jobOfferTemplate } from "../../FormValidations/JobOffer"

    interface Props {
        enterprise: any
        errors: any
    }

    let { enterprise = $bindable(), errors }: Props = $props()

    let cityOptions: Option[] = $state([])
    $effect(() => {
        const cities = selectedCities.map((opt) => ({
            id: opt.value as number,
            description: opt.label,
        }))
        if (enterprise) {
            enterprise.cityId = cities[0]?.id
        }
    })
    let isFetchingOptions = $state(true)
    const isCreatingEnterprise = $derived(enterprise?.id <= 0)

    let selectedCities: Option[] = $state([])

    onMount(async () => {
        isFetchingOptions = true
        if (isCreatingEnterprise) {
            cityOptions = await fetchCitiesAsOptions()
            enterprise = jobOfferTemplate.generate().enterprise
        }
        isFetchingOptions = false
    })
</script>

<div>
    <h1>
        Création d'une nouvelle <span class="hightlight">Entreprise</span>
    </h1>
    <div class="form-group-vertical">
        <label for="title">Nom de l'entreprise*</label>
        <br />
        <input
            type="text"
            bind:value={enterprise.name}
            name="enterprise.name"
            class="form-control"
            id="title"
        />
    </div>
    <p class="errors-input">
        {#if errors["enterprise.name"]}{errors["enterprise.name"]}{/if}
    </p>

    <div class="form-group-vertical">
        <label for="address">Adresse de l'entreprise*</label>
        <br />
        <input
            type="text"
            name="enterprise.address"
            bind:value={enterprise.address}
            class="form-control"
            id="address"
        />
    </div>
    <p class="errors-input">
        {#if errors["enterprise.address"]}{errors["enterprise.address"]}{/if}
    </p>

    <div class="form-group-vertical">
        <label for="email">Courriel de l'entreprise*</label>
        <br />
        <input
            type="text"
            name="enterprise.email"
            bind:value={enterprise.email}
            class="form-control"
            id="email"
        />
    </div>
    <p class="errors-input">
        {#if errors["enterprise.email"]}{errors["enterprise.email"]}{/if}
    </p>

    <div class="form-group-vertical">
        <label for="phone">Téléphone de l'entreprise*</label>
        <br />
        <input
            type="text"
            name="enterprise.phone"
            bind:value={enterprise.phone}
            class="form-control"
            id="phone"
        />
    </div>
    <p class="errors-input">
        {#if errors["enterprise.phone"]}{errors["enterprise.phone"]}{/if}
    </p>

    <div class="form-group-vertical">
        <label for="city">Ville de l'entreprise*</label>
        <br />
        {#if cityOptions.length === 0}
            <p>Chargement des villes...</p>
        {:else}
            <MultiSelect
                id="city"
                options={cityOptions as any[]}
                maxSelect={1}
                closeDropdownOnSelect={true}
                placeholder="Choisir ville..."
                bind:selected={selectedCities as any[]}
            />
        {/if}
    </div>
    <p class="errors-input">
        {#if errors["enterprise.cityId"]}{errors["enterprise.cityId"]}{/if}
    </p>
</div>

<style scoped>
    .form-group-vertical {
        display: flex;
        flex-direction: column;
        width: 100%;
        margin: auto;
    }
</style>
