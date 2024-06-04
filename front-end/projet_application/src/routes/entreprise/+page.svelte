<script lang="ts">
    import "../../styles/global.css"
    import { onMount } from "svelte"
    import { writable } from "svelte/store"
    import { GET } from "../../ts/server"
    import type { Entreprise } from "../../Models/Entreprise"
    import EntrepriseRow from "../../Components/Entreprise/EntrepriseRow.svelte"
    import Entreprises from "../../Components/Entreprise/Entreprises.svelte"
    import Button from "../../Components/Inputs/Button.svelte"
    import AddEntreprise from "../../Components/Entreprise/AddEntreprise.svelte"

    const modal = writable(false)
    const modalAdd = writable(false)
    const selectedEntrepriseId = writable(0)
    const openModal = (id: number) => {
        modal.set(true)
        selectedEntrepriseId.set(id)
    }
    const closeModal = () => {
        modal.set(false)
    }
    const handleEntrepriseClick = (offreId: number) => {
        openModal(offreId)
    }
    const openModalAdd = () => {
        modalAdd.set(true)
    }
    const closeModalAdd = () => {
        modalAdd.set(false)
        getEnterprises()
    }
    const handleEntreprise = () => {
        openModalAdd()
    }

    const entreprises = writable<Entreprise[]>([])
    const getEnterprises = async () => {
        try {
            const response = await GET<any>("/enterprise/getEnterprises")
            entreprises.set(response)
        } catch (error) {
            console.error("Error fetching job offers:", error)
        }
    }
    onMount(getEnterprises)
</script>

<main>
    <section class="haut">
        <div class="haut-gauche">
            <div class="divFlex">
                <Button
                    onClick={handleEntreprise}
                    text="Créer une nouvelle entreprise"
                />
            </div>
        </div>
    </section>
    <section class="haut">
        <div class="haut-gauche">
            <h1 class="title">
                <span class="text">ENTREPRISES </span>
                <span class="text"> EXISTANTES</span>
            </h1>
        </div>
    </section>
    <section class="offres">
        {#each $entreprises as entreprise}
            <EntrepriseRow
                {entreprise}
                handleModalClick={handleEntrepriseClick}
            />
        {/each}
    </section>
    {#if $modal}
        {#each $entreprises as entreprise}
            {#if entreprise.id === $selectedEntrepriseId}
                <Entreprises {entreprise} handleEntrepriseClick={closeModal} />
            {/if}
        {/each}
    {/if}
    {#if $modalAdd}
        <AddEntreprise handleEntrepriseClick={closeModalAdd} />
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
        width: 85%;
        margin-bottom: 30px;
    }
    .haut-gauche {
        display: flex;
        flex-direction: column;
        width: 50%;
        margin-left: 5.2%;
    }
    .divFlex {
        display: flex;
        margin-top: 20px;
    }
</style>
