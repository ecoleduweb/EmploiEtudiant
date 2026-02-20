<script lang="ts">
    import "../../styles/global.css"
    import { onMount } from "svelte"
    import { writable } from "svelte/store"
    import { GET, PATCH, POST, PUT } from "../../ts/server"
    import type { Enterprise } from "../../Models/Enterprise"
    import EnterpriseRow from "../../Components/Enterprise/EnterpriseRow.svelte"
    import CreateAndEditEnterprise from "../../Components/Enterprise/CreateAndEditEnterprise.svelte"
    import Button from "../../Components/Inputs/Button.svelte"
    import LoadingSpinner from "../../Components/Common/LoadingSpinner.svelte"
    import { enterprises } from "$lib"
    import Modal from "../../Components/Common/Modal.svelte"
    import fetchCity from "../../Service/CityService"
    import { getCityName } from "../../Service/CityService"

    // const modal = writable(false)
    // const modalAdd = writable(false)
    // const selectedEnterpriseId = writable(0)
    let createEnterprise = false
    let modalOpened = false
    let selectedEnterprise: Enterprise | undefined = undefined
    let searchTerm = ""

    const openModal = () => {
        modalOpened = true
    }
    const closeModal = () => {
        modalOpened = false
        refresh()
    }
    const handleEnterpriseClick = (enterprise: Enterprise) => {
        selectedEnterprise = enterprise
        openModal()
        refresh()
    }
    const openCreateEnterprise = () => {
        selectedEnterprise = undefined
        modalOpened = true
    }

    const addEnterprise = async (newEnterprise: Enterprise) => {
        try {
            const reponse = await POST<any, any>(`/enterprise/new`, {
                name: newEnterprise.name,
                address: newEnterprise.address,
                phone: newEnterprise.phone,
                email: newEnterprise.email,
                cityId: newEnterprise.cityId,
            })
        } catch (error) {
            console.error("Error creating enterprise:", error)
        }
    }
    const editEnterprise = async (enterprise: Enterprise) => {
        try {
            const response = await PUT<any, any>(
                `/enterprise/${enterprise.id}`,
                {
                    id: enterprise.id,
                    name: enterprise.name,
                    email: enterprise.email,
                    phone: enterprise.phone,
                    address: enterprise.address,
                    cityId: enterprise.cityId,
                },
            )
        } catch (error) {
            console.error("Error editing enterprise:", error)
        }
    }
    const upsertEnterprise = async (enterprise: Enterprise | void) => {
        if (enterprise !== undefined) {
            if (enterprise.id >= 0) {
                //Existant
                await editEnterprise(enterprise)
                closeModal()
            } //Nouveau
            else {
                await addEnterprise(enterprise)
                closeModal()
            }
        } else {
            closeModal()
        }
        //Si offer.id >= 0, veut dire existant
        //Si offer.id = -1, veut dire nouveau
        //Si offer = undefined, veut dire annuler
    }

    const getEnterprises = async () => {
        try {
            const response = await GET<any>("/enterprise/all")
            enterprises.set(response)
        } catch (error) {
            console.error("Error fetching job offers:", error)
        }
    }
    async function refresh() {
        await getEnterprises()
    }
    onMount(async () => {
        await fetchCity()
        await refresh()
    })
    $: filteredEnterprises = $enterprises.filter(
        (enterprise) =>
            enterprise.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            enterprise.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
            enterprise.address
                .toLowerCase()
                .includes(searchTerm.toLowerCase()) ||
            enterprise.phone.toLowerCase().includes(searchTerm.toLowerCase()) ||
            getCityName(enterprise.cityId)
                .toLowerCase()
                .includes(searchTerm.toLowerCase()),
    )
</script>

<main>
    <section class="haut">
        <div class="haut-gauche">
            <div class="divFlex">
                <Button
                    onClick={openCreateEnterprise}
                    text="Créer une nouvelle entreprise"
                />
            </div>
        </div>
    </section>
    <section class="haut">
        <div class="haut-gauche">
            <h1 class="title">
                <span class="text">MES </span>
                <span class="text"> ENTREPRISES</span>
            </h1>
        </div>
        <div class="haut-droite">
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

    <section class="Enterprises">
        {#each filteredEnterprises as enterprise}
            <EnterpriseRow
                {enterprise}
                handleModalClick={() => handleEnterpriseClick(enterprise)}
            />
        {/each}
    </section>
    {#if modalOpened}
        <Modal handleCloseClick={closeModal}>
            <CreateAndEditEnterprise
                enterprise={selectedEnterprise}
                handleApproveClick={(offer) => upsertEnterprise(offer)}
            />
        </Modal>
    {/if}
</main>

<style scoped>
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
    .haut {
        display: flex;
        width: 100%;
        margin-bottom: 30px;
    }
    .haut-gauche {
        display: flex;
        flex-direction: column;
        width: 50%;
        margin-left: 5.2%;
    }
    .haut-droite {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        width: 40%;
    }
    .divFlex {
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
        .haut-gauche {
            width: 100%;
            margin-left: 1vw;
        }
        .haut {
            margin-left: 4vw;
            flex-direction: column;
        }
        .haut-droite {
            width: 100%;
            margin-top: 1.5rem;
        }
        .search-container {
            width: 100%;
        }
    }
</style>
