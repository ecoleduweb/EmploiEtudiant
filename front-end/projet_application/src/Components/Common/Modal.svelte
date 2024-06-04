<script lang="ts">
    export let handleCloseClick: () => void

    const handleButtonClick = (event: MouseEvent) => {
        event.preventDefault()
        handleCloseClick()
    }
</script>

<div class="overlay">
    <div class="modal">
        <slot />
        <button class="close" on:click={handleButtonClick}>
            <img src="cancel.svg" class="image" alt="close" />
        </button>
    </div>
</div>

<style scoped>
    .overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }

    .modal {
        display: flex;
        flex-direction: row;
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        width: 80%;
        max-width: 600px;
        max-height: 100%;
        box-sizing: border-box;
        text-align: center;
    }

    .close {
        background: none;
        border: none;
        cursor: pointer;
        height: 100%;
    }

    .image {
        width: 30px;
        height: 30px;
    }
</style>
