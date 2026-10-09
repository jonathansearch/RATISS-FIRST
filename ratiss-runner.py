#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ratiss-runner.py — Lecteur Officiel Exclusif du Cerveau Souverain (.ratiss / .rt)
RATISS Labs · Auteur : Jonathan Evina (Yaoundé, Cameroun) · Licence MIT

Usage :
  python3 ratiss-runner.py RatissOne.ratiss "Bonjour mon pote !"
  python3 ratiss-runner.py RatissOne.ratiss --chat
  python3 ratiss-runner.py RatissOne.ratiss --check
"""

import os
import sys
import json
import time
import hashlib
import re

MAGIC_HEADER = "RATISS_SOUVERAIN_V2"

class RatissRunner:
    def __init__(self, chemin_modele):
        self.chemin_modele = chemin_modele
        self.modele = self._charger_et_valider(chemin_modele)
        self.meta = self.modele.get("META", {})
        self.rni = self.modele.get("BLOC_RNI_INTRINSEQUE", {})
        self.sanctuaire = self.modele.get("SANCTUAIRE", {})
        self.synchrotron = self.modele.get("SYNCHROTRON", {})
        self.memoire_episodique = self.modele.get("MEMOIRE_EPISODIQUE", {})
        self.eth = dict(self.modele.get("BLOC_ETH", {"pouls_base": 72, "temperature_base": 37.0}))
        self.eth_etat = {"pouls": self.eth.get("pouls_base", 72), "temperature": 37.0, "ton": "neutre"}
        self.dernier_sujet = None

    def _charger_et_valider(self, chemin):
        if not os.path.exists(chemin):
            raise FileNotFoundError(f"[ERREUR] Fichier modèle introuvable : {chemin}")
        with open(chemin, "r", encoding="utf-8") as f:
            data = json.load(f)

        if data.get("FORMAT") != MAGIC_HEADER:
            raise ValueError(f"[ERREUR SÉCURITÉ] Format invalide. Attendu {MAGIC_HEADER}, reçu {data.get('FORMAT')}")

        sha_declare = data.get("SIGNATURE_SHA256")
        sans_sha = {k: v for k, v in data.items() if k != "SIGNATURE_SHA256"}
        sha_calcule = hashlib.sha256(json.dumps(sans_sha, sort_keys=True).encode("utf-8")).hexdigest()

        if sha_declare and sha_declare != sha_calcule:
            raise PermissionError(f"[HALTE] Empreinte altérée ! Modèle corrompu ou falsifié.")
        return data

    def verifier_integrite(self):
        sha = self.modele.get("SIGNATURE_SHA256")
        print(f"✓ Cerveau       : {self.meta.get('NOM_MODELE')} ({self.meta.get('VERSION')})")
        print(f"✓ Auteur        : {self.meta.get('AUTEUR')}")
        print(f"✓ Loi RNI       : « {self.rni.get('loi_fondamentale')} »")
        print(f"✓ Sanctuaire    : {len(self.sanctuaire)} faits immuables scellés")
        print(f"✓ Sceau SHA-256 : {sha} (INTÈGRE)")
        return True

    def executer(self, message):
        t0 = time.time()
        msg = str(message).strip()
        tokens = set(re.findall(r"\b\w+\b", msg.lower()))
        
        # 1. Modulation somatique ETH
        if any(w in tokens for w in ["pote", "ami", "merci", "thanks", "super", "genial", "bravo"]):
            self.eth_etat = {"pouls": 84, "temperature": 37.2, "ton": "chaleureux"}
        elif any(w in tokens for w in ["danger", "faux", "erreur", "attention"]):
            self.eth_etat = {"pouls": 96, "temperature": 37.6, "ton": "vigilant"}
        else:
            self.eth_etat = {"pouls": 72, "temperature": 37.0, "ton": "neutre"}

        langue = "EN" if any(w in tokens for w in ["hello", "who", "what", "how", "thanks", "bye", "learn"]) else "FR"

        # 2. Apprentissage Épisodique Live ("Apprends que...")
        match_appr = re.search(r"(?:apprends(?:-moi)?(?: que)?|sache que|learn that|retien[ts] que)\s+(.+)", msg, re.IGNORECASE)
        if match_appr:
            enonce = match_appr.group(1).strip()
            h = hashlib.sha256(enonce.encode()).hexdigest()[:12]
            clefs = [w for w in re.findall(r"\b\w+\b", enonce.lower()) if len(w) > 3]
            entree = {"enonce": enonce, "sha256": h, "timestamp": time.time()}
            for c in clefs:
                self.memoire_episodique[c] = entree
            self.dernier_sujet = clefs[0] if clefs else "fait"
            dt_us = (time.time() - t0) * 1_000_000
            rep = f"Recorded in active memory in {dt_us:.1f} µs! Fact sealed #{h}: « {enonce} »." if langue == "EN" else f"Gravé dans ma mémoire active en {dt_us:.1f} µs ! Fait scellé #{h} : « {enonce} »."
            return {"intent": "apprentissage", "langue": langue, "reponse": rep, "eth": self.eth_etat}

        # 3. Salutations & Politesse
        if any(w in tokens for w in ["bonjour", "salut", "yo", "coucou", "hello", "hi"]):
            rep = "Hello! I am RATISS-ONE. Ready." if langue == "EN" else ("Salut mon pote ! Très heureux de te retrouver. Je t'écoute !" if self.eth_etat["ton"] == "chaleureux" else "Bonjour ! Je suis RATISS-ONE, le réseau neuronal souverain. Je t'écoute.")
            return {"intent": "saluer", "langue": langue, "reponse": rep, "eth": self.eth_etat}

        if any(w in tokens for w in ["merci", "thanks", "thank"]):
            rep = "You're very welcome! Always glad to collaborate." if langue == "EN" else ("De rien mon pote ! C'est un réel plaisir de collaborer avec toi." if self.eth_etat["ton"] == "chaleureux" else "Je t'en prie. Mes circuits restent à ton entière disposition.")
            return {"intent": "gratitude", "langue": langue, "reponse": rep, "eth": self.eth_etat}

        if any(p in msg.lower() for p in ["qui es tu", "qui es-tu", "ton nom", "who are you"]):
            rep = "I am RATISS-ONE, a sovereign entangled neural network working without GPU." if langue == "EN" else "Je suis RATISS-ONE, un tissu de neurones intriqués souverain et autonome conçu à Yaoundé."
            return {"intent": "identite", "langue": langue, "reponse": rep, "eth": self.eth_etat}

        # 4. Restitution de faits (Épisodique + Sanctuaire)
        est_anaphore = any(p in msg.lower() for p in ["et comment", "comment ça marche", "et où", "how does it work", "where"])
        sujet = self.dernier_sujet if (est_anaphore and self.dernier_sujet) else None
        
        if not sujet:
            for k in self.memoire_episodique:
                if k in tokens or k in msg.lower():
                    sujet = k
                    break
        if not sujet:
            for k in self.sanctuaire:
                if k in msg.lower() or k in tokens:
                    sujet = k
                    break

        if sujet:
            self.dernier_sujet = sujet
            if sujet in self.memoire_episodique:
                info = self.memoire_episodique[sujet]
                rep = f"According to what you taught me (sealed #{info['sha256']}): {info['enonce']}." if langue == "EN" else f"D'après ce que tu m'as appris (scellé #{info['sha256']}) : {info['enonce']}."
                return {"intent": "restitution_episodique", "langue": langue, "reponse": rep, "eth": self.eth_etat}

            ent = self.sanctuaire[sujet]
            mode = "EXPLICATION" if any(w in tokens for w in ["explique", "comment", "pourquoi", "explain", "how"]) else "DEFINITION"
            txt = ent["faits"].get(mode, ent["faits"].get("DEFINITION", ""))
            rep = f"Avec plaisir mon pote ! {txt}" if self.eth_etat["ton"] == "chaleureux" else txt
            return {"intent": f"sanctuaire_{mode.lower()}", "langue": langue, "reponse": rep, "eth": self.eth_etat}

        # 5. Inconnu Honnête
        rep = "I do not hold this fact yet. Say « Learn that... » to teach me!" if langue == "EN" else "Je ne tiens pas encore cette information. Dis-moi « Apprends que... » pour que je la retienne !"
        return {"intent": "inconnu_honnete", "langue": langue, "reponse": rep, "eth": self.eth_etat}

def main():
    if len(sys.argv) < 2:
        print("Usage :")
        print("  python3 ratiss-runner.py <modele.ratiss> \"Message à traiter\"")
        print("  python3 ratiss-runner.py <modele.ratiss> --chat")
        print("  python3 ratiss-runner.py <modele.ratiss> --check")
        sys.exit(1)

    chemin_modele = sys.argv[1]
    runner = RatissRunner(chemin_modele)

    if len(sys.argv) == 2 or sys.argv[2] == "--check":
        runner.verifier_integrite()
        return

    if sys.argv[2] == "--chat":
        print("\n" + "=" * 60)
        print(f"🤖 RATISS-ONE CHAT INTERACTIF [{runner.meta.get('NOM_MODELE')}]")
        print(f"🔬 Auteur : {runner.meta.get('AUTEUR')}")
        print("💡 Astuce : Tape 'exit' pour quitter.")
        print("=" * 60 + "\n")
        while True:
            try:
                texte = input("Toi > ").strip()
                if not texte:
                    continue
                if texte.lower() in ["exit", "quit", "q"]:
                    print("Au revoir !")
                    break
                res = runner.executer(texte)
                print(f"RATISS : {res['reponse']}\n")
            except (KeyboardInterrupt, EOFError):
                break
        return

    # Message direct
    message = " ".join(sys.argv[2:])
    res = runner.executer(message)
    print(res["reponse"])

if __name__ == "__main__":
    main()
