## 📊 Diagrammes de séquence

Ce projet comprend quatre **diagrammes de séquence UML** illustrant les interactions entre les différentes couches de l'application HBnB :
- **l'utilisateur**
- la **couche de Présentation** (API),
- la **couche de Logique Métier** (Business Logic),
- et la **couche de Persistance** (Base de Données).

Ces diagrammes permettent de **visualiser le flux d’informations et de responsabilités** lors de l’exécution des principales opérations de l’application.

---

### 1️⃣ Enregistrement d’un utilisateur

Ce diagramme décrit le processus lorsqu’un utilisateur crée un nouveau compte via l’API.

- La requête est d’abord analysée pour valider les champs obligatoires (email, mot de passe, etc.).
- La couche métier vérifie que l’email n’est pas déjà utilisé dans la base de données.
- Si tout est valide, le mot de passe est haché (par exemple avec bcrypt), puis un nouvel utilisateur est créé et stocké dans la base.
- Des réponses d’erreur sont renvoyées en cas de doublon d’email, de champs invalides ou d’échec d’insertion.

**But :** garantir un enregistrement sécurisé et cohérent tout en gérant les erreurs communes.

![Diagramme](images/creation_utilisateur.png)

---

### 2️⃣ Création d’un lieu (place)

Ce diagramme montre comment un utilisateur crée une nouvelle annonce de location (lieu).

- Après validation des champs (titre, prix, localisation, etc.), l’API transmet les données à la couche métier.
- Celle-ci vérifie que l'utilisateur existe et est autorisé à publier un lieu.
- Ensuite, le lieu est créé dans la base de données.
- Si une erreur survient (données manquantes, utilisateur inexistant, ou erreur interne), une réponse appropriée est retournée.

**But :** permettre à des utilisateurs authentifiés de publier des lieux tout en gérant les erreurs d’intégrité et de droits.

![Diagramme](images/place_creation.png)

---

### 3️⃣ Soumission d’un avis (review)

Ce diagramme illustre le dépôt d’un avis par un utilisateur sur un lieu existant.

- L’API valide la note, le commentaire, et les identifiants fournis.
- La logique métier vérifie que l’utilisateur et le lieu existent.
- L’avis est ensuite stocké dans la base de données.
- Le diagramme inclut les cas d’erreur pour utilisateur ou lieu introuvable, ou données invalides.

**But :** permettre l’évaluation des lieux tout en s’assurant de l’authenticité des données et des entités impliquées.

![Diagramme](images/review_registration.png)

---

### 4️⃣ Consultation d’une liste de lieux

Ce diagramme montre comment un utilisateur récupère une liste de lieux à partir de critères de recherche (localisation, prix, nombre de chambres, etc.).

- L’API valide les paramètres de requête.
- La logique métier transmet ces critères à la base de données.
- Selon le résultat, une liste de lieux ou une réponse vide est retournée.
- Le diagramme prend aussi en compte le cas où les critères sont invalides.

**But :** offrir une recherche flexible et efficace de lieux disponibles à la location.

![Diagramme](images/fetch.png)

---

## ✅ Conclusion

Ces diagrammes de séquence permettent de **clarifier l’architecture** de l’application HBnB et d'assurer que chaque couche respecte sa responsabilité :
- La **couche de présentation** gère la validation initiale et le formatage des réponses.
- La **logique métier** applique les règles spécifiques de l’application.
- La **persistance** est responsable de l’accès aux données.

Cette approche facilite la **maintenance, la scalabilité et la fiabilité** du système. Ces diagrammes servent aussi de **base de référence pour les futurs développeurs** du projet.


- **COULIBALY Beydi**  
  [@Beydi-dev](https://github.com/Beydi-dev)

- **ROUSSEAU Thomas**  
  [@Tomsonne](https://github.com/Tomsonne)