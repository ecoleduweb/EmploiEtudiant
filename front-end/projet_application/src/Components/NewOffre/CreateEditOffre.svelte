<script lang="ts">
  import "../../styles/global.css";
  import Modal from "../Common/Modal.svelte";
  import Button from "../Inputs/Button.svelte";
  import MultiSelect from "svelte-multiselect";
  import type { jobOffer } from "../../Models/Offre";
  import type { Entreprise } from "../../Models/Entreprise";
  import { writable } from "svelte/store";
  import { GET, POST } from "../../ts/server";
  import * as yup from "yup";
  import { extractErrors } from "../../ts/utils";
  import { onMount } from "svelte";
  import { jwtDecode } from "jwt-decode";
  import { onNavigate } from "$app/navigation";
  import { goto } from '$app/navigation';
  import type Token from "../../Models/Token";
  export let handleEmploiClick: () => void;
  export let isJobOfferEdit: boolean;

  const schema = yup.object().shape({
    title: yup.string().required("Le titre du poste est requis"),
    address: yup.string().required("L'adresse du lieu de travail est requise"),
    description: yup.string().required("La description de l'offre est requise"),
    dateEntryOffice: yup
      .string()
      .required("La date d'entrée en fonction est requise")
      .test("is-date", "Veuillez choisir une date valide !", (value) => {
        return !isNaN(Date.parse(value));
      }),
    deadlineApply: yup
      .string()
      .required("La date limite de l'offre est requise")
      .test("is-date", "Veuillez choisir une date valide !", (value) => {
        return !isNaN(Date.parse(value));
      }),
    email: yup
      .string()
      .matches(
        /\.[a-z]+$/,
        "Le courriel doit être de format valide : courriel@domaine.ca"
      )
      .email("Le courriel n'est pas valide")
      .required("Le courriel est requis"),
    hoursPerWeek: yup
      .string()
      .required("Le nombre d'heure par semaine est requis")
      .test(
        "is-number",
        "Veuillez entrer un nombre d'heure valide !",
        (value) => {
          return !isNaN(Number(value)) && Number(value) > 0;
        }
      ),
    scheduleId: yup
      .number()
      .required("Le type d'emploi est requis")
      .min(0, "Le type d'emploi est requis"),
    idProgramme: yup.array().min(1, "Le programme visé est requis"),
    acceptCondition: yup
      .boolean()
      .oneOf([true], "Vous devez accepter les conditions"),
  });

  export let offre: jobOffer = {
    id: 0,
    title: "",
    address: "",
    description: "",
    offerDebut: new Date().toISOString().split("T")[0],
    dateEntryOffice: new Date().toISOString().split("T")[0],
    deadlineApply: new Date().toISOString().split("T")[0],
    email: "",
    hoursPerWeek: 0,
    compliantEmployer: false,
    internship: false,
    offerLink: "https://",
    offerStatus: 0,
    active: true,
    salary: "",
    scheduleId: -1,
    employerId: 1, // HARDCODER
    isApproved: false,
  };

  let errors: jobOffer = {
    id: 0,
    title: "",
    address: "",
    description: "",
    offerDebut: "",
    dateEntryOffice: "",
    deadlineApply: "",
    email: "",
    hoursPerWeek: 0,
    compliantEmployer: false,
    internship: false,
    offerLink: "",
    offerStatus: 0,
    active: true,
    salary: "",
    scheduleId: 0,
    employerId: 0, // HARDCODER
    isApproved: false,
  };

  export let entreprise: Entreprise = {
    id: 0,
    name: "",
    address: "",
    email: "",
    phone: "",
    cityId: 0,
    isTemporary: false,
  };

  let errorsEntreprise: Entreprise = {
    id: 0,
    name: "",
    address: "",
    email: "",
    phone: "",
    cityId: 0,
    isTemporary: false,
  };

  let isEnterpriseSelected: boolean = false;

  let villeSelected: { label: string; value: number }[] = [];
  let villeFromSelectedEntreprise: [] = [];
  let villesOption: { label: string; value: number }[] = [];
  const getVilles = async () => {
    const response = await GET<any>("/city/allCities");
    villesOption = response.map((v: any) => {
      return { label: v.city, value: v.id };
    });
  };

    const getEmployerByUserId = async () => {
          const response = await GET<any>("/employer/getEmployerByUserId");
           if (response !== undefined) {
            getEnterprise(response.entrepriseId);
           }
    };

    onMount(async () => {
      await getVilles();
      const token = localStorage.getItem("token");
      if (token) {
        var decoded = jwtDecode<Token>(token);
        isModerator = decoded.isModerator;
    }
      if (isModerator === true) {
        await getAllEnterprise();
      }
      else 
      {
        await getEmployerByUserId();
      }
    });

    //-------------SECTION ADMIN-------------------------------------
    let isModerator: boolean = false;
    let enterpriseSelected: { label: string; value: number }[] = [];
    let enterpriseFromSelectedEnterprise: [] = []; // valeur de l'offre actuel (lorsque l'on editera une offre existante)
    let enterpriseOption: { label: string; value: number }[] = [];
    const getAllEnterprise = async () => {
      const response = await GET<any>("/enterprise/getEnterprises");
        enterpriseOption = response.map((e: Entreprise) => {
        return { label: e.name, value: e.id };
      });
    };

    const getEnterprise = async (enterpriseId: number) => {
    const response = await GET<any>(`/enterprise/getEnterprise?id=${enterpriseId}`);
      entreprise = response;
      const city = villesOption.find(ville => ville.value === response.cityId);
      if (city) {
          villeSelected = [city];
      }
      isEnterpriseSelected = true;
    
    };

  //--------------------------------------------------

  let programmeSelected: { label: string; value: number }[] = [];
  let programmeFromSelectedOffer: [] = []; // valeur de l'offre actuel (lorsque l'on editera une offre existante)
  let programmesOption = [
    { label: "Design d'intérieur", value: 1 },
    { label: "Éducation à l'enfance", value: 2 },
    { label: "Gestion et intervention en loisir", value: 3 },
    { label: "Graphisme", value: 4 },
    { label: "Informatique", value: 5 },
    { label: "Inhalothérapie", value: 6 },
    { label: "Pharmacie", value: 7 },
    { label: "Soins infirmiers", value: 8 },
    { label: "Arts visuels", value: 9 },
    { label: "Sciences de la nature", value: 10 },
    { label: "Sciences humaines", value: 11 },
  ];
  let scheduleSelected: { label: string; value: number }[] = [];
  let scheduleFromExistingOffer: [] = []; // valeur de l'offre actuel (lorsque l'on editera une offre existante)
  let scheduleOption = [
    { label: "Temps plein", value: 1 },
    { label: "Emploi d'été", value: 2 },
    { label: "Temps partiel", value: 3 },
  ];

  //--------------------------------------------------

  let errorsProgramme: string = ""; // Define a variable to hold the error message for selected program
  let errorsAcceptCondition: string = ""; // Define a variable to hold the error message for accepting condition
  let acceptCondition = false;

  const handleSubmit = async () => {
    if (!acceptCondition) {
      errorsAcceptCondition = "Vous devez accepter les conditions";
      return;
    }
    if (isJobOfferEdit) {
      await updateJobOffer();
    } else {
      await createJobOffer();
    }
  };

  async function createJobOffer() {
      try {
          offre.scheduleId = (scheduleSelected as any)?.value;
          let programmeName = programmeSelected.map((p) => p.label);
          await schema.validate(offre, { abortEarly: false });
          errors = {
              id: 0,
              title: "",
              address: "",
              description: "",
              offerDebut: "",
              dateEntryOffice: "",
              deadlineApply: "",
              email: "",
              hoursPerWeek: 0,
              compliantEmployer: false,
              internship: false,
              offerLink: "",
              offerStatus: 0,
              active: false,
              salary: "",
              scheduleId: 0,
              employerId: 0,
              isApproved: false,
          };
          entreprise.cityId = villeSelected[0].value;
          console.log("ENTEPRISE :" + entreprise.cityId);
          const requestData = {
              jobOffer: {
                  ...offre,
              },
              enterprise: {
                  ...entreprise,
              },
              studyPrograms: programmeName
          };
          const response = await POST<any, any>("/jobOffer/createJobOffer", requestData);
          if (response.message === "Job offer created successfully") {
            handleEmploiClick();
          }
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
  

  async function updateJobOffer() {
    try {
      offre.scheduleId = (scheduleSelected as any)?.value;
      let programmeName = programmeSelected.map((p) => p.label);
      await schema.validate(offre, { abortEarly: false });
      errors = {
        id: 0,
        title: "",
        address: "",
        description: "",
        offerDebut: "",
        dateEntryOffice: "",
        deadlineApply: "",
        email: "",
        hoursPerWeek: 0,
        compliantEmployer: false,
        internship: false,
        offerLink: "",
        offerStatus: 0,
        active: false,
        salary: "",
        scheduleId: 0,
        employerId: 0,
        isApproved: false,
      };
      errorsEntreprise = {
        id: 0,
        name: "",
        address: "",
        email: "",
        phone: "",
        cityId: 0,
        isTemporary: false,
      };
      entreprise.cityId = villeSelected[0].value;
      console.log("ENTEPRISE :" + entreprise.cityId);
      const requestData = {
        entreprise: {
          ...entreprise,
        },
        jobOffer: {
          ...offre,
        },
        studyPrograms: programmeName,
      };
      const response = await POST<any, any>(
        "/jobOffer/updateJobOffer",
        requestData
      );
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

  let maxDateString: any;
  $: {
    let offerDebut = new Date(offre.offerDebut);
    let maxDate = new Date(offerDebut.setDate(offerDebut.getDate() + 15 * 7));
    maxDateString = maxDate.toISOString().split("T")[0]; // format as yyyy-mm-dd
  }

  let todayMin = new Date();
  let minDateString = todayMin.toISOString().split("T")[0]; // format as yyyy-mm-dd


</script>

<Modal handleModalClick={handleEmploiClick}>
  <form on:submit|preventDefault={handleSubmit} class="form-offre">
    {#if isModerator === true}
      {#if isJobOfferEdit === true}
        <!-- rien -->
      {:else}
        <h1>Sélectionner une entreprise existante</h1>
        <div class="form-group-horizontal">
          <MultiSelect
            id="entreprise"
            options={enterpriseOption}
            closeDropdownOnSelect={true}
            maxSelect={1}
            placeholder="Choisir une entreprise..."
            bind:value={enterpriseSelected}
            bind:selected={enterpriseFromSelectedEnterprise}
            on:add={(event) => getEnterprise(event.detail.option.value)}
          />
          <Button
            submit={false}
            text="Créer une entreprise"
            onClick={() => goto("/entreprise")}
        />
        </div>
      {/if}
    {/if}
    
    {#if isJobOfferEdit === true}
      <h1>Modification d'une entreprise</h1>
    {:else}
      <h1>Création d'une nouvelle entreprise</h1>
    {/if}
    <div class="form-group-vertical">
      <label for="title">Nom*</label>
      <input
        type="text"
        bind:value={entreprise.name}
        class="form-control"
        id="titre"
        readonly={isEnterpriseSelected}
      />
    </div>
    <p class="errors-input">
      {#if errorsEntreprise.name}{errorsEntreprise.name}{/if}
    </p>
    <div class="form-group-vertical">
      <label for="schedule">Adresse*</label>
      <input
        type="text"
        bind:value={entreprise.address}
        class="form-control"
        id="address"
        readonly={isEnterpriseSelected}
      />
    </div>
    <p class="errors-input">
      {#if errorsEntreprise.address}{errorsEntreprise.address}{/if}
    </p>
    <div class="form-group-vertical">
      <label for="lieu">Courriel*</label>
      <input
        type="text"
        bind:value={entreprise.email}
        class="form-control"
        id="email"
        readonly={isEnterpriseSelected}
      />
    </div>
    <p class="errors-input">
      {#if errorsEntreprise.email}{errorsEntreprise.email}{/if}
    </p>
    <div class="form-group-vertical">
      <label for="lieu">Téléphone*</label>
      <input
        type="text"
        bind:value={entreprise.phone}
        class="form-control"
        id="phone"
        readonly={isEnterpriseSelected}
      />
    </div>
    <p class="errors-input">
      {#if errorsEntreprise.phone}{errorsEntreprise.phone}{/if}
    </p>
    <div class="form-group-vertical">
      <label for="lieu">Ville*</label>
      {#if villesOption.length === 0}
        <p>Chargement des villes...</p>
      {:else}
      <MultiSelect
        id="ville"
        options={villesOption}
        closeDropdownOnSelect={true}
        placeholder="Choisir ville..."
        bind:value={villeSelected}
        bind:selected={villeFromSelectedEntreprise}
        disabled={isEnterpriseSelected}
      />
      {/if}
    </div>
    {#if isJobOfferEdit === true}
      <h1>Modification d'une offre d'emploi</h1>
    {:else}
      <h1>Création d'une nouvelle offre d'emploi</h1>
    {/if}
    <div class="form-group-vertical">
      <label for="title">Titre du poste*</label>
      <input
        type="text"
        bind:value={offre.title}
        class="form-control"
        id="titre"
      />
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
      <input
        type="text"
        bind:value={offre.address}
        class="form-control"
        id="address"
      />
    </div>
    <p class="errors-input">
      {#if errors.address}{errors.address}{/if}
    </p>
    <div class="form-group-horizontal-date">
      <div class="form-group-vertical">
        <label for="offerDebut">Date de publication de l'offre</label>
        <input
          type="date"
          bind:value={offre.offerDebut}
          class="form-control"
          id="offerDebut"
          min={minDateString}
        />
      </div>
      <p class="errors-input">
        {#if errors.offerDebut}{errors.offerDebut}{/if}
      </p>
      <div class="form-group-vertical">
        <label for="dateEntryOffice"
          >Date d'entrée en fonction de l'emploi*</label
        >
        <input
          type="date"
          bind:value={offre.dateEntryOffice}
          class="form-control"
          id="dateEntryOffice"
          min={minDateString}
        />
      </div>
      <p class="errors-input">
        {#if errors.dateEntryOffice}{errors.dateEntryOffice}{/if}
      </p>
      <div class="form-group-vertical">
        <label for="deadlineApply">Date limite pour postuler*</label>
        <input
          type="date"
          bind:value={offre.deadlineApply}
          class="form-control"
          id="deadlineApply"
          max={maxDateString}
          min={offre.offerDebut}
        />
      </div>
      <p class="errors-input">
        {#if errors.deadlineApply}{errors.deadlineApply}{/if}
      </p>
    </div>
    <div class="form-group-vertical">
      <label for="duree">Programme visée*</label>
      <MultiSelect
        id="programme"
        options={programmesOption}
        closeDropdownOnSelect={true}
        placeholder="Choisir programme(s)..."
        bind:value={programmeSelected}
        bind:selected={programmeFromSelectedOffer}
      ></MultiSelect>
    </div>
    <p class="errors-input">
      {#if errorsProgramme}{errorsProgramme}{/if}
    </p>
    <div class="form-group-vertical">
      <label for="salaire">Salaire/H</label>
      <input
        type="text"
        bind:value={offre.salary}
        class="form-control"
        id="salaire"
      />
    </div>
    <p class="errors-input">
      {#if errors.salary}{errors.salary}{/if}
    </p>
    <div class="form-group-vertical">
      <label for="hoursPerWeek">Heure/Semaine*</label>
      <input
        type="text"
        bind:value={offre.hoursPerWeek}
        class="form-control"
        id="hoursPerWeek"
      />
    </div>
    <p class="errors-input">
      {#if errors.hoursPerWeek}{errors.hoursPerWeek}{/if}
    </p>
    <div class="form-group-horizontal">
      <label for="internship">Stage ?</label>
      <input
        type="checkbox"
        bind:checked={offre.internship}
        class="form-control"
        id="internship"
      />
    </div>
    <p class="errors-input">
      {#if errors.internship}{errors.internship}{/if}
    </p>
    <div class="form-group-horizontal">
      <label for="conciliation">Conciliation</label>
      <input
        type="checkbox"
        bind:checked={offre.compliantEmployer}
        class="form-control"
        id="compliantEmployer"
      />
    </div>
    <div class="form-group-vertical">
      <label for="offerLink">Adresse URL vers l'offre d'emploi détaillé</label>
      <input
        type="text"
        bind:value={offre.offerLink}
        class="form-control"
        id="offerLink"
      />
    </div>
    <p class="errors-input">
      {#if errors.offerLink}{errors.offerLink}{/if}
    </p>
    <div class="form-group-vertical">
      <label for="courriel-contact">Courriel contact*</label>
      <input
        type="text"
        bind:value={offre.email}
        class="form-control"
        id="email"
      />
    </div>
    <p class="errors-input">
      {#if errors.email}{errors.email}{/if}
    </p>
    <div class="form-group-vertical">
      <label for="description">Description du poste*</label>
      <textarea
        rows="15"
        cols="50"
        bind:value={offre.description}
        class="form-control"
        id="description"
      />
    </div>
    <p class="errors-input">
      {#if errors.description}{errors.description}{/if}
    </p>
    <div class="accept-Condition">
      <input
        type="checkbox"
        bind:checked={acceptCondition}
        class="form-control-acceptCondition"
        id="acceptCondition"
      />
      <label for="acceptCondition">J'acceptes les condtions </label>
    </div>
    <p class="errors-input">
      {#if errorsAcceptCondition}{errorsAcceptCondition}{/if}
    </p>
    <Button
      submit={true}
      text="Envoyer"
      on:click={() => handleSubmit()}
      onClick={() => ""}
    />
  </form>
</Modal>

<style>
  label {
    display: block;
    margin-bottom: 0.26vw;
  }

  .form-offre {
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
    border: 0.3vw solid #ccc;
    background-color: #ffff;
    box-shadow: 0 0.104vw 0.208vw rgba(0, 0, 0, 0.1);
    border-radius: 0.781vw;
    padding: 0 0.78vw 2vh 0;
  }

  .form-group-horizontal {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 80%;
    margin: 1vh 0;
  }

  .form-group-vertical {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    width: 80%;
    margin: 0.8vw;
  }
  .form-group-horizontal-date {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    width: 83.25%;
  }

  .errors-input {
    color: red;
    font-size: 0.8em;
  }
  .accept-Condition {
    display: flex;
    flex-direction: row;
    width: 80%;
    margin: 0.8vw;
  }
  .form-control-acceptCondition {
    margin-right: 0.8vw;
    margin-bottom: 0.5vw;
  }
</style>
