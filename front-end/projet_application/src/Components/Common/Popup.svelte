<script lang="ts">
    import Modal from "./Modal.svelte"
    import Button from "../Inputs/Button.svelte"
    export let handleApproveClick: () => void
    export let approbationMessage: string

</script>

<Modal handleCloseClick={handleApproveClick}>
    <div class="main-div">
        <div class="container">
            <div>
                <h5 class="infoTitle">{approbationMessage}</h5>
            </div>
            <div class="button">
                <Button text="Confirmer" onClick={handleApproveClick}/>
            </div>
        </div>
    </div>
</Modal>

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

    .infoTitle {
        color: black;
        font-size: 1.6vw;
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
</style>
