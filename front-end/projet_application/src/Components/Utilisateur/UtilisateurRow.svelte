<script lang="ts">
    import type { User } from "../../Models/User";
    export let user: User;
    import { GET } from "../../ts/server";
    import { onMount } from "svelte";
    export let handleModalClick: (id: number) => void;

</script>
<div class="userTitre">
    <div class="user">
        <div class="info">
            <p class="text">{user.email}</p>
            <p class="text">{user.firstName}</p>
            <p class="text">{user.lastName}</p>
        </div>
            <button class="button" on:click={() => handleModalClick(user.id)}>
                <img class="image" src="check.svg" alt="approve" />
            </button>
    </div>
    </div>

<style scoped>
    .userTitre {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        width: 100%;
        border-width: 0px;
        border-bottom: 1px solid #00ad9a;
        background-color: transparent;
    }
    .info {
        display: flex;
        width: 100%;
        font-size: 1.15rem;
        flex-direction: row;
        justify-content: space-around;
    }
    .text {
        width: 20%;
    }
    .user {
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
    .user:hover {
        background-color: #555b66;
    }
    .image {
        width: 30px;
        height: 30px;
    }
    .button {
        background-color: transparent;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
        border-radius: 4px;
    }
</style>
