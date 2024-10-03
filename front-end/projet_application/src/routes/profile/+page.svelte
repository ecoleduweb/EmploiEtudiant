<script lang="ts">
    import { goto } from "$app/navigation"
    import { currentUser, isLoggedIn } from "$lib"
    import { onMount } from "svelte"
    import ModifyEnterprise from "../../Components/Enterprise/ModifyEnterprise.svelte"
    import Button from "../../Components/Inputs/Button.svelte";
    import type { User } from "../../Models/User"
    import { PUT } from "../../ts/server"
    import { getCurrentUserEnterprise } from "../../Service/EnterpriseService"

    let lastname: string
    let firstname: string
    let password: string
    let showEnterpriseEditModal = false

    const handleShow = () => {
        showEnterpriseEditModal = true
    }

    const closeModal = () => {
        showEnterpriseEditModal = false
    }

    const ChangePassword = () => {
        PUT<any, any>("/user/updatePassword", {
            email: ($currentUser as User).email,
            password: password
        })

        isLoggedIn.set(false)
        goto("/")
        localStorage.removeItem("token")
    }

    const ChangeUser = (lastName: string, firstName: string) => {
        try {
            const updatedUser = {
                lastname: lastName || $currentUser?.lastName,
                firstname: firstName || $currentUser?.firstName,
                email: ($currentUser as User).email
            };

            PUT<any, any>("/user/user", updatedUser);

            if ($currentUser?.firstName !== firstName && firstName) {
                currentUser.set({ ...$currentUser!, firstName: firstName });
            }
            if ($currentUser?.lastName !== lastName && lastName) {
                currentUser.set({ ...$currentUser!, lastName: lastName });
            }
        } catch {
            alert("Erreur lors de la modification de l'utilisateur");
        }
    };

    let userHaveEnterprise = false

    onMount(async () => {
        try {
            userHaveEnterprise = await getCurrentUserEnterprise() != undefined
        }
        catch (err) {
            userHaveEnterprise = false
        }
    })

</script>

{#if $currentUser}
<div class="container">
    <h1 class="title">
        <span class="text">MON</span>
        <span class="text">PROFIL</span>
    </h1>
    <div class="info">
        <h5 class="infoTitle">Email</h5>
        <p class="text_content">{$currentUser.email}</p>
        <h5 class="infoTitle">Prénom</h5>
        <p class="text_content">{$currentUser.firstName}</p>
        <h5 class="infoTitle">Nom</h5>
        <p class="text_content">{$currentUser.lastName}</p>
        <br>
        
    </div>

    <div class="Modal">
        {#if userHaveEnterprise}
            <div class="divFlex">
                <Button
                    onClick={handleShow}
                    text="Modifier ton entreprise"
                />
            </div>
        {/if}
    </div>
    {#if showEnterpriseEditModal}
        <ModifyEnterprise handleCloseClick={closeModal}>
        </ModifyEnterprise>
    {/if}

    <div class="more-information">
        <h5 class="infoTitleBig">Modifier mon profil:</h5>
        <div class="editInfo">
            <h5 class="infoModify">Prénom:</h5>
            <input type="text_content"
                bind:value={firstname}
                placeholder="Nouveau prénom:"
                class="input"
            />

            <div class="button">
                <Button text="Changer" onClick={() => ChangeUser($currentUser.lastName, firstname)}/>
            </div>
        </div>

        <div class="editInfo">
            <h5 class="infoModify">Nom:</h5>
            <input type="text_content"
                bind:value={lastname}
                placeholder="Nouveau nom:"
                class="input"
            />

            <div class="button">
                <Button text="Changer" onClick={() => ChangeUser(lastname, $currentUser.firstName)}/>
            </div>
        </div>
        <div class="editInfo">
            <h5 class="infoModify">Mot de passe:</h5>
            <input type="text_content"
                bind:value={password}
                placeholder="Nouveau mot de passe"
                class="input"
            />

            <div class="button">
                <Button text="Changer" onClick={() => ChangePassword()}/>
            </div>
        </div>
        <div>
            <h5>Une reconnexion est nécessaire pour appliquer les modifications.</h5>
        </div>
    </div>
</div>
{/if}

<style scoped>
    .title {
        margin-bottom: 1vh;
        margin-top: 3vh;
    }
    .title span:first-child {
        color: white;
        margin: 0;
    }
    .title span:last-child {
        color: #00ad9a;
        margin: 0;
    }
    .text {
        font-size: 2.5vw;
        margin: 0;
    }
    .infoTitle {
        font-size: 1.2vw;
        margin: 0px;
        margin-bottom: 0.5vw;
        margin-right: 1.5vw;
        width: 10vw;
    }
    .infoTitleBig {
        font-size: 1.5vw;
        margin: 0px;
        margin-bottom: 0.5vw;
        margin-right: 1.5vw;
        width: 20vw;
    }
    .input
    {
        width: 10vw;
        margin-right: 1vw;
        margin-bottom: 0.5vw;
        font-size: 1vw;
    }
    .editInfo {
        display: flex;
        justify-content: space-between;
        width: 30vw;
        margin-bottom: 1vh;
    }
    .text_content {
        font-size: 1.1rem;
        margin: 0px;
        margin-bottom: 1vw;
    }
    .container {
        width: 95%;
        display: flex;
        flex-direction: column;
        text-align: left;
        justify-content: space-between;
        border-radius: 4px;
        transition: background-color 0.3s ease;
        margin-left: 4.5vw;
    }

    .editInfo > div, .title, .infoTitle, p, div > h5 {
        color: white;
    }

    .infoModify {
        font-size: 1.2vw;
        margin-bottom: 0.5vw;
        width: 8vw;
    }

    .more-information {
        background-color: #00ad9a;
        width: 33vw;
        padding: 1vw;
        border-radius: 5%;
        border: 2px solid white;
    }

    .divFlex {
        margin-bottom: 1vh;
    }
    

    @media (max-width: 768px) {
        .text {
            font-size: 6vw;
        }
        .infoTitleBig {
            font-size: 5vw;
            width: 100vw;
        }
        .infoTitle {
            font-size: 4vw;
            width: 100%;
        }
        .infoModify
        {
            font-size: 4vw;
            margin-bottom: 1.5vw;
            width: 30vw;
            text-align: center;
        }
        .input {
            font-size: 5vw;
            width: 50vw;
            margin-right: 1vw;
        }
        .editInfo {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center; 
            width: 80vw;
        }
        .text_content {
            font-size: 3.5vw;
            margin-bottom: 3.5vw;
        }
        .more-information {
            width: 80vw;
            padding: 2vw;
        }
    }
</style>
