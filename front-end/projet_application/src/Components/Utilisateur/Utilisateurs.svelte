<script lang="ts">
    import Modal from "../Common/Modal.svelte"
    import type { User } from "../../Models/User"
    import Button from "../Inputs/Button.svelte"
    import { PUT } from "../../ts/server"
    import { writable } from "svelte/store"
    export let user: User
    export let handleUserClick: () => void

    let confirmModal = writable(false)
    let confirmMode: number
    let approbationMessage: string = ""

    let lastname: string
    let firstname: string
    let password: string

    const ChangePassword = async () => {
        await PUT<any, any>("/user/updatePassword", {
            email: user.email,
            password: password
        })

        handleUserClick()
    }

    const ChangeUser = async (lastName: string, firstName: string) => 
    {
        await PUT<any, any>("/user/user", {
            lastname: lastName,
            firstname: firstName,
            email: user.email
        })

        handleUserClick()
    }

    const MakeAdmin = async () => 
    {
        await PUT<any, any>("/user/makeAdmin", {
            email: user.email
        })
    }

    const RemoveUser = async () => 
    {
        await PUT<any, any>("/user/deleteUser", 
        {
            email: user.email
        })
    }

    const DesactivateUser = async () => 
    {
        await PUT<any, any>("/user/desactivateUser", 
        {
            email: user.email
        })
    }

    const ConfirmAccept = async () => 
    {
        confirmModal.set(false)

        switch (confirmMode) 
        {
            case 1: 
            {
                await MakeAdmin()
                break;
            }

            case 2: 
            {
                await RemoveUser()
                break;
            }

            case 3: 
            {
                await DesactivateUser()
                break;
            }
        }

        handleUserClick()
    }

    const ConfirmRefuse = () => 
    {
        confirmModal.set(false)
    }

    const ConfirmBefore = (mode: number) => 
    {
        switch (mode) 
        {
            case 1: 
            {
                approbationMessage = "Voulez-vous vraiment donner/retirer les permissions administrateur à cet utilisateur?"
                break
            }
            case 2: 
            {
                approbationMessage = "Voulez-vous vraiment supprimer cet utilisateur?"
                break
            }
            case 3: 
            {
                approbationMessage = "Voulez-vous vraiment désactiver/activer cet utilisateur?"
                break
            }
        }

        confirmMode = mode
        confirmModal.set(true)
    }

    const ConfirmModalCallback = (result: boolean) => 
    {
        if (result) 
        {
            ConfirmAccept()
        }
        else 
        {
            ConfirmRefuse()
        }
    }

</script>

<Modal handleCloseClick={handleUserClick}>
    {#if !$confirmModal}
    <div class="container">
        <div class="titleContainer">
            <h3 class="title">{user.email}</h3>
        </div>
        <div class="info">
            <h5 class="infoTitle">Email</h5>
            <p class="text">{user.email}</p>
            <h5 class="infoTitle">Prénom</h5>
            <p class="text">{user.firstName}</p>
            <h5 class="infoTitle">Nom</h5>
            <p class="text">{user.lastName}</p>
            <h5 class="infoTitle">Autres informations:</h5>
        </div>

        <div class="editInfo">
            <h5 class="infoTitleModify">Prénom :</h5>
            <input type="text"
                bind:value={firstname}
                placeholder="Nouveau prénom :"
                class="input"
            />

            <div class="button">
                <Button text="Changer" onClick={() => ChangeUser(" ", firstname)}/>
            </div>
        </div>

        <div class="editInfo">
            <h5 class="infoTitleModify">Nom :</h5>
            <input type="text"
                bind:value={lastname}
                placeholder="Nouveau nom :"
                class="input"
            />

            <div class="button">
                <Button text="Changer" onClick={() => ChangeUser(lastname, " ")}/>
            </div>
        </div>
        <div class="editInfo">
            <h5 class="infoTitleModify">Mot de passe :</h5>
            <input type="text"
                bind:value={password}
                placeholder="Nouveau mot de passe :"
                class="input"
            />

            <div class="button">
                <Button text="Changer" onClick={() => ChangePassword()}/>
            </div>
        </div>
        <div>
            <h5 class="info">Une reconnexion est nécessaire pour appliquer les modifications.</h5>
        </div>
        <div class="editInfo userActions">
            <div class="button">
                <Button text="Modifier statut administrateur" onClick={() => ConfirmBefore(1)}/>
            </div>
            <div class="button">
                <Button text="Supprimer utilisateur" onClick={() => ConfirmBefore(2)}/>
            </div>
            <div class="button">
                <Button text="Désactiver utilisateur" onClick={() => ConfirmBefore(3)}/>
            </div>
        </div>
    </div>
    {:else}
        <div class="main-confirm">
            <div class="confirmContainer">
                <div>
                    <h5 class="infoTitle">{approbationMessage}</h5>
                </div>
                <div class="confirmButton">
                    <Button text="Confirmer" onClick={() => ConfirmModalCallback(true)} />
        
                    <Button text="Refuser" onClick={() => ConfirmModalCallback(false)} />
                </div>
            </div>
        </div>
        <style scoped>
            .confirmContainer {
                width: 100%;
                display: flex;
                flex-direction: column;
                text-align: center;
                justify-content: space-between;
                color: white;
                border-radius: 4px;
                transition: background-color 0.3s ease;
            }
        
            .infoTitle {
                color: black;
                font-size: 1.6vw;
            }
            
            .confirmButton {
                display: flex;
                flex-direction: row;
                justify-content: center;
                gap: 1vw;
            }
            .main-confirm {
                flex-direction: column;
                margin: auto;
            }
        </style>
        
    {/if}
</Modal>

<style scoped>

    .container {
        overflow-y: auto;
        max-height: 80vh; 
    }
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
        margin-right: 1.5vw;
        width: 10vw;
    }
    .input 
    {
        margin-right: 1vw;
        margin-bottom: 0.5vw;
    }
    .info {
        color: black;
    }
    .editInfo {
        display: flex;
        color: black;
        margin-bottom: 1vh;
    }
    .text {
        font-size: 1.1rem;
        margin: 0px;
        margin-bottom: 1.75vw;
        color: black;
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
    .userActions 
    {
        flex-direction: row;
        justify-content: space-evenly;
    }
    .infoTitleModify {
        font-size: 1.3rem;
        margin: 0px;
        margin-bottom: 0.5vw;
        margin-right: 1.5vw;
        width: 12vw;
    }

    @media (max-width: 768px) {
        .infoTitle {
            font-size: 3vw;
            width: 100%;
        }
        .input {
            font-size: 2vw;
            height: 6vw;
            margin-bottom: 2vh;
            text-align: center;
        }
        .text {
            font-size: 3vw;
        }
        .editInfo {
            flex-direction: column;
        }

        .infoTitleModify {
            font-size: 3vw;
            width: 100%;
            text-align: center;
        }
        .button {
            display: flex;
            justify-content: center;
            margin-bottom: 1vh;
        }

        .userActions {
            margin-bottom: 10vw;
        }
    }
</style>
