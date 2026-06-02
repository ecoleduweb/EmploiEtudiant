<script lang="ts">
    import MultiSelect from "svelte-multiselect"
    import { onMount } from "svelte"
    import type { Option } from "../../Models/Option"
    import type { Enterprise } from "../../Models/Enterprise"
    import {
        fetchEnterprises,
        fetchCurrentUserEnterprise,
    } from "../../Service/EnterpriseService"
    import { currentUser } from "$lib"
    import EntrepriseDetails from "./EntrepriseDetails.svelte"
    import CreateEditEnterprisePartialForm from "./CreateEditEnterprisePartialForm.svelte"
    interface Props {
        enterprise: Enterprise | undefined
        errors: any
    }
    let { enterprise = $bindable(), errors }: Props = $props()

    const isCreatingEnterprise = $derived(enterprise?.id === 0) // si le id est 0, on crée l'entreprise, sinon on affiche les détails de l'entreprise existante
    const isModerator = !!$currentUser?.isModerator

    let enterpriseOptions: Option[] = $state([])
    let enterprises: Enterprise[] = $state([])
    let selectedEnterprises: Option[] = $state([])

    // Met à jour le modèle quand une des valeur dans le $effect change. Ici ce sont les selected
    let isFetchingOptions = $state(true)

    // Utilisé pour mettre l'entreprise à jour à partir du id sélectionnée par l'admin
    $effect(() => {
        if (enterprises.length > 0) {
            const selectedEnterprise = enterprises.find(
                (x) => x.id === selectedEnterprises.at(0)?.value,
            )
            enterprise = selectedEnterprise
        }
    })

    onMount(async () => {
        isFetchingOptions = true
        if (isModerator) {
            enterprises = await fetchEnterprises()
            enterpriseOptions = enterprises.map((e) => ({
                value: e.id,
                label: e.name,
            }))
            selectedEnterprises = enterpriseOptions.filter(
                (opt) => opt.value === enterprise?.id,
            )
        } else {
            const usersEnterprise = await fetchCurrentUserEnterprise()
            if (usersEnterprise && enterprise) {
                Object.assign(enterprise, usersEnterprise)
            }
        }
        isFetchingOptions = false
    })
</script>

<div class="enterprise-section">
    {#if isModerator}
        <h1>Sélectionner une entreprise existante</h1>
        <div class="form-group-horizontal">
            <MultiSelect
                loading={isFetchingOptions}
                id="enterprise"
                options={enterpriseOptions as any}
                closeDropdownOnSelect={true}
                maxSelect={1}
                placeholder="Choisir une entreprise..."
                bind:selected={selectedEnterprises as any[]}
            />
        </div>
        <p class="errors-input">
            {#if errors.enterpriseId}{errors.enterpriseId}{/if}
        </p>
    {:else if isCreatingEnterprise && enterprise}
        <CreateEditEnterprisePartialForm bind:enterprise {errors} />
    {:else if enterprise}
        <h1>Mon <span class="hightlight">Entreprise</span></h1>
        <EntrepriseDetails {enterprise} />
        <hr />
    {/if}
</div>

<style scoped>
    .enterprise-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 2vh;
        margin: auto;
        width: 80%;
    }
    h1 {
        margin: auto;
    }
    .form-group-horizontal {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        width: 80%;
        margin: 1vh 0;
        margin-left: auto;
        margin-right: auto;
    }
    .errors-input {
        color: red;
        font-size: 0.8em;
    }
    @media (max-width: 768px) {
        .form-group-horizontal {
            flex-direction: column;
            align-items: center;
            width: 100%;
        }
    }
</style>
