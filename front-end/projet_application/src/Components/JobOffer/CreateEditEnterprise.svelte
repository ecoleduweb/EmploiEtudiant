<script lang="ts">
    import { MultiSelect } from "svelte-multiselect";
    import type { Writable } from "svelte/store"

    export let enterprise: any
    export let errorsEnterprise: any
    export let cityOptions: any
    export let selectedCity: Writable<any>
    export let cityFromEnterprise: any

    let selectCity: any
    $: selectedCity.set(selectCity)
</script>

<div class="form-group-vertical">
    <label for="title">Nom de l'entreprise*</label>
    <br>
    <input
        type="text"
        bind:value={enterprise.name}
        class="form-control"
        id="titre"
    />
</div>
<p class="errors-input">
    {#if errorsEnterprise.name}{errorsEnterprise.name}{/if}
</p>
<div class="form-group-vertical">
    <label for="schedule">Adresse de l'entreprise*</label>
    <br>
    <input
        type="text"
        bind:value={enterprise.address}
        class="form-control"
        id="address"
    />
</div>
<p class="errors-input">
    {#if errorsEnterprise.address}{errorsEnterprise.address}{/if}
</p>
<div class="form-group-vertical">
    <label for="lieu">Courriel de l'entreprise*</label>
    <br>
    <input
        type="text"
        bind:value={enterprise.email}
        class="form-control"
        id="email"
    />
</div>
<p class="errors-input">
    {#if errorsEnterprise.email}{errorsEnterprise.email}{/if}
</p>
<div class="form-group-vertical">
    <label for="lieu">Téléphone de l'entreprise*</label>
    <br>
    <input
        type="text"
        bind:value={enterprise.phone}
        class="form-control"
        id="phone"
    />
</div>
<p class="errors-input">
    {#if errorsEnterprise.phone}{errorsEnterprise.phone}{/if}
</p>
<div class="form-group-vertical">
    <label for="lieu">Ville de l'entreprise*</label>
    <br>
    {#if cityOptions.length === 0}
        <p>Chargement des villes...</p>
    {:else}
        <MultiSelect
            id="ville"
            options={cityOptions}
            closeDropdownOnSelect={true}
            placeholder="Choisir ville..."
            bind:value={selectCity}
            bind:selected={cityFromEnterprise}
        />
    {/if}
</div>
<p class="errors-input">
    {#if errorsEnterprise.cityId}{errorsEnterprise.cityId}{/if}
</p>


