<script lang="ts">
    import "../../styles/global.css"
    import Header from "../../Components/Common/Header.svelte"
    import Footer from "../../Components/Common/Footer.svelte"
    import { onMount } from "svelte"
    import { writable } from "svelte/store"
    import { GET } from "../../ts/server"
    import type { Enterprise } from "../../Models/Enterprise"
    import EnterpriseRow from "../../Components/Enterprise/EnterpriseRow.svelte"
    import Enterprises from "../../Components/Enterprise/Enterprises.svelte"
    import Button from "../../Components/Inputs/Button.svelte"
    import AddEnterprise from "../../Components/Enterprise/AddEnterprise.svelte"

    const modal = writable(false)
    const modalAdd = writable(false)
    const selectedEnterpriseId = writable(0)
    const openModal = (id: number) => {
        modal.set(true)
        selectedEnterpriseId.set(id)
    }
    const closeModal = () => {
        modal.set(false)
    }
    const handleEnterpriseClick = (offreId: number) => {
        openModal(offreId)
    }
    const openModalAdd = () => {
        modalAdd.set(true)
    }
    const closeModalAdd = () => {
        modalAdd.set(false)
        getEnterprises()
    }
    const handleEnterprise = () => {
        openModalAdd()
    }

    const enterprises = writable<Enterprise[]>([])
    const getEnterprises = async () => {
        try {
            const response = await GET<any>("/enterprise/all")
            enterprises.set(response)
        } catch (error) {
            console.error("Error fetching job offers:", error)
        }
    }
    onMount(getEnterprises)
</script>

<Header />
<main>
    <section class="haut">
        <div class="haut-gauche">
            <div class="divFlex">
                <Button
                    onClick={handleEnterprise}
                    text="Créer une nouvelle enterprise"
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
        {#each $enterprises as enterprise}
            <EnterpriseRow
                {enterprise}
                handleModalClick={handleEnterpriseClick}
            />
        {/each}
    </section>
    {#if $modal}
        {#each $enterprises as enterprise}
            {#if enterprise.id === $selectedEnterpriseId}
                <Enterprises {enterprise} handleEnterpriseClick={closeModal} />
            {/if}
        {/each}
    {/if}
    {#if $modalAdd}
        <AddEnterprise handleEnterpriseClick={closeModalAdd} />
    {/if}
</main>
<Footer />

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
