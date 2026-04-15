<script lang="ts">
    import Button from "../Inputs/Button.svelte"
    import type { Enterprise } from "../../Models/Enterprise"
    import type { User } from "../../Models/User"
    import MultiSelect from "svelte-multiselect"
    import { onMount } from "svelte"
    import fetchCity from "../../Service/CityService"
    import { entrepriseSchema } from "../../FormValidations/JobOffer"
    import { ValidationError } from "yup"
    import { extractErrors } from "../../ts/utils"
    import { GET } from "../../ts/server"

    type Props = {
        enterprise?: Enterprise
        handleApproveClick: (enterprise: Enterprise | void) => void
    }

    let {
        enterprise: enterpriseProp = {
            name: "",
            id: -1,
            email: "",
            phone: "",
            address: "",
            cityId: 0,
            isTemporary: false,
            users: [] 
        },
        handleApproveClick,
    }: Props = $props()

    let enterprise = $state({ ...enterpriseProp })
    let errorsEnterprise: any = $state([])
    let savedName = $state(enterpriseProp.name)
    let isNewEnterprise = $derived((enterprise.id ?? -1) <= 0)

    let villeSelected: { label: string; value: number } | null = $state(null)
    let cityFromSelectedEnterprise: { label: string; value: number }[] = $state([])
    let cityOptions: { label: string; value: number }[] = $state([])

    let userOptions: { label: string; value: number; originalUser: any }[] = $state([])
    let selectedUserObjects: any[] = $state([])
    let Users: any[] = $state([])
    const getAllUsers = async () => {
        try {
            const data = await GET<any>("/user/all")
            if (data && data.users) {
                userOptions = data.users.map((u: any) => {
                    const fullName = `${u.firstName} ${u.lastName}`.trim()
                    return { 
                        label: fullName.length > 0 ? fullName : u.email, 
                        value: u.id,
                        originalUser: u
                    }
                })
                if (enterprise.users && enterprise.users.length > 0) {
                    selectedUserObjects = userOptions.filter(opt => 
                        enterprise.users?.some(u => u.id === opt.value)
                    )
                }
            }
        } catch (err) {
            console.error(err)
        }
    }

    const getAllCities = async () => {
        try {
            cityOptions = await fetchCity()
            if (enterprise.cityId) {
                const found = cityOptions.find(c => c.value === enterprise.cityId)
                if (found) {
                    villeSelected = found
                    cityFromSelectedEnterprise = [found]
                }
            }
        } catch (error) {
            console.error(error)
        }
    }

    $effect(() => {
        if (villeSelected) {
            enterprise.cityId = villeSelected.value
        }
    })

const prepareAndVerifyIfValid = async () => {
        if (enterprise !== null) {
            try {
                enterprise.cityId = villeSelected?.value ?? -1;

                enterprise.users = selectedUserObjects.map(opt => opt.originalUser);

                console.log("Enterprise data before validation:", enterprise);
                
                await entrepriseSchema.validate(enterprise, { abortEarly: false });
                
                console.log("Enterprise data after validation:", enterprise);
                return enterprise; 
            } catch (err) {
                if (err instanceof ValidationError) {
                    errorsEnterprise = extractErrors(err);
                }
                return null;
            }
        }
    };

    const handleSubmit = async () => {
        console.log("on commence validation ", enterprise);
        const validatedData = await prepareAndVerifyIfValid();
        console.log("Validated Enterprise Data:", validatedData);
        if (validatedData) {
            handleApproveClick(validatedData);
        }
    };

    onMount(() => {
        getAllCities()
        getAllUsers()
    })
</script>

<div class="main-div">
    <div class="container">
        <h5 class="infoTitle">
            {isNewEnterprise
                ? "Veuillez remplir les informations pour la nouvelle entreprise"
                : "Modification de l'entreprise : " + savedName}
        </h5>

        {#if enterprise && cityOptions}
            <div class="modalContent">
                <div class="form-group-vertical">
                    <label for="enterprise-name"> Nom* </label>
                    <input id="enterprise-name" type="text" bind:value={enterprise.name} class="form-control" />
                    <p class="errors-input">{errorsEnterprise.name || ""}</p>
                </div>

                <div class="form-group-vertical">
                    <label for="enterprise-address"> Adresse* </label>
                    <input id="enterprise-address" type="text" bind:value={enterprise.address} class="form-control" />
                    <p class="errors-input">{errorsEnterprise.address || ""}</p>
                </div>

                <div class="form-group-vertical">
                    <label for="enterprise-email"> Courriel* </label>
                    <input id="enterprise-email" type="text" bind:value={enterprise.email} class="form-control" />
                    <p class="errors-input">{errorsEnterprise.email || ""}</p>
                </div>

                <div class="form-group-vertical">
                    <label for="enterprise-phone"> Téléphone* </label>
                    <input id="enterprise-phone" type="text" bind:value={enterprise.phone} class="form-control" />
                    <p class="errors-input">{errorsEnterprise.phone || ""}</p>
                </div>

                <div class="form-group-vertical">
                    <label for="ville">Ville*</label>
                    <MultiSelect
                        id="enterprise-city"
                        options={cityOptions}
                        bind:value={villeSelected}
                        placeholder="Choisir une ville..."
                        bind:selected={cityFromSelectedEnterprise}
                        closeDropdownOnSelect={true}
                        maxSelect={1}
                    />
                    <p class="errors-input">{errorsEnterprise.cityId || ""}</p>
                </div>
            </div>
        {/if}

        <h5 class="infoTitle" style="margin-top: 10px;">Assigner des employés</h5>
        <div class="form-group-vertical" style="margin-left: auto; margin-right: auto;">
            <MultiSelect
                id="enterprise-admin"
                options={userOptions}
                bind:selected={selectedUserObjects}
                closeDropdownOnSelect={false}
                placeholder="Choisir les utilisateurs..."
            />
        </div>

        <div class="button">
            <Button text={isNewEnterprise ? "Créer" : "Modifier"} onClick={handleSubmit} />
            <Button text="Annuler" onClick={() => handleApproveClick(undefined)} />
        </div>
    </div>
</div>

<style scoped>
    .container {
        width: 100%;
        display: flex;
        flex-direction: column;
        text-align: center;
        justify-content: flex-start; 
        color: black;
        border-radius: 4px;
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
        margin-top: 20px;
    }
    .main-div {
        display: flex;
        flex-direction: column;
        margin: auto;
        background-color: white;
        padding: 15px;
        border-radius: 8px;
    }
    .infoTitle {
        color: black;
        margin: 10px 0;
        font-weight: bold;
    }
    .form-group-vertical {
        display: flex;
        flex-direction: column;
        width: 75%;
        margin: 0.5vw auto;
        text-align: left;
    }
    .form-control {
        width: 100%;
        padding: 5px;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    .errors-input {
        color: red;
        font-size: 0.8em;
        margin-top: 0.2vw;
        min-height: 1em;
    }
</style>