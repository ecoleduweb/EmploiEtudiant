<script lang="ts">
    import type { StudyProgram } from "../../Models/StudyProgram";

    export let studyProgram: StudyProgram
    export let handleModalClick: () => void

</script>

<button class="studyProgram" on:click={() => handleModalClick()}>
    <div class="Program">
        <div class="info">
            <p class="text">{studyProgram.name}</p>
        </div>
        <img class="image" src="edit.svg" alt="modifier" />
    </div>
</button>

<style scoped>
    .studyProgram {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        width: 90%;
        border-width: 0px;
        border-bottom: 1px solid #00ad9a;
        margin-left: 5.2%;
        background-color: transparent;
        height: 6%;
        border-radius: 4px;
    }
    .info {
        display: flex;
        width: 90%;
        font-size: 1.2rem;
        flex-direction: row;
        justify-content: space-around;
    }

    .text {
        width: 100%;
        text-align: left;
        margin-left: 0.2vw;
    }

    .Program {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        color: white;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        width: 100%;
        height: 100%;
        padding: 5px 0px 5px 0px;
    }
    .studyProgram:hover {
        background-color: #555b66;
    }
    .image {
        width: 30px;
        height: 30px;
    }
</style>
