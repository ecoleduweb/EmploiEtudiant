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

    const ChangeUser = (lastName: string, firstName: string) => 
    {
        try {
            PUT<any, any>("/user/user", {
                lastname: lastName,
                firstname: firstName,
                email: ($currentUser as User).email
            })
            currentUser.set({...$currentUser!, firstName: firstName, lastName: lastName});
        }
        catch {
            //TODO message d'erreur
        }
    }

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
        <h5 class="infoTitle">Autres informations:</h5>
    </div>

    <div class="editInfo">
        <h5 class="infoTitle">Nom:</h5>
        <input type="text_content"
            bind:value={lastname}
            placeholder="Nouveau nom:"
            class="input"
        />

        <div class="button">
            <Button text="Changer" onClick={() => ChangeUser(lastname, " ")}/>
        </div>
    </div>
    <div class="editInfo">
        <h5 class="infoTitle">Prénom:</h5>
        <input type="text_content"
            bind:value={firstname}
            placeholder="Nouveau prénom:"
            class="input"
        />

        <div class="button">
            <Button text="Changer" onClick={() => ChangeUser(" ", firstname)}/>
        </div>
    </div>
    <div class="editInfo">
        <h5 class="infoTitle">Mot de passe:</h5>
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
</div>
{/if}

<style scoped>
    .titleContainer {
        display: flex;
        flex-direction: column;
    }
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
        font-size: 1.3rem;
        margin: 0px;
        margin-bottom: 0.5vw;
        margin-right: 1.5vw;
    }
    .input 
    {
        margin-right: 1vw;
        margin-bottom: 0.5vw;
    }
    .editInfo {
        display: flex;
    }
    .text_content {
        font-size: 1.1rem;
        margin: 0px;
        margin-bottom: 1.75vw;
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
</style>
