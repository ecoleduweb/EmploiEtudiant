<script lang="ts">
    import type { Option } from "$lib"

    export let studyProgram: Option
    export let handleModalClick: (id: number) => void
</script>

<button class="studyProgram" on:click={() => handleModalClick(studyProgram.value)}>
    <div class="Program">
        <div class="info">
            <p class="text">{studyProgram.label}</p>
        </div>
        <img class="image" src="edit.svg" alt="ajouter" />
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
        width: 20%;
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
