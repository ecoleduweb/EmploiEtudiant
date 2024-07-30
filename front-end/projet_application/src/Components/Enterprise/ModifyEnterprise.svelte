<script lang="ts">
    import Modal from "../Common/Modal.svelte"
    import { MultiSelect } from "svelte-multiselect";
    import CreateEditEnterprise from "../JobOffer/CreateEditEnterprise.svelte"

    //À faire:
     //Trouver l'entreprise de l'utilisateur actuelle
     //Avoir les villes et les montrées
     //Vérifier les entrées et montrer une erreur s'il y à une entrée incorrecte
     //Envoyer une requête au serveur
     //Faire le code au serveur (S'il n'existe pas déjà, je ne sais pas s'il y existe déjà quelque chose au serveur pour modifier les entreprises)

    let enterprise: any
    let errorsEnterprise: any
    let cityOptions: any
    let selectedCity: any
    let cityFromEnterprise: any
    export let handleCloseClick: () => void

</script>

<Modal {handleCloseClick}>
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
</Modal>