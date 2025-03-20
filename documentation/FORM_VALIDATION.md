# 📋 Validation d'un formulaire (Front-end & Back-end)

## 📖 Introduction

La validation d'un formulaire est essentielle pour garantir que les données soumises respectent les exigences attendues avant d'être traitées par le serveur. Ce guide explique la validation **côté front-end (Svelte)** et **côté back-end (Flask)**, en illustrant le processus avec un exemple de création d'une entreprise.

## 🏗️ Technologies utilisées

- **Front-end** : [Svelte](https://svelte.dev/) (validation côté client)
- **Back-end** : [Python](https://www.python.org/) avec [Flask](https://flask.palletsprojects.com/en/2.0.x/) (validation côté serveur)
- **Autres outils** : [Yup](https://github.com/jquense/yup) pour la validation côté front-end, reCAPTCHA pour la sécurité.

## 🚀 Fonctionnement du projet

### 🏗️ Front-end (Svelte)

Le front-end est responsable de la validation immédiate des données avant qu'elles ne soient envoyées au serveur. L'utilisateur saisit des informations sur une nouvelle entreprise dans un formulaire. Le formulaire vérifie la validité des données en temps réel et affiche des messages d'erreur si nécessaire.

**Exemple de formulaire en Svelte :**

Le formulaire inclut des champs tels que le nom de l'entreprise, l'email et le mot de passe. Chaque champ est validé selon des règles définies (ex. : un email valide, un mot de passe suffisamment sécurisé).

```html
<script lang="ts">
  import * as yup from "yup";
  import { writable } from "svelte/store";

  const schema = yup.object({
    companyName: yup.string().required("Nom de l'entreprise requis"),
    email: yup.string().email("Email invalide").required("Email requis"),
    password: yup
      .string()
      .required("Mot de passe requis")
      .matches(
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*])(?=.{12,})/,
        "Le mot de passe doit contenir au moins 12 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial"
      ),
  });

  let errors = {
    companyName: "",
    email: "",
    password: "",
  };

  let formData = {
    companyName: "",
    email: "",
    password: "",
  };

  const handleSubmit = async () => {
    try {
      await schema.validate(formData, { abortEarly: false });
      // Soumettre les données si validées
    } catch (validationErrors) {
      // Afficher les erreurs de validation
      errors = validationErrors.inner.reduce((acc, err) => {
        acc[err.path] = err.message;
        return acc;
      }, {});
    }
  };
</script>

<form on:submit|preventDefault="{handleSubmit}">
  <div>
    <label for="companyName">Nom de l'entreprise</label>
    <input type="text" id="companyName" bind:value="{formData.companyName}" />
    <p>{errors.companyName}</p>
  </div>
  <div>
    <label for="email">Courriel</label>
    <input type="email" id="email" bind:value="{formData.email}" />
    <p>{errors.email}</p>
  </div>
  <div>
    <label for="password">Mot de passe</label>
    <input type="password" id="password" bind:value="{formData.password}" />
    <p>{errors.password}</p>
  </div>
  <button type="submit">Créer</button>
</form>
```

**Exemple d'interface :**

![Exemple d'interface](../front-end/projet_application/static/images/Création%20compte%20Entreprise.png)

### 🏗️ Back-end (Flask)

Le serveur, via Flask, doit également valider les données envoyées par le formulaire afin de s'assurer qu'elles respectent les exigences nécessaires avant de les enregistrer dans la base de données.

**Exemple de validation côté serveur en Flask :**

```python
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

def validate_password(password):
    if len(password) < 12:
        return "Le mot de passe doit contenir au moins 12 caractères."
    if not re.search("[a-z]", password):
        return "Le mot de passe doit contenir une minuscule."
    if not re.search("[A-Z]", password):
        return "Le mot de passe doit contenir une majuscule."
    if not re.search("[0-9]", password):
        return "Le mot de passe doit contenir un chiffre."
    if not re.search("[!@#$%^&*]", password):
        return "Le mot de passe doit contenir un caractère spécial."
    return None

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validation des champs
    if not data.get("company_name"):
        return jsonify({"error": "Nom de l'entreprise requis"}), 400
    if not data.get("email") or "@" not in data["email"]:
        return jsonify({"error": "Email invalide"}), 400
    password_error = validate_password(data.get("password", ""))
    if password_error:
        return jsonify({"error": password_error}), 400

    # Enregistrement dans la base de données
    hashed_password = generate_password_hash(data["password"], method="sha256")
    new_company = Company(
        company_name=data["company_name"],
        email=data["email"],
        password=hashed_password,
    )

    db.session.add(new_company)
    db.session.commit()

    return jsonify({"message": "Entreprise créée avec succès!"}), 201

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
```

### 🔒 Sécurité avec reCAPTCHA

De plus, pour renforcer la sécurité, vous pouvez ajouter une vérification de reCAPTCHA dans le formulaire. Cela aide à éviter les soumissions automatisées de formulaires.

**Ajout de reCAPTCHA dans le front-end (Svelte) :**

```html
<svelte:head>
  <script
    src="https://www.google.com/recaptcha/api.js?render=your-recaptcha-key"
  ></script>
</svelte:head>

<script>
  const doRecaptcha = async () => {
    return new Promise((resolve) => {
      grecaptcha.ready(() => {
        grecaptcha
          .execute("your-recaptcha-key", { action: "submit" })
          .then((token) => resolve(token));
      });
    });
  };
</script>
```

**Vérification de reCAPTCHA côté serveur (Flask) :**

```Python
import requests

def verify_recaptcha(token):
    secret_key = "your-recaptcha-secret-key"
    url = f"https://www.google.com/recaptcha/api/siteverify?secret={secret_key}&response={token}"
    response = requests.post(url)
    result = response.json()
    return result.get("success", False)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    recaptcha_token = data.get("recaptcha_token")

    if not verify_recaptcha(recaptcha_token):
        return jsonify({"error": "reCAPTCHA échoué"}), 400
    # Continuez avec les autres validations...
```

**Exemple diagramme flux validation de formulaire front-end et back-end**

![Exemple diagramme flux validation de formulaire front-end et back-end](../front-end/projet_application/static/images/Diagramme%20flux%20validation%20de%20formulaire%20front-end%20et%20back-end.png)

## 🛠️ Conclusion

La validation des formulaires est essentielle pour assurer que les données soumises par les utilisateurs soient à la fois correctes et sécurisées. En utilisant la validation côté client avec Svelte et côté serveur avec Flask, on s'assure que seules les données valides et protégées arrivent au serveur. Cela permet non seulement de garantir la qualité des données, mais aussi d'améliorer l'expérience utilisateur en réduisant les erreurs et en fournissant des retours immédiats.
