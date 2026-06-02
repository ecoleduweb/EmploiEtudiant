<script lang="ts">
    import type { Enterprise } from "../../Models/Enterprise"
    import { formatPhoneNumber } from "../../ts/utils"

    type Props = {
        enterprise: Enterprise
        handleModalClick: () => void
        cityName?: string
    }

    let { enterprise, handleModalClick, cityName = "" }: Props = $props()

    let formattedPhone = $derived(formatPhoneNumber(enterprise.phone))
</script>

<button class="enterprise" onclick={() => handleModalClick()}>
    <div class="row">
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
        <div class="info">
            <ul>
                {#each enterprise.users as user}
                    <li class="text">{user.firstName} {user.lastName}</li>
                {/each}
            </ul>
        </div>
        <img class="image" src="edit.svg" alt="modifier" />
    </div>
</button>

<style scoped>
    .enterprise {
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

    .row {
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
    .row:hover {
        background-color: #555b66;
    }
    .image {
        width: 30px;
        height: 30px;
    }
</style>
