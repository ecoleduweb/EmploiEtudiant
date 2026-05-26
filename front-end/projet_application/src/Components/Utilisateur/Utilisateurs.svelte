<script lang="ts">
    import Modal from "../Common/Modal.svelte"
    import type { User } from "../../Models/User"
    import Button from "../Inputs/Button.svelte"
    import { DELETE, PUT } from "../../ts/server"

    export let user: User
    export let onCloseModal: () => void

    let showConfirmModal = false
    let confirmMode: number = 0
    let approbationMessage: string = ""

    let lastname: string = ""
    let firstname: string = ""
    let password: string = ""

    const changePassword = async (user: User) => {
        await PUT<any, any>(`/auth/updatePassword/${user.id}`, user)
        onCloseModal()
    }

    const updateUser = async (user: User) => {
        await PUT<User, User>(`/user/${user.id}`, user)
        onCloseModal()
    }

    const toggleAdmin = async (user: User) => {
        await PUT<any, User>(`/user/toggleAdmin/${user.id}`, {})
    }

    const deleteUser = async (user: User) => {
        await DELETE(`/user/${user.id}`)
    }

    const desactivateUser = async (user: User) => {
        await PUT<any, User>(`/user/toggleActive/${user.id}`, {})
    }

    const confirmAccept = async (user: User) => {
        showConfirmModal = false

        switch (confirmMode) {
            case 1: {
                await toggleAdmin(user)
                break
            }
            case 2: {
                await deleteUser(user)
                break
            }
            case 3: {
                await desactivateUser(user)
                break
            }
        }
        onCloseModal()
    }

    const confirmRefuse = () => {
        showConfirmModal = false
    }

    const handleConfirmToProceed = (mode: number) => {
        switch (mode) {
            case 1: {
                approbationMessage = `Voulez-vous vraiment {user.isModerator ? 'retirer' : 'accorder'} les permissions administrateur à cet utilisateur?`
                break
            }
            case 2: {
                approbationMessage = `Voulez-vous vraiment supprimer ${user.firstName} ${user.lastName}?`
                break
            }
            case 3: {
                approbationMessage = `Voulez-vous vraiment ${user.active ? "désactiver" : "activer"} ${user.firstName} ${user.lastName}?`
                break
            }
        }

        confirmMode = mode
        showConfirmModal = true
    }

    const handleConfirm = (result: boolean, user: User) => {
        if (result) {
            confirmAccept(user)
        } else {
            confirmRefuse()
        }
    }
</script>

<Modal handleCloseClick={onCloseModal}>
    {#if !showConfirmModal}
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
                <input
                    type="text"
                    bind:value={firstname}
                    placeholder="Nouveau prénom :"
                    class="input"
                />

                <div class="button">
                    <Button
                        text="Changer"
                        onClick={() =>
                            updateUser({ ...user, firstName: firstname })}
                    />
                </div>
            </div>

            <div class="editInfo">
                <h5 class="infoTitleModify">Nom :</h5>
                <input
                    type="text"
                    bind:value={lastname}
                    placeholder="Nouveau nom :"
                    class="input"
                />

                <div class="button">
                    <Button
                        text="Changer"
                        onClick={() =>
                            updateUser({ ...user, lastName: lastname })}
                    />
                </div>
            </div>

            <div class="editInfo">
                <h5 class="infoTitleModify">Mot de passe :</h5>
                <input
                    type="text"
                    bind:value={password}
                    placeholder="Nouveau mot de passe :"
                    class="input"
                />

                <div class="button">
                    <Button
                        text="Changer"
                        onClick={() =>
                            changePassword({ ...user, password: password })}
                    />
                </div>
            </div>

            <div>
                <h5 class="info">
                    Une reconnexion est nécessaire pour appliquer les
                    modifications.
                </h5>
            </div>

            <div class="editInfo userActions">
                <div class="button">
                    <Button
                        text={user.isModerator
                            ? "Retirer les privilèges d'administrateur"
                            : "Accorder les privilèges d'administrateur"}
                        onClick={() => handleConfirmToProceed(1)}
                    />
                </div>
                <div class="button">
                    <Button
                        text="Supprimer utilisateur"
                        onClick={() => handleConfirmToProceed(2)}
                    />
                </div>
                <div class="button">
                    <Button
                        text={user.active
                            ? "Désactiver l'utilisateur"
                            : "Activer l'utilisateur"}
                        onClick={() => handleConfirmToProceed(3)}
                    />
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
                    <Button
                        text="Confirmer"
                        onClick={() => handleConfirm(true, user)}
                    />
                    <Button
                        text="Refuser"
                        onClick={() => handleConfirm(false, user)}
                    />
                </div>
            </div>
        </div>
    {/if}
</Modal>

<style>
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

    .container {
        overflow-y: auto;
        max-height: 80vh;
        width: 95%;
        display: flex;
        flex-direction: column;
        text-align: left;
        justify-content: space-between;
        color: white;
        border-radius: 4px;
        transition: background-color 0.3s ease;
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

    .infoTitle {
        font-size: 1.3rem;
        margin: 0px;
        margin-bottom: 0.5vw;
        margin-right: 1.5vw;
        color: black;
    }

    .input {
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

    .userActions {
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
