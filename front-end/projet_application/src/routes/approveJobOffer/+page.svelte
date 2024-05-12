<script lang="ts">
    import "../../styles/global.css";
    import Header from "../../Components/Common/Header.svelte";
    import Footer from "../../Components/Common/Footer.svelte";
    import Button from "../../Components/Inputs/Button.svelte";
    import { writable } from "svelte/store";
    import type { jobOffer } from "../../Models/Offre";
    import type { Entreprise } from "../../Models/Entreprise";
    import OfferRow from "../../Components/OffreEmplois/OfferRow.svelte";
    import CreateEditOffre from "../../Components/NewOffre/CreateEditOffre.svelte";
    import { GET } from "../../ts/server";
    import { onMount } from "svelte";
  import EntrepriseRow from "../../Components/Entreprise/EntrepriseRow.svelte";
  import { MultiSelect } from "svelte-multiselect";
  
    let isJobOfferEdit = false;
  
    const handleOffreEmploi = () => {
      isJobOfferEdit = false;
      openModal(0);
    };
  
    const modal = writable(false);
    const selectedEmploiId = writable(0);
    const openModal = (id: number) => {
      modal.set(true);
      selectedEmploiId.set(id);
    };
    const closeModal = () => {
      modal.set(false);
    };
    const handleEmploiClick = (offreId: number) => {
      isJobOfferEdit = true;
      openModal(offreId);
    };
    let offre: jobOffer = {
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
      salary: 0,
      scheduleId: -1,
      employerId: 1,
      isApproved: false,
    };
  
    let error: jobOffer = {
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
      salary: 0,
      scheduleId: 0,
      employerId: 0,
      isApproved: false,
    };
  
    let entreprise: Entreprise = {
      id: 0,
      name: "",
      address: "",
      email: "",
      phone: "",
      cityId: 0,
      isTemporary: false,
    }
  
    let errorEntreprise: Entreprise = {
      id: 0,
      name: "",
      address: "",
      email: "",
      phone: "",
      cityId: 0,
      isTemporary: false,
    }
  
    const getEntreprise = async () => {
      try {
        const responseEntreprise = await GET<any>("/enterprise/getEnterpriseByEmployer?id=" + offre.employerId);
        entreprise = responseEntreprise;
      } catch (error) {
        console.error("Error fetching entreprise:", error);
      }
    };
    onMount(getEntreprise);

    let entrepriseOptions: { label: string; value: number }[] = [];
    const entreprises = writable<Entreprise[]>([]);
    const getEnterprises = async () => {
      try {
        const response = await GET<any>("/enterprise/getEnterprises");
        const data = await response.json();
        entreprises.set(data);
        entrepriseOptions = data.map((e: any) => {
            return { label: e.name, value: e.id };
        });
      } catch (error) {
        console.error("Error fetching job offers:", error);
      }
      console.log(entrepriseOptions);
    };
    onMount(getEnterprises);
  </script>
  
  <Header />
  <main>
    <div class="haut-gauche">
        <h1 class="title">
            <span class="text">ENTREPRISE</span>
        </h1>
    </div>
    <section class="haut">
      <EntrepriseRow entreprise={entreprise} handleModalClick={handleEmploiClick}/>
    </section>
    <MultiSelect
        options={entrepriseOptions}
        placeholder="Select entreprise"
    />
  </main>
  <Footer />
  
  <style scoped>
    main {
      display: flex;
      flex-direction: column;
      justify-content: center;
      width: 100%;
      min-height: 81vh;
    }
    .haut {
      display: flex;
      widows: 85%;
    }
    .haut-gauche {
      display: flex;
      width: 30%;
      justify-content: center;
      align-items: center;
    }
    .divFlex {
      display: flex;
      margin-bottom: 40px;
    }
    .title {
        left: 7.2%;
        margin: 0;
        margin-top: 30px;
    }
    .title span:first-child {
        color: white;
        margin: 0;
    }
    .title span:last-child {
        color: #00ad9a;
        margin: 0;
    }
    .offres {
      display: flex;
      flex-direction: column;
      margin-left: 10%;
    }
    .textOffre {
      font-size: 2.5em;
      margin: 0;
      margin-bottom: 1%;
      color: white;
    }
    .textSections {
      font-size: 1.8em;
      margin: 0;
      margin-top: 15px;
      margin-bottom: 5;
      color: white;
    }
  </style>
  