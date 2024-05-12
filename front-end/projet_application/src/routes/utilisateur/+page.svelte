<script lang="ts">
  import "../../styles/global.css";
  import Header from "../../Components/Common/Header.svelte";
  import Footer from "../../Components/Common/Footer.svelte";
  import { onMount } from "svelte";
  import { get, writable } from "svelte/store";
  import { GET } from "../../ts/server";
  import type { Users } from "../../Models/User";
  import UserRow from "../../Components/Utilisateur/UtilisateurRow.svelte";
  import Users from "../../Components/Utilisateur/Utilisateurs.svelte";
  import Button from "../../Components/Inputs/Button.svelte";
  import UtilisateurRow from "../../Components/Utilisateur/UtilisateurRow.svelte";

  const modal = writable(false);
  const modalAdd = writable(false);
  const selectedUserId = writable(0);

  const handleUserClick = (id: number) => {
    openModal(id);
};
  const openModal = (id: number) => {
    modal.set(true);
    selectedUserId.set(id);
};
  const closeModal = () => {
    modal.set(false);
};

  const users = writable<User[]>([]);
  const getUsers = async () => {
      try {
          const response = await GET<any>("/user/getAllUsers");
          users.set(response.users);

      } catch (error) {
          console.error("Error fetching users:", error);
      }
  };
  onMount(getUsers);


  

</script>
<Header/>
<main>
  <section class="haut">
      <div class="haut-gauche">
          <h1 class="title">
              <span class="text">Utilisateur</span>
          </h1>
      </div>
  </section>
  <section class="offres">
    <h2 class="textSections">Admins</h2>
    {#each $users.filter(user => user.isModerator) as user}
        <UtilisateurRow {user} handleModalClick={() => handleUserClick(user.id)}  />
    {/each}
  </section>
    <section class="offres">
    <h2 class="textSections">Utilisateurs</h2>
    {#each $users.filter(user => !user.isModerator) as user}
        <UtilisateurRow {user} handleModalClick={() => handleUserClick(user.id)}  />
    {/each}
</section>


  {#if $modal}
      {#each $users as user}
          {#if user.id === $selectedUserId}
              <Users {user} handleUserClick={closeModal} />
          {/if}
      {/each}
  {/if}

</main>
<Footer/>

<style scoped>
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
  .text {
      font-size: 2.5vw;
      margin: 0;
  }
  main {
      display: flex;
      flex-direction: column;
      width: 100%;
  }
  .haut {
      display: flex;
      width: 85%;
      margin-bottom: 30px;
  }
  .haut-gauche {
      display: flex;
      flex-direction: column;
      width: 50%;
      margin-left: 5.2%;
  }
  .textSections {
    font-size: 1.8em;
    margin: 0;
    margin-top: 15px;
    margin-bottom: 5;
    color: white;
  }
</style>
