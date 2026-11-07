---
id: D05
lang: fr
title: Préservation des preuves
review: 2026-11-07
---

# D05 — Préservation des preuves

[↑ Documents de référence](README.md)

Les preuves servent à **comprendre** l'attaque (comment l'attaquant est entré, ce qu'il a fait), à
**vérifier** qu'il est bien parti, et à **appuyer** une plainte ou une déclaration d'assurance. Une
preuve mal collectée est souvent perdue définitivement : un redémarrage efface la mémoire vive, une
réinstallation efface le disque.

Ce document s'appuie sur la **RFC 3227** (« Guidelines for Evidence Collection and Archiving »),
la référence de base de la collecte de preuves numériques.

## 1. Les principes

1. **Collecter d'abord, analyser ensuite.** On fige l'état du système avant de chercher à comprendre.
2. **Du plus volatil au moins volatil** (section 2).
3. **Modifier le moins possible.** Chaque commande lancée sur une machine compromise laisse des traces
   et peut écraser des indices.
4. **Ne pas faire confiance au système compromis.** Ses outils (`netstat`, `ps`, `dir`) peuvent avoir
   été remplacés par l'attaquant : utiliser des outils lancés depuis un support externe protégé en
   écriture.
5. **Travailler sur une copie**, jamais sur l'original.
6. **Tout noter, en UTC.** Chaque action est datée, en précisant si l'heure est en UTC ou locale
   (convention de ce dépôt : **UTC**).
7. **Respecter la loi et la vie privée.** La collecte se limite à ce qui est nécessaire à l'enquête ;
   associer le DPO dès que des données personnelles de salariés ou de clients sont concernées.

## 2. L'ordre de collecte

Ordre de volatilité recommandé par la RFC 3227, du plus fragile au plus durable :

| Ordre | Élément | Durée de vie | Exemples d'outils (indicatifs) |
|---|---|---|---|
| 1 | Registres et cache du processeur | Nanosecondes | Rarement collectés en pratique |
| 2 | Mémoire vive, processus, connexions réseau, table de routage, cache ARP | Jusqu'à l'extinction | WinPmem, DumpIt (Windows) ; LiME, AVML (Linux) ; collecte par l'EDR |
| 3 | Systèmes de fichiers temporaires | Jusqu'au redémarrage | Copie de `/tmp`, `%TEMP%` |
| 4 | Disque | Jusqu'à réécriture | Image disque bit à bit (FTK Imager, `dd`, `dc3dd`) ; collecte ciblée (KAPE, Velociraptor) |
| 5 | Journaux distants et données de supervision | Selon la rétention | Export du SIEM, journaux du pare-feu, de l'annuaire, du proxy, de l'EDR |
| 6 | Configuration physique et topologie réseau | Longue | Schémas, configurations des équipements |
| 7 | Supports d'archivage | Très longue | Sauvegardes |

> 🕒 **Les journaux distants (ordre 5) ont souvent la rétention la plus courte en pratique.** Un
> pare-feu ou un proxy peut n'en garder que quelques jours. Demander leur export **dès l'ouverture**
> de l'incident, en parallèle de la collecte sur les machines.

## 3. Ce qu'il ne faut pas faire

| À éviter | Pourquoi | À la place |
|---|---|---|
| **Éteindre ou redémarrer** la machine | La mémoire vive est perdue ; un attaquant a pu piéger le démarrage | **Isoler du réseau** (isolation EDR, port de switch, VLAN de quarantaine) et laisser allumé |
| Lancer un antivirus « pour nettoyer » | Il supprime les fichiers malveillants avant qu'on les ait analysés | Collecter d'abord, éradiquer ensuite |
| Copier des fichiers avec l'explorateur, `xcopy` ou `tar` | Les dates d'accès changent | Image disque ou outil de collecte forensique |
| Débrancher brutalement **sans réfléchir** | Certains logiciels malveillants effacent leurs traces s'ils perdent le réseau | Évaluer avec le N2 ; en cas de rançongiciel actif, l'isolation reste la priorité |
| Analyser sur l'original | Toute modification fragilise la valeur de la preuve | Travailler sur une copie dont l'empreinte est vérifiée |

## 4. Prouver qu'une preuve n'a pas été modifiée

Chaque élément collecté reçoit une **empreinte SHA-256**, calculée **au moment de la collecte** et
recalculée **à chaque transfert**. Deux empreintes identiques prouvent que le fichier n'a pas changé.

```powershell
# Windows (PowerShell) : empreinte d'une image mémoire
Get-FileHash -Algorithm SHA256 .\poste42-memoire.raw
```

```bash
# Linux : empreinte d'une image disque
sha256sum poste42-disque.img
```

L'empreinte est recopiée dans le **registre de preuves** (section 5), jamais seulement dans un
fichier posé à côté de la preuve.

## 5. La chaîne de custody

La chaîne de custody est l'**historique complet** d'une preuve : où et quand elle a été trouvée,
qui l'a manipulée, où elle a été stockée et à qui elle a été remise. Sans elle, une preuve peut être
contestée. Pour chaque élément, on consigne :

| Champ | Exemple |
|---|---|
| Identifiant de la preuve | `INC-2026-014-P03` |
| Description | Image mémoire du poste PC-COMPTA-07 |
| Source | Nom de la machine, numéro de série, adresse IP |
| Collecte | 2026-11-07 14:32 UTC, par A. Dupont (N2), avec WinPmem lancé depuis une clé USB protégée en écriture |
| Empreinte SHA-256 | Valeur complète |
| Stockage | Disque chiffré n° 3, armoire forte du SOC |
| Transferts | Date et heure, de qui à qui, motif, empreinte vérifiée (oui ou non) |

Un modèle prêt à remplir est disponible : le [registre de preuves (T04)](../templates/T04-registre-de-preuves.md).

## 6. Conserver et protéger les preuves

- **Stockage chiffré et à accès restreint** : les preuves contiennent des données sensibles et,
  parfois, des logiciels malveillants actifs.
- **Les logiciels malveillants collectés** sont conservés dans une archive protégée par mot de passe
  (convention répandue : `infected`), sur un poste d'analyse isolé, jamais sur un poste bureautique.
- **Durée de conservation** fixée avec le juridique : au moins jusqu'à la fin de toute procédure
  judiciaire ou d'assurance liée à l'incident.
- **Jamais dans ce dépôt** : le `.gitignore` exclut les formats de preuves courants, mais la règle
  est simple : aucune donnée d'un incident réel ne va sur GitHub.

## 7. Source

- [RFC 3227 — Guidelines for Evidence Collection and Archiving](https://www.rfc-editor.org/rfc/rfc3227)
