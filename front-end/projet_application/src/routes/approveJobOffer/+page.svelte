<script lang="ts">
    import "../../styles/global.css"
    import { writable } from "svelte/store"
    import type { JobOffer } from "../../Models/Offre"
    import type { Enterprise } from "../../Models/Enterprise"
    import { GET } from "../../ts/server"
    import { onMount } from "svelte"
    import EnterpriseRow from "../../Components/Enterprise/EnterpriseRow.svelte"
    import { MultiSelect } from "svelte-multiselect"

    let isJobOfferEdit = false

    const modal = writable(false)
    const selectedEmploiId = writable(0)
    const openModal = (id: number) => {
        modal.set(true)
        selectedEmploiId.set(id)
    }
    const handleEmploiClick = (offreId: number) => {
        isJobOfferEdit = true
        openModal(offreId)
    }
    let jobOffer: JobOffer = {
        id: 0,
        title: "",
        address: "",
        description: "",
        offerDebut: "",
        dateEntryOffice: "",
        deadlineApply: "",
        email: "",
        hoursPerWeek: 0,
        internship: false,
        offerLink: "",
        offerStatus: 0,
        active: true,
        salary: "",
        employerId: 1,
        isApproved: false,
        approbationMessage: "",
    }

    let error: any = {}

    let enterprise: Enterprise = {
        id: 0,
        name: "",
        address: "",
        email: "",
        phone: "",
        cityId: 0,
        isTemporary: false,
    }

    const getEnterprise = async () => {
        try {
            const responseEnterprise = await GET<any>(
                `/enterprise/employer/${jobOffer.employerId}`
            )
            enterprise = responseEnterprise
        } catch (error) {
            console.error("Error fetching enterprise:", error)
        }
    }
    onMount(getEnterprise)

    let enterpriseOptions: { label: string; value: number }[] = []
    const enterprises = writable<Enterprise[]>([])
    const getEnterprises = async () => {
        try {
            const response = await GET<any>("/enterprise/all")
            const data = await response.json()
            enterprises.set(data)
            enterpriseOptions = data.map((e: any) => {
                return { label: e.name, value: e.id }
            })
        } catch (error) {
            console.error("Error fetching job offers:", error)
        }
        console.log(enterpriseOptions)
    }
    onMount(getEnterprises)
</script>

<main>
    <div class="haut-gauche">
        <h1 class="title">
            <span class="text">ENTREPRISE</span>
        </h1>
    </div>
    <section class="haut">
        <EnterpriseRow enterprise={enterprise} handleModalClick={handleEmploiClick} />
    </section>
    <MultiSelect options={enterpriseOptions} placeholder="Select entreprise" />
</main>

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
