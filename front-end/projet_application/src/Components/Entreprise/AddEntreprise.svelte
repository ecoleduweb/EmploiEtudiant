<script lang="ts">
    import "../../styles/global.css";
    import Button from "../../Components/Inputs/Button.svelte";
    import MultiSelect from 'svelte-multiselect';
    import { writable, type Writable } from 'svelte/store';
    import { POST } from "../../ts/server";
    import * as yup from "yup";
    import { extractErrors } from "../../ts/utils";
    import type { Entreprise } from "../../Models/Entreprise";
    import { goto } from '$app/navigation';
    import Modal from "../Common/Modal.svelte";
    export let handleEntrepriseClick: () => void;

    const schema = yup.object().shape({
    name: yup.string().required("Le nome de l'entreprise est requis."),
    address: yup.string().required("L'adresse du lieu de travail est requise."),
    email : yup.string().matches(/\.[a-z]+$/, "Le courriel doit être de format valide : courriel@domaine.ca").email("Le courriel n'est pas valide").required("Le courriel est requis"),
    phone: yup.string().matches(/^[0-9]{10}$/, "Le numéro de téléphone doit être de 10 chiffres").required("Le numéro de téléphone est requis"),
    cityId: yup.number().required("La ville est requise"),
    });

   let enterprise: Entreprise = {
        id: 0,
        name: "",
        email: "",
        phone: "",
        address: "",
        cityId: 0,
        isTemporary: true,
    };

    let villeSelected: { label: string; value: number }[] = [];
    let villeFromSelectedEntreprise: [] = [];
    let villeOption = [
        { label: "Trois-Pistoles", value: 1 },
        { label: "Rivière-du-Loup", value: 2 },
        { label: "Squatec", value: 3 },
        { label: "Chibougamau", value: 4 },
        { label: "Amqui", value: 5 },
        { label: "Trois-Rivière", value: 6 },
        { label: "Lévis", value: 7 },
    ];

    let errors : Entreprise = {
        id : 0,
        name: "",
        email: "",
        phone: "",
        address: "",
        cityId: 0,
        isTemporary: true,
    };

    const handleSubmit = async () => {
        try {
            await schema.validate(enterprise, { abortEarly: false });
            errors = {
                id : 0,
                name: "",
                email: "",
                phone: "",
                address: "",
                cityId: 0,
                isTemporary: true,
            };
            const requestData = {
                enterprise: enterprise,
            };
            const response = await POST<any, any>("/enterprise/createEnterprise", requestData);
            handleEntrepriseClick();
        } catch (err) {
            console.log(err);
            if (err instanceof yup.ValidationError) {
                errors = extractErrors(err);
                console.log(errors);
            }
        }
    }
</script>

<Modal handleModalClick={handleEntrepriseClick}>
    <form on:submit|preventDefault={handleSubmit} class="form-offre">
        <h1 class="title">Créer une nouvelle entreprise</h1>
        <div class="form-group-vertical">
            <label for="title">Nom*</label>
            <input type="text" bind:value={enterprise.name} class="form-control" id="name" />
            <p class="errors-input">
                {#if errors.name}{errors.name}{/if}
            </p>
        </div>
        <div class="form-group-vertical">
            <label for="title">Email*</label>
            <input type="text" bind:value={enterprise.email} class="form-control" id="email" />
            <p class="errors-input">
                {#if errors.email}{errors.email}{/if}
            </p>
        </div>
        <div class="form-group-vertical">
            <label for="title">Téléphone*</label>
            <input type="text" bind:value={enterprise.phone} class="form-control" id="phone" />
            <p class="errors-input">
                {#if errors.phone}{errors.phone}{/if}
            </p>
        </div>
        <div class="form-group-vertical">
            <label for="title">Adresse*</label>
            <input type="text" bind:value={enterprise.address} class="form-control" id="address" />
            <p class="errors-input">
                {#if errors.address}{errors.address}{/if}
            </p>
        </div>
        <div class="form-group-vertical">
            <label for="title">Ville*</label>
            <MultiSelect
                id="ville"
                options={villeOption}
                placeholder="Choisir ville(s)..."
                bind:value={villeSelected}
                bind:selected={villeFromSelectedEntreprise}
                closeDropdownOnSelect={true}
            ></MultiSelect>
            <p class="errors-input">
                {#if errors.cityId}{errors.cityId}{/if}
            </p>
        </div>
        <Button submit={true} text="Créer" on:click={() => handleSubmit()} />
    </form>
</Modal>
<style>
    label {
      display: block;
      margin-bottom: 0.26vw;
    }

    .form-offre {
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 100%;
      
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
    }

    .title{
        font-size: 2vw;
        margin-top: 10px;
    }
    
  </style>
