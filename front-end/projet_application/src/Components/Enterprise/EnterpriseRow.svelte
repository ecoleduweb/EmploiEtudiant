<script lang="ts">
    import type { Enterprise } from "../../Models/Enterprise"
    import type { City } from "../../Models/City"
    import { GET } from "../../ts/server"
    import { onMount } from "svelte"
    import { formatPhoneNumber } from "../../ts/utils"
    interface Props {
        enterprise: Enterprise;
        handleModalClick: (id: number) => void;
    }
/*oici l'explication du bug en 5 lignes :

La règle : En HTML, un <button> ne peut jamais contenir un autre bouton ou un <select> ; c'est une structure interdite.

Le conflit : Ta modale étant techniquement dans le bouton de la ligne, elle y injecte tes nouveaux éléments interactifs.

Le crash : Svelte 5 détecte cette structure invalide lors du rendu et bloque immédiatement l'exécution du JavaScript (erreur d'hydratation).

Le blocage : Comme le code plante, ta variable loaded ne devient jamais true, laissant le logo de chargement tourner à l'infini.

La solution : Utiliser une <div> cliquable pour la ligne permet d'accepter tous les éléments enfants */
    let { enterprise, handleModalClick }: Props = $props();
    let ville: City
    let nomVille: string | undefined = $state()
    let formattedPhone: string | undefined = $state()
    let Users: any[] = $state([]);
    const getCity = async (id: number) => {
        try {
            ville = await GET<any>(`/city/${id}`)
            nomVille = ville.city
        } catch (error) {
            console.error("Error fetching city:", error)
        }
    }

    onMount(async () => {
 formattedPhone = formatPhoneNumber(enterprise.phone);
    
    // On vérifie que l'ID existe avant d'appeler getCity
    if (enterprise.cityId !== undefined) {
        await getCity(enterprise.cityId);
    }
           if (enterprise.id !== undefined) {
        await getAllUsersAssignedToEntreprise(enterprise.id);
    } 
    });
    const getAllUsersAssignedToEntreprise = async (enterpriseId: number) => {
        try {
            const data = await GET<any>(`/enterprise/${enterpriseId}/users`);
            if (data) {
                Users = data.map((u: any) => {
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
</script>



<div 
    class="enterprise-container" 
    onclick={() => handleModalClick(enterprise.id!)} 
    onkeydown={(e) => e.key === 'Enter' && handleModalClick(enterprise.id!)}
    role="button"
    tabindex="0"
    style="cursor: pointer;"
>
    <div class="emploi">
        <div class="info">
            <p class="textTitre">{enterprise.name}</p>
            <p class="text">{enterprise.email}</p>
            <p class="text">{formattedPhone}</p>
            <p class="text">{enterprise.address}</p>
            <p class="text">{nomVille}</p>
<select
    class="form-control"
    style="margin-bottom: 10px;"
    onclick={(e) => e.stopPropagation()}
>
    <option value={undefined}>Utilisateurs non assignés</option>
    {#each Users as user}
        <option value={user.value}>{user.label}</option>
    {/each}
</select>
        </div>
        <div class="info-mobile">
            <p class="textTitre">{enterprise.name}</p>
            <p class="text">{enterprise.email}</p>
        </div>
        <img class="image" src="searchBar.svg" alt="ajouter" />
    </div>
</div>

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
    }
    .info {
        display: flex;
        width: 90%;
        font-size: 1.2rem;
        flex-direction: row;
        justify-content: space-around;
        align-items: center;
    }
    .text {
        width: 20%;
    }
    .textTitre {
        width: 20%;
        font-weight: bold;
        font-size: 1.8rem;
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

    .info-mobile {
        display: none;
    }

    @media (max-width: 768px) {
        .info {
            display: none;
        }
        .info-mobile {
            display: flex;
            flex-direction: row;
            justify-content: space-between;
            align-items: center;
            width: 60%;
        }

        .text {
            font-size: 3.5vw;
        }
    }
</style>
