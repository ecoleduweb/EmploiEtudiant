<script lang="ts">
    import { MultiSelect } from "svelte-multiselect"

    interface Props {
        enterprise: any
        errorsEnterprise: any
        cityOptions: any
        cityFromEnterprise: any
    }

    let {
        enterprise = $bindable(),
        errorsEnterprise,
        cityOptions,
        cityFromEnterprise = $bindable(),
    }: Props = $props()
</script>

<div class="form-group-vertical">
    <label for="title">Nom de l'entreprise*</label>
    <br />
    <input
        type="text"
        bind:value={enterprise.name}
        class="form-control"
        id="title"
    />
</div>
<p class="errors-input">
    {#if errorsEnterprise.name}{errorsEnterprise.name}{/if}
</p>

<div class="form-group-vertical">
    <label for="address">Adresse de l'entreprise*</label>
    <br />
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
    <label for="email">Courriel de l'entreprise*</label>
    <br />
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
    <label for="phone">Téléphone de l'entreprise*</label>
    <br />
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
    <label for="city">Ville de l'entreprise*</label>
    <br />
    {#if cityOptions.length === 0}
        <p>Chargement des villes...</p>
    {:else}
        <MultiSelect
            id="city"
            options={cityOptions}
            maxSelect={1}
            closeDropdownOnSelect={true}
            placeholder="Choisir ville..."
            bind:selected={cityFromEnterprise}
        />
    {/if}
</div>
<p class="errors-input">
    {#if errorsEnterprise.cityId}{errorsEnterprise.cityId}{/if}
</p>
