<script lang="ts">
    import type { User } from "../../Models/User"
    interface Props {
        user: User
        handleModalClick: (id: number) => void
    }

    let { user, handleModalClick }: Props = $props()
</script>

<button class="user" onclick={() => handleModalClick(user.id)}>
    <p class="item">
        {#if !user.active}🔒{/if}
        {user.email}
    </p>
    <p class="item">{user.firstName}</p>
    <p class="item info-desktop">{user.lastName}</p>
</button>

<style scoped>
    .item {
        margin: 0;
        padding: 0;
        flex-grow: 1;
        width: 100%;
        font-size: 1.2rem;
        text-align: left;
    }
    .user {
        border: none;
        border-bottom: 1px solid #00ad9a;
        background-color: transparent;
        display: flex;
        flex-direction: row;
        justify-content: flex-start;
        align-items: center;
        color: white;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        padding: 5px 0px 5px 0px;
    }
    .user:hover {
        background-color: #555b66;
    }

    @media (max-width: 540px) {
        .info-desktop {
            display: none;
        }
        .user {
            display: flex;
            width: 90%;
            font-size: 1rem;
            flex-direction: row;
            justify-content: space-around;
            margin-left: 2vw;
        }
    }
</style>
