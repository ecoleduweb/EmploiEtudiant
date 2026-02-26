<script lang="ts">
    interface Props {
        handleCloseClick: () => void;
        widthFix?: boolean | undefined;
        children?: import('svelte').Snippet;
    }

    let { handleCloseClick, widthFix = false, children }: Props = $props();

    const handleButtonClick = (event: MouseEvent) => {
        event.preventDefault()
        handleCloseClick()
    }
</script>

<div class="overlay">
    <div class={widthFix ? "modal removeWidth" : "modal"}>
        {@render children?.()}
        <button class="close" onclick={handleButtonClick}>
            <img src="cancel.svg" class="image" alt="close" />
        </button>
    </div>
</div>


<style scoped>
    .modal {
        position: relative;
        display: flex;
        flex-direction: column;
        background-color: #ffffff;
        border-radius: 10px;
        padding: 30px 20px 20px 20px;

        width: 80%;
        max-width: 800px;
        max-height: 100%;
        box-sizing: border-box;
        text-align: center;
    }
    .removeWidth {
        width: unset !important;
    }
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

    .close {
        position: absolute;
        top: -5px;
        right: 8px;
        background: none;
        border: none;
        cursor: pointer;
        padding: 5px;
    }

    .image {
        width: 30px;
        height: 30px;
    }
</style>
