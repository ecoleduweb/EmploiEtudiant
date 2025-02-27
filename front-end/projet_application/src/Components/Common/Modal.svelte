<script lang="ts">
    export let handleCloseClick: () => void
    export let widthFix: boolean | undefined = false
    export let disableOverlayClose: boolean = false

    const handleButtonClick = (event: MouseEvent) => {
        event.preventDefault()
        handleCloseClick()
    }

    // Ferme le modal si l'utilisateur clique à l'extérieur du modal
    const handleOverlayClick = (event: MouseEvent) => {
        if (!disableOverlayClose && (event.target as HTMLElement).classList.contains('overlay')) {
            handleCloseClick()
        }
    }


    // Ferme le modal si l'utilisateur appuie sur la touche Escape
    const handleKeyDown = (event: KeyboardEvent) => {
        if (event.key === 'Escape') {
            handleCloseClick()
        }
    }

        // Ajoute l'écouteur d'événements pour la touche Escape lorsque le composant est monté
        import { onMount, onDestroy } from 'svelte'

        onMount(() => {
            window.addEventListener('keydown', handleKeyDown)
        })

        onDestroy(() => {
            window.removeEventListener('keydown', handleKeyDown)
        })
</script>

<div class="modal-container">
    <div class="overlay" on:click={handleOverlayClick}>
        <div class={widthFix ? "modal removeWidth" : "modal"}>
            <slot />
            <button class="close" on:click={handleButtonClick}>
                <img src="cancel.svg" class="image" alt="close" />
            </button>
        </div>
    </div>
</div>

<style scoped>
    .modal-container {
        margin: 20px;
        border: 2px solid #00ad9a;
    }

    .overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(5px); /* Effet de flou */
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    animation: fadeIn 0.3s ease-in-out; /* Animation de l'overlay */

    }

    /* Animation d’apparition de l'overlay */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    /* Animation d’ouverture du modal */
    @keyframes scaleIn {
        from { transform: scale(0.9); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    .modal {
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        animation: scaleIn 0.2s ease-in-out; /* Animation du modal */
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        width: 90%;
        max-width: 800px;
        max-height: 100%;
        box-sizing: border-box;
        text-align: center;
        border: 2px solid #00ad9a;
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
        background: none;
        border: none;
        cursor: pointer;
        height: 100%;
    }

    .image {
        width: 30px;
        height: 30px;
    }

    .image:hover {
        transform: scale(1.2);
        filter: brightness(1.2);
    }

</style>
