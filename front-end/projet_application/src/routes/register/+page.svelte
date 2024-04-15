<script lang="ts">
  import "../../styles/global.css";
  import Button from "../../Components/Inputs/Button.svelte";
  import Link from "../../Components/Inputs/Link.svelte";
  import type { Register } from "../../Models/Register.ts";
  import { extractErrors } from "../../ts/utils";
  import * as yup from "yup";
  import "../../styles/global.css";
  import { POST } from "../../ts/server";
  import { goto } from "$app/navigation";
  import { jwtDecode } from "jwt-decode";

  const schema = yup.object({
    user: yup.object({
      firstName: yup.string().required("Prénom requis"),
      lastName: yup.string().required("Nom de famille requis"),
      email: yup
        .string()
        .email("Courriel invalide")
        .required("Courriel requis"),
      password: yup
        .string()
        .required("Mot de passe requis")
        .matches(
          /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{12,})/,
          "Ne correspond pas aux critères de sécurité"
        ),
    }),
    validatePassword: yup
      .string()
      .required("Confirmer le mot de passe")
      .oneOf(
        [yup.ref("user.password"), null],
        "Les mots de passes ne correspondent pas"
      ),
  });
  let errors: Register = {
    user: {
      id: 0,
      firstName: "",
      lastName: "",
      email: "",
      password: "",
      role: "",
    },
    validatePassword: "",
  };

  let register: Register = {
    user: {
      id: 0,
      firstName: "",
      lastName: "",
      email: "",
      password: "",
      role: "",
    },
    validatePassword: "",
  };

  const handleSubmit = async () => {
    try {
      await schema.validate(register, { abortEarly: false });
      errors = {
        user: {
          id: 0,
          firstName: "",
          lastName: "",
          email: "",
          password: "",
          role: "",
        },
        validatePassword: "",
      };
      try {
        const response = await POST<any, any>("/user/createUser", {
          //id: 1,
          email: register.user.email,
          password: register.user.password,
          firstName: register.user.firstName,
          lastName: register.user.lastName,
          role: "user",
        });
        const data = await response.json();
        console.log(data);
        if (response.token != "") {
          const token = jwtDecode(response.token);
          console.log(token);
          localStorage.setItem("token", response.token);
          goto("/dashboard");
        }
      } catch (error) {
        errors = {
          user: {
            id: 0,
            firstName: "",
            lastName: "",
            email: "",
            password: "",
            role: "",
          },
          validatePassword: "",
        };
      }
    } catch (err) {
      errors = extractErrors(err);
    }
    // Here you can handle form submission, for now, just logging the values
  };
</script>

<div class="container">
  <h1>Créer un compte</h1>
  <form on:submit|preventDefault={handleSubmit} class="form-register">
    <div class="info-block">
      <h2>Informations personnelles</h2>
      <div class="form-fields">
        <div class="form-inputs">
          <label for="firstName">Prénom</label>
          <input
            type="text"
            id="firstName"
            bind:value={register.user.firstName}
          />
          <p class="errors-input">
            {#if errors["user.firstName"]}
              {errors["user.firstName"]}
            {/if}
          </p>
        </div>
        <div class="form-inputs">
          <label for="lastName">Nom de famille</label>
          <input
            type="text"
            class="input-lastName"
            id="lastName"
            name="lastName"
            bind:value={register.user.lastName}
          />
          <p class="errors-input">
            {#if errors["user.lastName"]}
              {errors["user.lastName"]}
            {/if}
          </p>
        </div>
      </div>
    </div>
    <div class="info-block">
      <h2>Informations de l'utilisateur</h2>
      <div class="form-connexion">
        <div class="form-inputs">
          <label for="email">Courriel</label>
          <input id="email" bind:value={register.user.email} />
          <p class="errors-input">
            {#if errors["user.email"]}
              {errors["user.email"]}
            {/if}
          </p>
        </div>
        <div class="form-inputs">
          <label for="password">Mot de passe</label>
          <input
            type="password"
            id="password"
            bind:value={register.user.password}
          />
          <p class="errors-input">
            {#if errors["user.password"]}
              {errors["user.password"]}
            {/if}
          </p>
        </div>
        <div class="form-inputs">
          <label for="password">Valider Mot de passe</label>
          <input
            type="password"
            id="confirm_password"
            bind:value={register.validatePassword}
          />
          <p class="errors-input">
            {#if errors.validatePassword}{errors.validatePassword}{/if}
          </p>
        </div>
      </div>
    </div>
    <div class="form-inputs form-submit">
      <div class="form-buttons">
        <Link text="Retour" href="/" />
      </div>
      <div class="form-buttons">
        <Button submit={true} text="Créer" />
      </div>
    </div>
  </form>
</div>

<style scoped>
  @import "../../styles/register.css";
</style>
