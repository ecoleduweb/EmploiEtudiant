<script lang="ts">
    import "../../styles/global.css"
    import { writable } from "svelte/store"
    import { GET } from "../../ts/server"
    import { onMount } from "svelte"
    import type { StudyProgram } from "../../Models/StudyProgram"
    import StudyProgramRow from "../../Components/StudyProgram/StudyProgramRow.svelte"
    import Modal from "../../Components/Common/Modal.svelte"
    import ModifyStudy from "../../Components/StudyProgram/ModifyStudy.svelte"
    import Button from "../../Components/Inputs/Button.svelte"
    import CreateStudy from "../../Components/StudyProgram/CreateStudy.svelte"

    const modal = writable(false)
    let createStudyProgram = false
    const selectedProgramId = writable(0)
    const openModal = (id: number) => {
        modal.set(true)
        selectedProgramId.set(id)
    }
    const closeModal = () => {
        modal.set(false)
        restart()
    }
    const openCreateStudy = () => {
        createStudyProgram = true
    }
    const closeCreateStudy = () => {
        createStudyProgram = false
        restart()
    }
    const handleStudyProgramClick = (offreId: number) => {
        openModal(offreId)
        restart()
    }

    const studyPrograms = writable<StudyProgram[]>([])
    const getStudyPrograms = async () => {
        try {
            const response = await GET<any>("/studyProgram/studyPrograms")
                studyPrograms.set(response)
        } catch (error) {
            console.error("Error fetching job offers:", error)
        }
    }

    let unique = {} // Chaque {} sont unique

    async function restart() {
        await getStudyPrograms()
        unique = {}
    }

    onMount(getStudyPrograms)
</script>

<main>
    <section class="haut">
        <div class="haut-gauche">
            <div class="divFlex">
                <Button
                    onClick={openCreateStudy}
                    text="Créer une nouvelle enterprise"
                />
            </div>
        </div>
    </section>
    <section class="haut">
        <div class="haut-gauche">
            <h1 class="title">
                <span class="text">PROGRAMMES </span><span class="text">
                    DISPONIBLES</span
                >
            </h1>
        </div>
    </section>
    {#key unique}
        <section class="StudyPrograms">
            {#each $studyPrograms as studyProgram}
                <StudyProgramRow {studyProgram} handleModalClick={handleStudyProgramClick}/>
            {/each}
        </section>
    {/key}
    {#if $modal}
        {#each $studyPrograms as studyProgram}
            {#if studyProgram.id === $selectedProgramId}
                <Modal handleCloseClick={closeModal}>
                    <ModifyStudy {studyProgram} handleApproveClick={closeModal} />
                </Modal>
            {/if}
        {/each}
    {/if}

    {#if createStudyProgram}
        <Modal handleCloseClick={closeCreateStudy}>
            <CreateStudy handleApproveClick={closeCreateStudy} />
        </Modal>
    {/if}

</main>

<style scoped>
    main {
        height: 100%;
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
    .StudyPrograms {
        width: fit-content;
        display: flex;
        flex-direction: column;
        width: 100%;
    }
    .StudyPrograms {
        width: fit-content;
        display: flex;
        flex-direction: column;
        width: 100%;
    }

    @media screen and (max-width: 900px) and (min-width: 300px) 
    {
        .text 
        {
            font-size: 3.3vw;
        }
    }
</style>
