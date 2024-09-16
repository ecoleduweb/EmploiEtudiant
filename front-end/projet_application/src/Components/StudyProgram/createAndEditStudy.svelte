<script lang="ts">
    import Button from "../Inputs/Button.svelte"
    import type { StudyProgram } from "../../Models/StudyProgram"
    import { onMount } from "svelte"
    export let studyProgram: StudyProgram = {name: "", id: -1}
    export let handleApproveClick: (studyProgram: StudyProgram | void) => void

    let savedName = studyProgram.name

</script>

<div class="main-div">
    <div class="container">
        <div>
            <h5 class="infoTitle">{studyProgram.id <= 0 ? "Veuillez choisir un nouveau nom pour le nouveau programme" : "Veuillez choisir un nouveau nom pour le programme suivant: " + savedName}</h5>
            <input type="text"
                bind:value={studyProgram.name}
                placeholder="Nouveau nom"
                class="input"
            />
        </div>
        <div class="button">
            <Button text={studyProgram.id <= 0 ? "Créer" : "Modifier"} onClick={() => { 
                handleApproveClick(studyProgram)
                savedName = studyProgram.name
            }}/>

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

    @media (max-width: 768px) {
        .infoTitle {
            font-size: 4vw;
        }
        .input {
            font-size: 4vw;
            height: 8vw;
            margin-bottom: 2vh;
        }
    }
</style>
