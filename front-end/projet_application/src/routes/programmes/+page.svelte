<script lang="ts">
    import "../../styles/global.css"
    import { GET, POST, PUT } from "../../ts/server"
    import { onMount } from "svelte"
    import Modal from "../../Components/Common/Modal.svelte"
    import Button from "../../Components/Inputs/Button.svelte"
    import CreateAndEditStudy from "../../Components/StudyProgram/createAndEditStudy.svelte"
    import { studyPrograms } from "$lib"
    import type { Option } from "$lib"
    import StudyProgramRow from "../../Components/StudyProgram/ProgramRow.svelte"
    import type { StudyProgram } from "../../Models/StudyProgram"

    let createStudyProgram = false
    let editStudyProgram = false
    let selectedProgram: StudyProgram | undefined = undefined


    const openEditModal = (id: number) => {
        editStudyProgram = true
        $studyPrograms.map((x: any) => {
            if (x.id == id) 
            {
                selectedProgram = x
            }
        });
    }

    const closeEditModal = () => {
        editStudyProgram = false
        refresh()
    }

    const handleStudyProgramClick = (offer: StudyProgram) => {
        openEditModal(offer.id)
        refresh()
    }

    const openCreateStudy = () => {
        selectedProgram = undefined
        createStudyProgram = true
    }
    
    const closeCreateStudy = () => {
        createStudyProgram = false
        refresh()
    }



    const addStudy = async (offer: StudyProgram) => {
        try {
            const response = await POST<any, any>(`/studyProgram/new`, 
            {
                name: offer.name
            })

            //window.location.reload() //Pour l'unstant encore, il vas refresh la page (Ça vas venir)
        } catch (error) {
            console.error("Error creating study program:", error)
        }

        await refresh()
    }

    const editStudy = async (offer: StudyProgram) => {
        try {
            const response = await PUT<any, any>(`/studyProgram/studyProgram/${offer.id}`, 
            {
                name: offer.name
            })

            //window.location.reload() //Pour l'unstant encore, il vas refresh la page (Ça vas venir)
        } catch (error) {
            console.error("Error editing study program:", error)
        }

        await refresh()
    }



    const upsertStudyProgram = (offer: StudyProgram | void) => 
    {
        if (offer !== undefined)
        {
            if (offer.id >= 0) //Existant
            {
                editStudy(offer)
            }
            else //Nouveau 
            {
                addStudy(offer)
            }
        }
        //Si offer.id >= 0, veut dire existant
        //Si offer.id = -1, veut dire nouveau
        //Si offer = undefined, veut dire annuler
    }

    const getStudyPrograms = async () => {
        try {
            let response = await GET<any>(
            `/studyProgram/studyPrograms`
            )

            if (response)
            studyPrograms.set(response) 
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
                    DISPONIBLES</span
                >
            </h1>
        </div>
    </section>
    <section class="StudyPrograms">
        {#each $studyPrograms as studyProgram}
            <StudyProgramRow {studyProgram} handleModalClick={() => handleStudyProgramClick(studyProgram)}/>
        {/each}
    </section>
    {#if editStudyProgram}
        <Modal handleCloseClick={closeEditModal}>
            <CreateAndEditStudy studyProgram={selectedProgram} handleApproveClick={(offer) => upsertStudyProgram(offer)} />
        </Modal>
    {/if}

    {#if createStudyProgram}
        <Modal handleCloseClick={closeCreateStudy}>
            <CreateAndEditStudy studyProgram={selectedProgram} handleApproveClick={(offer) => upsertStudyProgram(offer)} />
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
