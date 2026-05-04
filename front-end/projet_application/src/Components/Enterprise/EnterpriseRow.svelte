<script lang="ts">
    import type { Enterprise } from "../../Models/Enterprise"
    import { formatPhoneNumber } from "../../ts/utils"
    import { GET } from "../../ts/server"
    import { onMount } from "svelte"

    type Props = {
        enterprise: Enterprise
        handleModalClick: () => void
        cityName?: string
    }

    let { enterprise, handleModalClick, cityName = "" }: Props = $props()
    let formattedPhone = $derived(formatPhoneNumber(enterprise.phone))

    let Users = $derived(
        enterprise.users?.map((u: any) => {
            const fullName = `${u.firstName} ${u.lastName}`.trim();
            return {
                label: fullName.length > 0 ? fullName : u.email,
                value: u.id
            };
        }) ?? []
    );
  
  
</script>

<button class="enterprise" onclick={() => handleModalClick()}>
    <div class="emploi">
        <div class="info">
            <p class="text">{enterprise.name}</p>
        </div>
        <div class="info">
            <p class="text">{enterprise.email}</p>
        </div>
        <div class="info">
            <p class="text">{formattedPhone}</p>
        </div>
        <div class="info">
            <p class="text">{enterprise.address}</p>
        </div>
        <div class="info">
            <p class="text">{cityName}</p>
        </div>

        <div class="assigned-users-list">
            <span class="list-label">Admins :</span>
            {#if Users.length > 0}
                <div class="users-vertical-stack">
                    {#each Users as user}
                        <div class="user-item" title={user.label}>
                            {user.label}
                        </div>
                    {/each}
                </div>
            {:else}
                <p  class="no-user">Aucun utilisateur n'est séléctionné</p>
            {/if}
        </div>
        
        <img class="image" src="edit.svg" alt="modifier" />
    </div>
</button>

<style scoped>
    .assigned-users-list {
        width: 20%;
        display: flex;
        flex-direction: column;
        gap: 5px;
        padding: 5px;
    }
    .enterprise {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        width: 90%;
        border-width: 0px;
        border-bottom: 1px solid #00ad9a;
        margin-left: 5.2%;
        background-color: transparent;
        height: auto;
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
    .list-label {
        font-size: 0.8rem;
        color: #00ad9a;
        font-weight: bold;
        margin-bottom: 4px;
    }
    .users-vertical-stack {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .user-item {
        background-color: rgba(0, 173, 154, 0.1);
        border: 1px solid #00ad9a;
        border-radius: 4px;
        padding: 2px 8px;
        font-size: 0.85rem;
        color: white;
        text-align: center;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .no-user {
        font-size: 0.9rem;
        color: #888;
        margin: 0;
    }
    .emploi {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        color: white;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        width: 100%;
        height: auto;
        padding: 10px 0px;
    }
    .emploi:hover {
        background-color: #555b66;
    }
    .image {
        width: 30px;
        height: 30px;
    }
</style>