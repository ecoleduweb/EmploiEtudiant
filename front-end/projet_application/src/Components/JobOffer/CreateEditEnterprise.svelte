<script lang="ts">
    import { MultiSelect } from "svelte-multiselect";

    export let enterprise: any
    export let errorsEnterprise: any
    export let cityOptions: any
    export let selectedCity: any
    export let cityFromEnterprise: any
</script>

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
    {#if cityOptions.length === 0}
        <p>Chargement des villes...</p>
    {:else}
        <MultiSelect
            id="ville"
            options={cityOptions}
            closeDropdownOnSelect={true}
            placeholder="Choisir ville..."
            bind:value={selectedCity}
            bind:selected={cityFromEnterprise}
        />
    {/if}
</div>