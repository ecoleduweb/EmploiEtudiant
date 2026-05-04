<script lang="ts">
    import "../../styles/global.css"
    import { onMount } from "svelte"
    import { GET, PATCH, POST, PUT } from "../../ts/server"
    import type { Enterprise } from "../../Models/Enterprise"
    import EnterpriseRow from "../../Components/Enterprise/EnterpriseRow.svelte"
    import CreateAndEditEnterprise from "../../Components/Enterprise/CreateAndEditEnterprise.svelte"
    import Button from "../../Components/Inputs/Button.svelte"
    import { enterprises } from "$lib"
    import Modal from "../../Components/Common/Modal.svelte"
    import fetchCity from "../../Service/CityService"
    import { getCityName } from "../../Service/CityService"
    import { updateEnterprise,  createEnterprise as addEnterpriseToAPI } from "../../Service/EnterpriseService"

    let createEnterprise = false
    let modalOpened = $state(false)
    let selectedEnterprise: Enterprise | undefined = $state(undefined)
    let searchTerm = $state("")

    const openModal = () => {
        modalOpened = true
    }

    const closeModal = () => {
        modalOpened = false
    }
    const handleEnterpriseClick = (enterprise: Enterprise) => {
        selectedEnterprise = enterprise
        openModal()
    }
    const openCreateEnterprise = () => {
        selectedEnterprise = undefined
        modalOpened = true
    }
    const normalize = (str: string) => {
        return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    }
    const addEnterprise = async (newEnterprise: Enterprise) => {
        try {
           const createdEnterprise: any = await addEnterpriseToAPI(newEnterprise)

            enterprises.update((list) => [...list, createdEnterprise])
        } catch (error) {
            console.error("Error creating enterprise:", error)
        }
    }
    const editEnterprise = async (enterprise: Enterprise) => {
        try {
            await updateEnterprise(enterprise, enterprise.id!)

            enterprises.update((list) =>
                list.map((ent) =>
                    ent.id === enterprise.id ? enterprise : ent,
                ),
            )
        } catch (error) {
            console.error("Error editing enterprise:", error)
        }
    }

    const upsertEnterprise = async (enterprise: Enterprise | void) => {
        if (enterprise !== undefined) {
            if (enterprise.id !== undefined && enterprise.id >= 0) {
                await editEnterprise(enterprise)
                closeModal()
            }
            else {
                await addEnterprise(enterprise)
                closeModal()
            }
        } else {
            closeModal()
        }
    }

    const getEnterprises = async () => {
        try {
            const response = await GET<any>("/enterprise/all")
            enterprises.set(response)
        } catch (error) {
            console.error("Error fetching job offers:", error)
        }
    }

    onMount(async () => {
        await fetchCity()
        await getEnterprises()
    })

    type EnterpriseWithCity = Enterprise & { cityName: string }
    let filteredEnterprises: EnterpriseWithCity[] = $state([])

    $effect(() => {
        if ($enterprises) {
            ;(async () => {
                const search = searchTerm.toLowerCase()

                const enterprisesWithCity: EnterpriseWithCity[] =
                    await Promise.all(
                        $enterprises.map(async (enterprise) => {
                            const cityName = await getCityName(
                                enterprise.cityId,
                            )
                            return { ...enterprise, cityName }
                        }),
                    )

                filteredEnterprises = enterprisesWithCity.filter(
                    (enterprise) =>
                        normalize(enterprise.name)
                            .toLowerCase()
                            .includes(search) ||
                        normalize(enterprise.email)
                            .toLowerCase()
                            .includes(search) ||
                        normalize(enterprise.address)
                            .toLowerCase()
                            .includes(search) ||
                        normalize(enterprise.phone)
                            .toLowerCase()
                            .includes(search) ||
                        normalize(enterprise.cityName)
                            .toLowerCase()
                            .includes(search)||
                        (enterprise.users?.some((user) =>
                        normalize(
                            `${user.email ?? ""}`
                        )
                            .toLowerCase()
                            .includes(search)
                        ) ?? false)
                )
            })()
        }
    })
</script>

<main>
    <section class="top">
        <div class="top-left">
            <div class="flex-container">
                <Button
                    onClick={openCreateEnterprise}
                    text="Créer une nouvelle entreprise"
                />
            </div>
        </div>
    </section>
    <section class="top">
        <div class="top-left">
            <h1 class="title">
                <span class="text">MES </span>
                <span class="text"> ENTREPRISES</span>
            </h1>
        </div>
        <div class="top-right">
            <div class="search-container">
                <svg
                    class="search-icon"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                >
                    <circle cx="11" cy="11" r="8"></circle>
                    <path d="m21 21-4.35-4.35"></path>
                </svg>
                <input
                    type="text"
                    bind:value={searchTerm}
                    placeholder="Rechercher une entreprise..."
                    class="search-input"
                />
            </div>
        </div>
    </section>

    <section class="enterprises">
        {#each filteredEnterprises as enterprise}
            <EnterpriseRow
                {enterprise}
                cityName={enterprise.cityName}
                handleModalClick={() => handleEnterpriseClick(enterprise)}
            />
        {/each}
    </section>
    {#if modalOpened}
        <Modal handleCloseClick={closeModal}>
            <CreateAndEditEnterprise
                enterprise={selectedEnterprise}
                handleApproveClick={(enterprise) => upsertEnterprise(enterprise)}
            />
        </Modal>
    {/if}
</main>

<style>
    .title {
        left: 7.2%;
        margin: 0;
        margin-top: 30px;
    }

    .title span:first-child {
        color: white;
        margin: 0;
    }

    .title span:last-child {
        color: #00ad9a;
        margin: 0;
    }

    .text {
        font-size: 2.5vw;
        margin: 0;
    }

    main {
        display: flex;
        flex-direction: column;
        width: 100%;
        height: 100%;
    }

    .top {
        display: flex;
        width: 100%;
        margin-bottom: 30px;
    }
    .top-left {
        display: flex;
        flex-direction: column;
        width: 50%;
        margin-left: 5.2%;
    }

    .top-right {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        width: 40%;
    }
    .flex-container {
        display: flex;
        margin-top: 20px;
    }

    .search-container {
        display: flex;
        align-items: center;
        background-color: rgba(0, 173, 154, 0.1);
        border: 2px solid #00ad9a;
        border-radius: 8px;
        padding: 0.5vw 1vw;
        width: 300px;
        transition: all 0.3s ease;
    }

    .search-container:hover {
        background-color: rgba(0, 173, 154, 0.15);
        box-shadow: 0 4px 12px rgba(0, 173, 154, 0.2);
    }

    .search-container:focus-within {
        background-color: rgba(0, 173, 154, 0.2);
        box-shadow: 0 4px 16px rgba(0, 173, 154, 0.3);
        border-color: #00ad9a;
    }

    .search-icon {
        width: 20px;
        height: 20px;
        color: #00ad9a;
        margin-right: 0.8vw;
        flex-shrink: 0;
    }

    .search-input {
        flex: 1;
        border: none;
        background-color: transparent;
        color: white;
        font-size: 1rem;
        outline: none;
        padding: 0;
    }

    .search-input::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }

    @media (max-width: 768px) {
        .text {
            font-size: 6vw;
            margin-right: 2vw !important;
        }
        .title {
            display: flex;
            justify-content: left;
            flex-direction: row;
        }
        .top-left {
            width: 100%;
            margin-left: 1vw;
        }
        .top {
            margin-left: 4vw;
            flex-direction: column;
        }
        .top-right {
            width: 100%;
            margin-top: 1.5rem;
        }
        .search-container {
            width: 100%;
        }
    }
</style>
