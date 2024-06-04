<script lang="ts">
    import "../../styles/global.css"
    import Button from "../../Components/Inputs/Button.svelte"
    import MultiSelect from "svelte-multiselect"
    import { writable, type Writable } from "svelte/store"
    import { GET, POST } from "../../ts/server"
    import * as yup from "yup"
    import { extractErrors } from "../../ts/utils"
    import type { Entreprise } from "../../Models/Entreprise"
    import { goto } from "$app/navigation"
    import Modal from "../Common/Modal.svelte"
    import { onMount } from "svelte"
    export let handleEntrepriseClick: () => void

    const schema = yup.object().shape({
        name: yup.string().required("Le nome de l'entreprise est requis."),
        address: yup
            .string()
            .required("L'adresse du lieu de travail est requise."),
        email: yup
            .string()
            .matches(
                /\.[a-z]+$/,
                "Le courriel doit être de format valide : courriel@domaine.ca",
            )
            .email("Le courriel n'est pas valide")
            .required("Le courriel est requis"),
        phone: yup
            .string()
            .matches(
                /^[0-9]{10}$/,
                "Le numéro de téléphone doit être de 10 chiffres",
            )
            .required("Le numéro de téléphone est requis"),
        cityId: yup.number().required("La ville est requise"),
    })

    let enterprise: Entreprise = {
        id: 0,
        name: "",
        email: "",
        phone: "",
        address: "",
        cityId: 0,
        isTemporary: true,
    }

    let villeSelected: { label: string; value: number } = {
        label: "",
        value: 0,
    }
    let villeFromSelectedEntreprise: [] = []
    let villeOption: { label: string; value: number }[] = []

    const getAllCities = async () => {
        try {
            const response = await GET<any>("/city/allCities")
            villeOption = response.map((city: any) => {
                return { label: city.city, value: city.id }
            })
        } catch (error) {
            console.error("Error fetching cities:", error)
        }
    }
    onMount(getAllCities)

    let errors: Entreprise = {
        id: 0,
        name: "",
        email: "",
        phone: "",
        address: "",
        cityId: 0,
        isTemporary: true,
    }

    const updateCityId = () => {
        enterprise.cityId = villeSelected.value
    }

    const handleSubmit = async () => {
        try {
            await schema.validate(enterprise, { abortEarly: false })
            errors = {
                id: 0,
                name: "",
                email: "",
                phone: "",
                address: "",
                cityId: 0,
                isTemporary: true,
            }
            updateCityId()
            const response = await POST<any, any>(
                "/enterprise/createEnterprise",
                enterprise,
            )
            handleEntrepriseClick()
        } catch (err) {
            console.log(err)
            if (err instanceof yup.ValidationError) {
                errors = extractErrors(err)
                console.log(errors)
            }
        }
    }
</script>

<Modal handleModalClick={handleEntrepriseClick}>
    <form on:submit|preventDefault={handleSubmit} class="form-offre">
        <h1 class="title">Créer une nouvelle entreprise</h1>
        <div class="form-group-vertical">
            <label for="title">Nom*</label>
            <input
                type="text"
                bind:value={enterprise.name}
                class="form-control"
                id="name"
            />
            <p class="errors-input">
                {#if errors.name}{errors.name}{/if}
            </p>
        </div>
        <div class="form-group-vertical">
            <label for="title">Email*</label>
            <input
                type="text"
                bind:value={enterprise.email}
                class="form-control"
                id="email"
            />
            <p class="errors-input">
                {#if errors.email}{errors.email}{/if}
            </p>
        </div>
        <div class="form-group-vertical">
            <label for="title">Téléphone*</label>
            <input
                type="text"
                bind:value={enterprise.phone}
                class="form-control"
                id="phone"
            />
            <p class="errors-input">
                {#if errors.phone}{errors.phone}{/if}
            </p>
        </div>
        <div class="form-group-vertical">
            <label for="title">Adresse*</label>
            <input
                type="text"
                bind:value={enterprise.address}
                class="form-control"
                id="address"
            />
            <p class="errors-input">
                {#if errors.address}{errors.address}{/if}
            </p>
        </div>
        <div class="form-group-vertical">
            <label for="title">Ville*</label>
            <MultiSelect
                id="ville"
                options={villeOption}
                placeholder="Choisir une ville..."
                bind:value={villeSelected}
                bind:selected={villeFromSelectedEntreprise}
                closeDropdownOnSelect={true}
                maxSelect={1}
            ></MultiSelect>
            <p class="errors-input">
                {#if errors.cityId}{errors.cityId}{/if}
            </p>
        </div>
        <!-- <div class="form-group-vertical">
            <label for="title">Ville*</label>
            <select id="ville" bind:value={villeSelected} class="form-control">
                {#each villeOption as { label, value }}
                    <option value={value}>{label}</option>
                {/each}
            </select>
            <p class="errors-input">
                {#if errors.cityId}{errors.cityId}{/if}
            </p>
        </div> -->

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

    .title {
        font-size: 2vw;
        margin-top: 10px;
    }
</style>
