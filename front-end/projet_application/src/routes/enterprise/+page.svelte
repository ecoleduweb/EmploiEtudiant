<script lang="ts">
    import "../../styles/global.css"
    import { onMount } from "svelte"
    import type { Enterprise } from "../../Models/Enterprise"
    import EnterpriseRow from "../../Components/Enterprise/EnterpriseRow.svelte"
    import CreateEditEnterprise from "../../Components/Enterprise/CreateEditEnterprise.svelte"
    import Button from "../../Components/Inputs/Button.svelte"
    import Modal from "../../Components/Common/Modal.svelte"
    import { fetchEnterprises } from "../../Service/EnterpriseService"
    import type { User } from "../../Models/User"

    let showCreateEditEnterpriseModal = $state(false)
    let selectedEnterprise: Enterprise | undefined = $state(undefined)
    let searchTerm = $state("")
    let enterprises = $state<Enterprise[]>([])
    let filteredEnterprises: Enterprise[] = $state([])

    const closeModal = () => {
        showCreateEditEnterpriseModal = false
    }

    const handleShowCreateEditEnterpriseModal = (
        enterprise: Enterprise | undefined = undefined,
    ) => {
        selectedEnterprise = enterprise
        showCreateEditEnterpriseModal = true
    }

    const normalize = (str: string) => {
        return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    }

    const handleApproveClick = async (
        upsertedEnterprise: Enterprise | void,
    ) => {
        if (upsertedEnterprise !== undefined) {
            const index = enterprises.findIndex(
                (x) => x.id === upsertedEnterprise.id,
            )
            if (index !== -1) {
                enterprises[index] = upsertedEnterprise
            } else {
                enterprises = [upsertedEnterprise, ...enterprises]
            }
        }
        closeModal()
    }

    onMount(async () => {
        enterprises = await fetchEnterprises()
    })

    $effect(() => {
        if (enterprises) {
            const search = searchTerm.toLowerCase()
            filteredEnterprises = enterprises.filter(
                (enterprise) =>
                    normalize(enterprise.name).toLowerCase().includes(search) ||
                    normalize(enterprise.email)
                        .toLowerCase()
                        .includes(search) ||
                    normalize(enterprise.address)
                        .toLowerCase()
                        .includes(search) ||
                    normalize(enterprise.phone)
                        .toLowerCase()
                        .includes(search) ||
                    normalize(enterprise.city?.city ?? "")
                        .toLowerCase()
                        .includes(search) ||
                    normalize(
                        enterprise.users
                            ?.map((x: User) => x.firstName + " " + x.lastName)
                            .join(" ") ?? "",
                    )
                        .toLowerCase()
                        .includes(search),
            )
        }
    })
</script>

<main>
    <section class="top">
        <div class="top-left">
            <div class="flex-container">
                <Button
                    onClick={() => handleShowCreateEditEnterpriseModal()}
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
        <div class="row">
            <div class="info">
                <p class="text">Nom</p>
            </div>
            <div class="info">
                <p class="text">Courriel</p>
            </div>
            <div class="info">
                <p class="text">Téléphone</p>
            </div>
            <div class="info">
                <p class="text">Adresse</p>
            </div>
            <div class="info">
                <p class="text">Ville</p>
            </div>
            <div class="info">
                <p class="text">Utilisateurs</p>
            </div>
            <div class="info"></div>
        </div>
        {#each filteredEnterprises as enterprise}
            <EnterpriseRow
                {enterprise}
                cityName={enterprise.city?.city}
                handleModalClick={() =>
                    handleShowCreateEditEnterpriseModal(enterprise)}
            />
        {/each}
    </section>
    {#if showCreateEditEnterpriseModal}
        <Modal handleCloseClick={closeModal}>
            <CreateEditEnterprise
                enterpriseToEdit={selectedEnterprise}
                onApproveClick={(upsertedEnterprise) =>
                    handleApproveClick(upsertedEnterprise)}
            />
        </Modal>
    {/if}
</main>

<style scoped>
    .row {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        color: white;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        width: 90%;
        margin-left: 5.2%;
    }
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
