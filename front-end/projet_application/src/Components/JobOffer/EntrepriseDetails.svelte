<script lang="ts">
    import { formatPhoneNumber } from "../../ts/utils"
    import { getCityNameById } from "../../Service/CityService"
    import type { Enterprise } from "../../Models/Enterprise"
    import { onMount } from "svelte"
    interface Props {
        enterprise: Enterprise
    }
    let { enterprise }: Props = $props()
    let cityName = $state("")
    onMount(async () => {
        if (enterprise.cityId) {
            cityName = await getCityNameById(enterprise.cityId)
        }
    })
</script>

<div class="form-group-vertical">
    <label for="title">Nom : </label>
    <p>{enterprise.name}</p>
</div>
<div class="form-group-vertical">
    <label for="schedule">Adresse : </label>
    <p>{enterprise.address}</p>
</div>
<div class="form-group-vertical">
    <label for="lieu">Courriel : </label>
    <p>{enterprise.email}</p>
</div>
<div class="form-group-vertical">
    <label for="lieu">Téléphone : </label>
    <p>{formatPhoneNumber(enterprise.phone)}</p>
</div>
<div class="form-group-vertical last">
    <label for="lieu">Ville : </label>
    <p>{cityName}</p>
</div>

<style scoped>
    label,
    p {
        color: black;
        display: inline;
    }

    .last {
        padding-bottom: 1%;
    }
</style>
