<script lang="ts">
    import Button from "../Inputs/Button.svelte"
    import { PUT } from "../../ts/server"
    import type { StudyProgram } from "../../Models/StudyProgram"
    export let studyProgram: StudyProgram
    export let handleApproveClick: () => void

    let nameChosen = ""

    const editStudy = async (newName: string) => {
        try {
            const response = await PUT<any, any>(`/studyProgram/studyProgram/${studyProgram.id}`, 
            {
                name: newName
            })

            //window.location.reload() //Pour l'unstant encore, il vas refresh la page (Ça vas venir)
        } catch (error) {
            console.error("Error editing study program:", error)
        }
        handleApproveClick()
    }
</script>

<div class="main-div">
    <div class="container">
        <div>
            <h5 class="infoTitle">Veuillez choisir un nouveau nom pour le programme suivant: {studyProgram.name}</h5>
            <input type="text"
                bind:value={nameChosen}
                placeholder="Nouveau nom"
                class="input"
            />
        </div>
        <div class="button">
            <Button text="Modifier" onClick={() => editStudy(nameChosen)} />

            <Button text="Annuler" onClick={() => handleApproveClick()} />
        </div>
    </div>
</div>

<style scoped>
    .container {
        width: 100%;
        display: flex;
        flex-direction: column;
        text-align: center;
        justify-content: space-between;
        color: white;
        border-radius: 4px;
        transition: background-color 0.3s ease;
    }
    .input {
        width: 100%;
        height: 3vw;
        border-radius: 4px;
        border: 1px solid #00ad9a;
        background-color: transparent;
        margin-bottom: 1.5vw;
    }
    .button {
        display: flex;
        flex-direction: row;
        justify-content: center;
        gap: 1vw;
    }
    .main-div {
        flex-direction: column;
        margin: auto;
    }
    .infoTitle 
    {
        color: black;
    }
</style>
