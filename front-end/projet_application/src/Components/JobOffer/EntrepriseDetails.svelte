<script lang="ts">
    import MultiSelect from "svelte-multiselect"
    import type { Writable } from "svelte/store"
    export let enterprise: any
    export let selectedCity: any
</script>

<div class="form-group-vertical">
    <label for="title">Nom*</label>
    <p>{enterprise.name}</p>
</div>
<div class="form-group-vertical">
    <label for="schedule">Adresse*</label>
    <p>{enterprise.address}</p>
</div>
<div class="form-group-vertical">
    <label for="lieu">Courriel*</label>
    <p>{enterprise.email}</p>
</div>
<div class="form-group-vertical">
    <label for="lieu">Téléphone*</label>
    <p>{enterprise.phone}</p>
</div>
<div class="form-group-vertical">
    <label for="lieu">Ville*</label>
    <p>{selectedCity[0].label}</p>
</div>