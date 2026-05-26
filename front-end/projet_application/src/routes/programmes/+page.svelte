<script lang="ts">
    import "../../styles/global.css"
    import { GET, POST, PUT } from "../../ts/server"
    import { onMount } from "svelte"
    import Modal from "../../Components/Common/Modal.svelte"
    import Button from "../../Components/Inputs/Button.svelte"
    import CreateAndEditStudy from "../../Components/StudyProgram/createAndEditStudy.svelte"
    import { studyPrograms } from "$lib"
    import StudyProgramRow from "../../Components/StudyProgram/ProgramRow.svelte"
    import type { StudyProgram } from "../../Models/StudyProgram"

    let showModal = $state(false)
    let selectedProgram: StudyProgram | undefined = $state(undefined)

    const openModal = () => {
        showModal = true
    }

    const closeModal = () => {
        showModal = false
        refresh()
    }

    const handleStudyProgramClick = (studyProgram: StudyProgram) => {
        selectedProgram = studyProgram
        openModal()
        refresh()
    }

    const openCreateStudy = () => {
        selectedProgram = undefined
        showModal = true
    }

    const addStudy = async (offer: StudyProgram) => {
        try {
            const response = await POST<any, any>(`/studyProgram/new`, {
                name: offer.name,
            })

            //window.location.reload() //Pour l'unstant encore, il vas refresh la page (Ça vas venir)
        } catch (error) {
            console.error("Error creating study program:", error)
        }

        await refresh()
    }

    const editStudy = async (offer: StudyProgram) => {
        try {
            const response = await PUT<StudyProgram, any>(
                `/studyProgram/${offer.id}`,
                offer,
            )
            studyPrograms.update((programs) =>
                programs.map((program) =>
                    program.id === offer.id
                        ? { ...program, ...offer }
                        : program,
                ),
            )
        } catch (error) {
            console.error("Error editing study program:", error)
        }
    }

    const upsertStudyProgram = async (studyProgram: StudyProgram | void) => {
        if (studyProgram !== undefined) {
            //Existant
            if (studyProgram.id >= 0) {
                await editStudy(studyProgram)
            }
            //Nouveau
            else {
                await addStudy(studyProgram)
            }
        }
        closeModal()
    }

    const getStudyPrograms = async () => {
        try {
            let response = await GET<any>(`/studyProgram/all`)

            if (response) studyPrograms.set(response)
        } catch (error) {
            console.error("Error fetching job offers:", error)
        }
    }

    async function refresh() {
        await getStudyPrograms()
    }

    onMount(refresh)
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
                    D'ÉTUDES</span
                >
            </h1>
        </div>
    </section>
    <section class="StudyPrograms">
        {#each $studyPrograms as studyProgram}
            <StudyProgramRow
                {studyProgram}
                handleModalClick={() => handleStudyProgramClick(studyProgram)}
            />
        {/each}
    </section>
    {#if showModal}
        <Modal handleCloseClick={closeModal}>
            <CreateAndEditStudy
                studyProgram={selectedProgram}
                handleApproveClick={(offer) => upsertStudyProgram(offer)}
            />
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
    .divFlex {
        display: flex;
        margin-top: 20px;
    }

    @media (max-width: 768px) {
        .text {
            font-size: 6vw;
            margin-left: 2vw !important;
        }
        .title {
            display: flex;
            justify-content: space-between;
            flex-direction: row;
            width: 100%;
        }
    }
</style>
