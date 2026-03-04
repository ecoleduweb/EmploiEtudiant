<script lang="ts">
    import type { Enterprise } from "../../Models/Enterprise"
    export let enterprise: Enterprise
    export let handleModalClick: () => void
    export let cityName: string = ""
    import { formatPhoneNumber } from "../../ts/utils"

    $: formattedPhone = formatPhoneNumber(enterprise.phone)
</script>

<button class="enterprise" on:click={() => handleModalClick()}>
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
        height: 100%;
        padding: 5px 0px 5px 0px;
    }
    .emploi:hover {
        background-color: #555b66;
    }
    .image {
        width: 30px;
        height: 30px;
    }
</style>
