<script lang="ts">
    import "../../styles/global.css";
    import Button from "../../Components/Inputs/Button.svelte";
    import MultiSelect from 'svelte-multiselect';
    import type { jobOffer } from "../../Models/Offre";
    import { writable, type Writable } from 'svelte/store';
    import { POST } from "../../ts/server";
    import * as yup from "yup";
    import { extractErrors } from "../../ts/utils";
    import type { Entreprise } from "../../Models/Entreprise";
    import { goto } from '$app/navigation';

    const schema = yup.object().shape({
    title: yup.string().required("Le titre du poste est requis"),
    address: yup.string().required("L'adresse du lieu de travail est requise"),
    description: yup.string().required("La description de l'offre est requise"),
    dateEntryOffice: yup.string().required("La date d'entrée en fonction est requise").test('is-date', "Veuillez choisir une date valide !", value => {
    return !isNaN(Date.parse(value));
    }),
    deadlineApply: yup.string().required("La date limite de l'offre est requise").test('is-date', "Veuillez choisir une date valide !", value => {
    return !isNaN(Date.parse(value));
    }),
    email : yup.string().matches(/\.[a-z]+$/, "Le courriel doit être de format valide : courriel@domaine.ca").email("Le courriel n'est pas valide").required("Le courriel est requis"),
    hoursPerWeek: yup.string().required("Le nombre d'heure par semaine est requis").test('is-number', "Veuillez entrer un nombre d'heure valide !", value => {
      return !isNaN(Number(value)) && Number(value) > 0;
    }),
    scheduleId: yup.number().required("Le type d'emploi est requis").min(0, "Le type d'emploi est requis"),
    idProgramme: yup.array().min(1, "Le programme visé est requis"),
    offerLink: yup.string().matches(/^(http|https):\/\/[^ "]+$/, "Le lien doit être de format valide : https://www.exemple.ca").url("Le lien doit être de format valide : https://www.exemple.ca").required("Le lien de l'offre est requis"),
  });

    let scheduleSelected: { label: string; value: number }[] = [];
    let scheduleFromExistingOffer: [] = []; // valeur de l'offre actuel (lorsque l'on editera une offre existante)
    let scheduleOption = [
    { label: "Temps plein", value: 1 },
    { label: "Emploi d'été", value: 2 },
    { label: "Temps partiel", value: 3 }
];

// SECTION ENTREPRISE --------------------------------------------
   let enterprise: Entreprise = {
        name: "",
        email: "",
        phone: "",
        address: "",
        cityId: 0,
        isTemporary: true,
    };

    let villeSelected: { label: string; value: number }[] = [];
    let villeFromSelectedEntreprise: [] = [];
    let villeOption = [
        { label: "Trois-Pistoles", value: 1 },
        { label: "Rivière-du-Loup", value: 2 },
        { label: "Squatec", value: 3 },
        { label: "Chibougamau", value: 4 },
        { label: "Amqui", value: 5 },
        { label: "Trois-Rivière", value: 6 },
        { label: "Lévis", value: 7 },
    ];
    //--------------------------------------------------

    let errorsProgramme: string = ""; // Define a variable to hold the error message for selected program

    const handleSubmit = async () => {
        try {
            await schema.validate(offre, { abortEarly: false });
            errors = {
                title: "",
                address: "",
                description: "",
                dateEntryOffice: "",
                deadlineApply: "",
                email: "",
                hoursPerWeek: "",
                compliantEmployer: false,
                internship: false,
                offerLink: "",
                offerStatus: 0,
                urgent: false,
                active: true,
                salary: "",
                scheduleId: 0,
                employerId: 0,
            };
            const requestData = {
                enterprise: enterprise,
            };
            const response = await POST<any, any>("/jobOffer/createEnterprise", requestData);
            goto('/entreprises');
        } catch (err) {
            console.log(err);
            if (err instanceof yup.ValidationError) {
                errors = extractErrors(err);
            }
            // Handle the case where no program is selected
            if (programmeSelected.length === 0) {
                errorsProgramme = "Le programme visé est requis";
            } else {
                errorsProgramme = "";
            }
        }
    }
</script>

<button class="entreprise" on:click={() => handleModalClick(entreprise.id)}>
    <div class="emploi">
        <div class="container">
            <form on:submit|preventDefault={handleSubmit} class="form-offre">
              <!-- -------------------SECTION ENTREPRISE------------------------------ -->
              <!-- --AJOUTER VALIDATION SI COMPTE A DEJA UN ENTREPRISE POUR CACHER CE FORMULAIRE------- -->
                <h1 class="title">Créer une nouvelle entreprise</h1>
                <div class="form-group-vertical">
                  <label for="title">Nom*</label>
                  <input type="text" bind:value={enterprise.name} class="form-control" id="titre" />
                </div>
                <div class="form-group-vertical">
                  <label for="title">Email*</label>
                  <input type="text" bind:value={enterprise.email} class="form-control" id="titre" />
                </div>
                <div class="form-group-vertical">
                  <label for="title">Téléphone*</label>
                  <input type="text" bind:value={enterprise.phone} class="form-control" id="titre" />
                </div>
                <div class="form-group-vertical">
                  <label for="title">Adresse*</label>
                  <input type="text" bind:value={enterprise.address} class="form-control" id="titre" />
                </div>
                <div class="form-group-vertical">
                <label for="title">Adresse*</label>
                <MultiSelect
                    id="programme"
                    options={villeOption}
                    placeholder="Choisir ville(s)..."
                    bind:value={villeSelected}
                    bind:selected={villeFromSelectedEntreprise}
                ></MultiSelect>
              </div>
            </form>
        </div>
    </div>
</button>

<style scoped>
    .entreprise {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        width: 90%;
        border-width: 0px;
        border-bottom: 1px solid #00ad9a;
        margin-left: 5.2%;
        background-color: transparent;
    }
    .info {
        display: flex;
        width: 90%;
        font-size: 1.2rem;
        flex-direction: row;
        justify-content: space-around;
    }
    .text {
        width: 20%;
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
