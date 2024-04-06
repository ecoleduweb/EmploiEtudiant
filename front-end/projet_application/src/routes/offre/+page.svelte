<script lang="ts">
    import "../../styles/global.css";
    import Button from "../../Components/Inputs/Button.svelte";
    import MultiSelect from 'svelte-multiselect';
    import type { jobOffer } from "../../Models/Offre";
    import { POST } from "../../ts/server";
    import * as yup from "yup";
    import { extractErrors } from "../../ts/utils";
  
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

    let offre: jobOffer = {
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
    urgent: false,
    active: true,
    salary: "",
    scheduleId: -1,
    idProgramme : [],
    };

    let errors: jobOffer = {
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
    urgent: false,
    active: true,
    salary: "",
    scheduleId: 0,
    idProgramme : [],
    };

    let programmeSelected: { label: string; value: number }[] = [];
    let programmeFromSelectedOffer: [] = []; // valeur de l'offre actuel (lorsque l'on editera une offre existante)
    let programmesOption = [
    { label: "Design d'intérieur", value: 1 },
    { label: "Éducation à l'enfance", value: 2 },
    { label: "Gestion et intervention en loisir", value: 3 },
    { label: "Graphisme", value: 4 },
    { label: "Informatique", value: 5 },
    { label: "Inhalothérapie", value: 6 },
    { label: "Pharmacie", value: 7 }
];
  let scheduleSelected: { label: string; value: number }[] = [];
  let scheduleFromExistingOffer: [] = []; // valeur de l'offre actuel (lorsque l'on editera une offre existante)
  let scheduleOption = [
  { label: "Temps plein", value: 1 },
  { label: "Emploi d'été", value: 2 },
  { label: "Temps partiel", value: 3 }
  ];

  const handleSubmit = async () => {

    try {
      offre.scheduleId = (scheduleSelected as any)?.value;
      offre.idProgramme = programmeSelected.map((p) => p.value);
      console.log(offre.idProgramme);

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
        urgent: false,
        active: true,
        salary: "",
        scheduleId: 0,
        idProgramme : [],
      };
      console.log(offre);
      const response = await POST<jobOffer, any>("jobOffer/createJobOffer", offre);
      console.log(response);
    } catch (err) {
      console.log(err);
      errors = extractErrors(err);
    }
  }

  </script>

  <div class="container">
    <form on:submit|preventDefault={handleSubmit} class="form-offre">
      <h1>Créer une nouvelle offre d'emploi</h1>
      <div class="form-group-vertical">
        <label for="title">Titre du poste*</label>
        <input type="text" bind:value={offre.title} class="form-control" id="titre" />
      </div>
      <p class="errors-input">
        {#if errors.title}{errors.title}{/if}
      </p>
      <div class="form-group-vertical">
        <label for="schedule">Type d'emplois*</label>
        <MultiSelect
          id="schedule"
          options={scheduleOption}
          maxSelect={1}
          closeDropdownOnSelect={true}
          placeholder="Choisir période(s)..."
          bind:value={scheduleSelected}
          bind:selected={scheduleFromExistingOffer}
        /> 
      </div>
      <p class="errors-input">
        {#if errors.scheduleId}{errors.scheduleId}{/if}
      </p>
      <div class="form-group-vertical">
        <label for="lieu">Adresse du lieu de travail*</label>
        <input type="text" bind:value={offre.address} class="form-control" id="address" />
      </div>
      <p class="errors-input">
        {#if errors.address}{errors.address}{/if}
      </p>
      <div class="form-group-vertical">
        <label for="dateEntryOffice">Date d'entrée en fonction*</label>
        <input type="date" bind:value={offre.dateEntryOffice} class="form-control" id="dateEntryOffice" />
      </div>
      <p class="errors-input">
        {#if errors.dateEntryOffice}{errors.dateEntryOffice}{/if}
      </p>
      <div class="form-group-vertical">
        <label for="deadlineApply">Date limite pour postuler*</label>
        <input type="date" bind:value={offre.deadlineApply} class="form-control" id="deadlineApply" />
      </div>
      <p class="errors-input">
        {#if errors.deadlineApply}{errors.deadlineApply}{/if}
      </p>
      <div class="form-group-vertical">
        <label for="duree">Programme visée*</label>
        <MultiSelect
          id="programme"
          options={programmesOption}
          placeholder="Choisir programme(s)..."
          bind:value={programmeSelected}
          bind:selected={programmeFromSelectedOffer}
        >
        </MultiSelect>
      </div> 
      <p class="errors-input">
        {#if errors.idProgramme}{errors.idProgramme}{/if}
      </p>
      <div class="form-group-vertical">
        <label for="salaire">Salaire/H (0.00)</label>
        <input type="text" bind:value={offre.salary} class="form-control" id="salaire" />
      </div>
      <p class="errors-input">
          {#if errors.salary}{errors.salary}{/if}
      </p>
      <div class="form-group-vertical">
        <label for="hoursPerWeek">Heure/Semaine*</label>
        <input type="text" bind:value={offre.hoursPerWeek} class="form-control" id="hoursPerWeek" />
      </div>
      <p class="errors-input">
          {#if errors.hoursPerWeek}{errors.hoursPerWeek}{/if}
      </p>
      <div class="form-group-horizontal">
        <label for="internship">Stage ?</label>
        <input type="checkbox" bind:checked={offre.internship} class="form-control" id="internship" />
      </div>
      <p class="errors-input">
        {#if errors.internship}{errors.internship}{/if}
      </p>
      <div class="form-group-horizontal">
        <label for="conciliation">Conciliation</label>
        <input type="checkbox" bind:checked={offre.compliantEmployer} class="form-control" id="compliantEmployer" />
      </div>
      <div class="form-group-horizontal">
        <label for="urgente">Urgente</label>
        <input type="checkbox" bind:checked={offre.urgent} class="form-control" id="urgente" />
      </div>
      <div class="form-group-vertical">
        <label for="offerLink">Lien*</label>
        <input type="text" bind:value={offre.offerLink} class="form-control" id="offerLink" />
      </div>
      <p class="errors-input">
        {#if errors.offerLink}{errors.offerLink}{/if}
      </p>
      <div class="form-group-vertical">
        <label for="courriel-contact">Courriel contact*</label>
        <input type="text" bind:value={offre.email} class="form-control" id="email" />
      </div>
      <p class="errors-input">
        {#if errors.email}{errors.email}{/if}
      </p>
      <div class="form-group-vertical">
        <label for="description">Description du poste*</label>
        <textarea rows="15" cols="50" bind:value={offre.description} class="form-control" id="description" />
      </div>
      <p class="errors-input">
        {#if errors.description}{errors.description}{/if}
      </p>
      <Button submit={true} text="Enregistrer" on:click={() => handleSubmit()} />
    </form>
  </div>

  <style>
    
  .container{
      display: flex;
      flex-direction: column;
      align-items: center;
      background-color: #f5f5f5;

  }
  label {
      display: block;
      margin-bottom: 0.26vw;
  }

  .form-offre {
      display: flex;
      flex-direction: column;
      align-items: center;
      border: 0.3vw solid #ccc;
      background-color: #ffff;
      box-shadow: 0 0.104vw 0.208vw rgba(0, 0, 0, 0.1); /* Add a subtle box shadow */
      border-radius: 0.781vw;
      width: 70%;
      padding: 0 0.78vw 2vh 0;
  }

  .form-group-horizontal {
      display: flex;
      flex-direction: row;
      justify-content: space-between;
      width: 50%;
      margin: 1vh 0;
  }

  .form-group-vertical {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      width: 50%;
      margin: 0.8vw;
  }

  .errors-input {
      color: red;
      font-size: 0.8em;
  }
  </style>