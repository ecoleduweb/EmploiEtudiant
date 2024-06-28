<script lang="ts">
    import { goto, invalidateAll } from "$app/navigation"
    import { currentUser, isLoggedIn } from "$lib"
    import Button from "../../Components/Inputs/Button.svelte";
    import type { User } from "../../Models/User"
    import { PUT } from "../../ts/server"

    let lastname: string
    let firstname: string
    let password: string

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
        PUT<any, any>("/user/updateUser", {
            lastname: lastName,
            firstname: firstName,
            email: ($currentUser as User).email
        })

        //Bug, le lastname et le firstname ne refresh pas, car le client le prend du token, mais maintenant le lastname/firstname à changer, donc il faudra refetch
    }

</script>

{#if $currentUser}
<div class="container">
    <div class="titleContainer">
        <h3 class="title">Utilisateur</h3>
    </div>
    <div class="info">
        <h5 class="infoTitle">Email</h5>
        <p class="text">{$currentUser.email}</p>
        <h5 class="infoTitle">Prenom</h5>
        <p class="text">{$currentUser.firstName}</p>
        <h5 class="infoTitle">Nom</h5>
        <p class="text">{$currentUser.lastName}</p>
        <br>
        <h5 class="infoTitle">Autre informations:</h5>
    </div>

    <div class="editInfo">
        <h5 class="infoTitle">Nom:</h5>
        <input type="text"
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
        <input type="text"
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
        <input type="text"
            bind:value={password}
            placeholder="Nouveau mot de passe"
            class="input"
        />

        <div class="button">
            <Button text="Changer" onClick={() => ChangePassword()}/>
        </div>
    </div>
</div>
{/if}

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
    .text {
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
        color: white;
        border-radius: 4px;
        transition: background-color 0.3s ease;
        margin-top: 2%;
        margin-left: 2%;
    }
</style>
