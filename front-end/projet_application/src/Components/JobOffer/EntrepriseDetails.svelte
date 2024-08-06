<script lang="ts">
    export let enterprise: any
    export let selectedCity: any

    console.log(selectedCity)
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
    <p>{enterprise.phone}</p>
</div>
<div class="form-group-vertical last">
    <label for="lieu">Ville : </label>
    
    <p>{selectedCity?.length ? selectedCity[0].label : 'En chargement'}</p>
</div>

<style scoped>
    label, p {
        color: black;
        display: inline;
    }

    .last {
        padding-bottom: 1%;
    }
</style>