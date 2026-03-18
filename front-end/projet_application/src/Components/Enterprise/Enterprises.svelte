<script lang="ts">
    import Modal from "../Common/Modal.svelte"
    import type { Enterprise } from "../../Models/Enterprise"
    import { GET } from "../../ts/server"
    import { onMount } from "svelte"
    import type { City } from "../../Models/City"
    import { assignUserToEnterprise } from "../../Service/EnterpriseService"
    import type { User } from "../../Models/User"
    interface Props {
        enterprise: Enterprise;
        handleEnterpriseClick: () => void;
    }

    let { enterprise, handleEnterpriseClick }: Props = $props();
    let Users: any[] = $state([]);
    let selectedUserId: number | undefined = $state();
    let ville: City | undefined = $state();
    let nomVille: string  | undefined = $state();

    const getCity = async (id: number) => {
        try {
            ville = await GET<any>(`/city/${id}`)
            nomVille = ville?.city
        } catch (error) {
            console.error("Error fetching city:", error)
        }
    }
const getAllUsers = async () => {
    try {
        const data = await GET<any>("/user/all");
        
        if (data && data.users) {
            Users = data.users.map((u: any) => {
                const fullName = `${u.firstName} ${u.lastName}`.trim();
                return { 
                    label: fullName.length > 0 ? fullName : u.email, 
                    value: u.id 
                };
            });
        }
    } catch (err) {
        console.error("Erreur utilisateurs:", err);
    }
}

const handleAssign = async () => {

    if (selectedUserId !== undefined && enterprise?.id) {
        try {
            const response = await assignUserToEnterprise(
                selectedUserId, 
                enterprise.id
            );
        } catch (error) {
            console.error("Erreur:", error);
        }
    } else {
        alert("Veuillez sélectionner un utilisateur.");
    }
};
    onMount(() => {
        getCity(enterprise.cityId);
        getAllUsers();
    })
</script>

<Modal handleCloseClick={handleEnterpriseClick}>
    <div class="container">
        <div class="titleContainer">
            <h3 class="title">{enterprise.name}</h3>
        </div>
        <div class="info">
            <h5 class="infoTitle">Adresse courriel</h5>
            <p class="text">{enterprise.email}</p>
            <h5 class="infoTitle">Numéro de téléphone</h5>
            <p class="text">{enterprise.phone}</p>
            <h5 class="infoTitle">Adresse de l'enterprise</h5>
            <p class="text">{enterprise.address}</p>
            <h5 class="infoTitle">Ville</h5>
            <p class="text">{nomVille}</p>
            
            <hr style="border: 0.5px solid #00ad9a; margin: 1vw 0;" />
            
            <h5 class="infoTitle">Assigner un administrateur</h5>
           <div class="assign-action">
                <select bind:value={selectedUserId} class="form-control" style="margin-bottom: 10px;">
                    <option value={undefined}>Choisir un utilisateur...</option>
                    {#each Users as user}
                        <option value={user.value}>{user.label}</option>
                    {/each}
                </select>

                <button 
                    type="button"
                    class="btn-assign"
                    onclick={handleAssign}
                    style="background-color: #00ad9a; color: white; border: none; padding: 10px; border-radius: 4px; cursor: pointer; width: 100%;"
                >
                    Confirmer l'assignation
                </button>
            </div>
        </div>
    </div>
</Modal>

<style scoped>
    .titleContainer {
        display: flex;
        flex-direction: column;
    }
    .title {
        font-size: 2.5rem;
        color: #00ad9a;
        margin: 0px;
        margin-bottom: 1.5vw;
    }
    /* .subtitle {
        font-size: 1.5rem;
        margin: 0px;
        margin-bottom: 2.25vw;
        color: black;
    } */
    .infoTitle {
        font-size: 1.3rem;
        margin: 0px;
        margin-bottom: 0.5vw;
    }
    .info {
        color: black;
    }
    .text {
        font-size: 1.1rem;
        margin: 0px;
        margin-bottom: 1.75vw;
        color: black;
    }
    .btn-assign:hover {
        background-color: #008a7b !important; /* Un vert un peu plus foncé */
        transform: scale(1.02);
        transition: all 0.2s ease;
    }
    
    .btn-assign:active {
        transform: scale(0.98);
    }
    .container {
        width: 95%;
        display: flex;
        flex-direction: column;
        text-align: left;
        justify-content: space-between;
        color: white;
        border-radius: 4px;
        transition: background-color 0.3s ease;
    }
</style>
