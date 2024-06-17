<script lang="ts">
    import "../../styles/global.css"
    import { writable } from "svelte/store"
    import { GET } from "../../ts/server"
    import { onMount } from "svelte"
    import type { StudyProgram } from "../../Models/StudyProgram"
    import StudyProgramRow from "../../Components/StudyProgram/StudyProgramRow.svelte"
    import Modal from "../../Components/Common/Modal.svelte"
    import Button from "../../Components/Inputs/Button.svelte"
    import CreateAndModifyStudy from "../../Components/StudyProgram/CreateAndModifyStudy.svelte"
    import { studyPrograms } from "$lib"
    import type { Option } from "$lib"

    let createStudyProgram = false
    let editStudyProgram = false
    let selectedProgram: Option | undefined = undefined
    const openModal = (id: number) => {
        editStudyProgram = true

        $studyPrograms.map((x: any) => {
            if (x.value == id) 
            {
                selectedProgram = x
            }
        });
    }
    const closeModal = () => {
        editStudyProgram = false
        refresh()
    }
    const openCreateStudy = () => {
        createStudyProgram = true
    }
    const closeCreateStudy = () => {
        createStudyProgram = false
        refresh()
    }
    const handleStudyProgramClick = (offerId: number) => {
        openModal(offerId)
        refresh()
    }

    const getStudyPrograms = async () => {
        try {
            let response = await GET<any>(
            `/studyProgram/studyPrograms`
            )

            if (response)
            studyPrograms.set( response.map((x: any) => ({"label": x.name, "value": x.id})) ) 
        } catch (error) {
            console.error("Error fetching job offers:", error)
        }
    }

    async function refresh() {
        await getStudyPrograms()
    }

    onMount(getStudyPrograms)
</script>

<main>
    <section class="haut">
        <div class="haut-gauche">
            <div class="divFlex">
                <Button
                    onClick={openCreateStudy}
                    text="Créer un nouveau programme"
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
    <section class="StudyPrograms">
        {#each $studyPrograms as studyProgram}
            <StudyProgramRow {studyProgram} handleModalClick={handleStudyProgramClick}/>
        {/each}
    </section>
    {#if editStudyProgram}
        <Modal handleCloseClick={closeModal}>
            <CreateAndModifyStudy settings={( { mode: 1, studyProgram: selectedProgram} )} handleApproveClick={closeModal} />
        </Modal>
    {/if}

    {#if createStudyProgram}
        <Modal handleCloseClick={closeCreateStudy}>
            <CreateAndModifyStudy settings={( { mode: 0, studyProgram: undefined} )} handleApproveClick={closeCreateStudy} />
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
