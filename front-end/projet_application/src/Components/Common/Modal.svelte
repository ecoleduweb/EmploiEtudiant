<script lang="ts">
    export let handleModalClick: () => void;

    const handleButtonClick = (event: MouseEvent) => {
        event.preventDefault();
        handleModalClick();
    };
</script>

<button class="overlay" on:click={handleButtonClick}>
    <button class="modal" on:click|stopPropagation>
        <slot />
        <button class="close" on:click={handleButtonClick}>
            <img src="cancel.svg" class="image" alt="close" />
        </button>
    </button>
</button>

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
        box-sizing: border-box;
        text-align: center;
    }

    .close {
        width: 5%;
        background: none;
        border: none;
        top: 10px;
        right: 10px;
        cursor: pointer;
    }

    .image {
        width: 30px;
        height: 30px;
    }
</style>
