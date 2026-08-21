"""Build the central legal JSON/HTML files and app fallback assets.

The JSON documents are the canonical in-app representation. HTML is generated
from the same data so the public pages cannot silently diverge from the app
texts. The script uses only Python's standard library.
"""

from __future__ import annotations

import argparse
import html
import json
import shutil
from pathlib import Path


LEGAL = Path(__file__).resolve().parents[1]
VERSION = "2026-08-08.2"
APP_VERSIONS = {
    "scootrules": "2026-08-08.3",
    "scootkeeper": "2026-08-08.3",
    "plakettenalarm": "2026-08-08.3",
}
LANGUAGES = ("de", "en", "es", "fr", "it", "pt")
APPS = {
    "bonsafe": "BonSafe",
    "scootkeeper": "ScootKeeper",
    "plakettenalarm": "PlakettenAlarm",
    "zahntagebuch": "ZahnTagebuch",
    "babylog": "BabyLog",
    "familybash": "FamilyBash",
    "nametrends": "NameTrends",
    "scootrules": "ScootRules",
    "sleeplog": "SleepLog",
    "snackblocker": "SnackBlocker",
}
def suffix(language: str) -> str:
    return "" if language == "de" else f"_{language}"


def section(number: int, headings: dict[str, str], bodies: dict[str, str]) -> dict:
    return {
        "number": number,
        "heading": headings,
        "body": bodies,
    }


def localized(values: dict[str, str], language: str) -> str:
    return values[language]


IMPRINT = {
    "de": {
        "title": "Impressum",
        "headings": [
            "Angaben gemäß § 5 DDG",
            "Kontakt",
            "Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV",
            "Verbraucherstreitbeilegung",
            "Haftungshinweis",
        ],
        "bodies": [
            "Marc Neumann\nSchwabenstraße 47\n71101 Schönaich\nDeutschland",
            "E-Mail: marc.neumann.neu@gmail.com",
            "Marc Neumann (Anschrift wie oben)",
            "Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen (§ 36 VSBG).",
            "Alle Inhalte der Apps werden sorgfältig recherchiert, erfolgen jedoch ohne Gewähr und stellen keine Rechts- oder Fachberatung dar.",
        ],
    },
    "en": {
        "title": "Legal Notice",
        "headings": [
            "Information pursuant to Section 5 DDG",
            "Contact",
            "Responsible for content pursuant to Section 18(2) MStV",
            "Consumer dispute resolution",
            "Disclaimer",
        ],
        "bodies": [
            "Marc Neumann\nSchwabenstraße 47\n71101 Schönaich\nGermany",
            "Email: marc.neumann.neu@gmail.com",
            "Marc Neumann (address as above)",
            "We are neither willing nor obliged to participate in dispute resolution proceedings before a consumer arbitration board (Section 36 VSBG).",
            "All app content is researched with care, but is provided without guarantee and does not constitute legal or professional advice.",
        ],
    },
    "es": {
        "title": "Aviso legal",
        "headings": [
            "Información conforme al artículo 5 DDG",
            "Contacto",
            "Responsable del contenido conforme al artículo 18, apartado 2, MStV",
            "Resolución de litigios de consumo",
            "Exención de responsabilidad",
        ],
        "bodies": [
            "Marc Neumann\nSchwabenstraße 47\n71101 Schönaich\nAlemania",
            "Correo electrónico: marc.neumann.neu@gmail.com",
            "Marc Neumann (domicilio indicado arriba)",
            "No estamos dispuestos ni obligados a participar en procedimientos de resolución de litigios ante una junta de arbitraje de consumo (artículo 36 VSBG).",
            "Todo el contenido de las aplicaciones se ha elaborado con cuidado, pero se ofrece sin garantía y no constituye asesoramiento jurídico ni profesional.",
        ],
    },
    "fr": {
        "title": "Mentions légales",
        "headings": [
            "Informations conformément à l'article 5 DDG",
            "Contact",
            "Responsable du contenu conformément à l'article 18, paragraphe 2, MStV",
            "Règlement des litiges de consommation",
            "Clause de non-responsabilité",
        ],
        "bodies": [
            "Marc Neumann\nSchwabenstraße 47\n71101 Schönaich\nAllemagne",
            "E-mail : marc.neumann.neu@gmail.com",
            "Marc Neumann (adresse indiquée ci-dessus)",
            "Nous ne sommes ni disposés ni tenus de participer à une procédure de règlement des litiges devant un organisme de médiation de la consommation (article 36 VSBG).",
            "Le contenu des applications est préparé avec soin, mais fourni sans garantie et ne constitue pas un conseil juridique ou professionnel.",
        ],
    },
    "it": {
        "title": "Note legali",
        "headings": [
            "Informazioni ai sensi dell'articolo 5 DDG",
            "Contatti",
            "Responsabile dei contenuti ai sensi dell'articolo 18, paragrafo 2, MStV",
            "Risoluzione delle controversie dei consumatori",
            "Esclusione di responsabilità",
        ],
        "bodies": [
            "Marc Neumann\nSchwabenstraße 47\n71101 Schönaich\nGermania",
            "E-mail: marc.neumann.neu@gmail.com",
            "Marc Neumann (indirizzo come sopra)",
            "Non siamo disposti né obbligati a partecipare a procedimenti di risoluzione delle controversie davanti a un organo di conciliazione dei consumatori (articolo 36 VSBG).",
            "Tutti i contenuti delle app sono preparati con cura, ma forniti senza garanzia e non costituiscono consulenza legale o professionale.",
        ],
    },
    "pt": {
        "title": "Aviso legal",
        "headings": [
            "Informações nos termos do artigo 5.º do DDG",
            "Contacto",
            "Responsável pelo conteúdo nos termos do artigo 18.º, n.º 2, MStV",
            "Resolução de litígios de consumo",
            "Exclusão de responsabilidade",
        ],
        "bodies": [
            "Marc Neumann\nSchwabenstraße 47\n71101 Schönaich\nAlemanha",
            "E-mail: marc.neumann.neu@gmail.com",
            "Marc Neumann (morada indicada acima)",
            "Não estamos dispostos nem obrigados a participar em processos de resolução de litígios perante um organismo de arbitragem de consumo (artigo 36.º VSBG).",
            "Todo o conteúdo das aplicações é preparado com cuidado, mas é fornecido sem garantia e não constitui aconselhamento jurídico ou profissional.",
        ],
    },
}


COMMON = {
    "de": {
        "controller_h": "Verantwortlicher",
        "controller_b": "Marc Neumann, Schwabenstraße 47, 71101 Schönaich, Deutschland\nE-Mail: marc.neumann.neu@gmail.com",
        "photos_h": "Fotos",
        "photos_b": "Fotos werden nur verarbeitet, wenn du die Funktion aktiv auswählst. Sie werden im app-eigenen Speicherbereich deines Geräts abgelegt. Die App nutzt den Android-Systemfotowähler beziehungsweise den System-Kameradialog und hat keinen Zugriff auf deine übrige Mediathek.",
        "notifications_h": "Benachrichtigungen",
        "notifications_b": "Erinnerungen werden vollständig lokal auf deinem Gerät geplant und ausgelöst. Dafür wird keine Verbindung zu einem Push- oder Benachrichtigungsserver aufgebaut. Die Berechtigung kannst du jederzeit in den Android-Einstellungen widerrufen.",
        "sync_h": "Abruf und Aktualisierung der Rechtstexte",
        "sync_b": "Damit Impressum und Datenschutzerklärung aktuell bleiben, ruft die App die öffentlichen Rechtstexte von GitHub Pages beziehungsweise raw.githubusercontent.com höchstens einmal alle 24 Stunden ab. Dabei wird technisch bedingt deine IP-Adresse an GitHub übertragen. Es werden keine App-Inhalte oder Nutzungsprofile an uns übermittelt. Ohne Internetverbindung werden die mit der App ausgelieferten Fassungen angezeigt. Der Abruf erfolgt in unserem berechtigten Interesse an aktuellen Pflichtinformationen (Art. 6 Abs. 1 lit. f DSGVO).",
        "rights_h": "Deine Rechte",
        "rights_b": "Du hast nach der DSGVO insbesondere das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch sowie das Recht auf Beschwerde bei einer Datenschutzaufsichtsbehörde. Da die App-Daten grundsätzlich lokal bei dir liegen, kannst du sie dort selbst einsehen, ändern oder löschen. Für Daten in einem freiwillig genutzten Google-Konto ist Google der zuständige Ansprechpartner.",
        "changes_h": "Änderungen dieser Erklärung",
        "changes_b": "Diese Datenschutzerklärung wird bei Änderungen der App, der eingesetzten Dienste oder der Datenverarbeitung angepasst. Die jeweils aktuelle Fassung ist in der App und unter der verlinkten Adresse abrufbar.",
    },
    "en": {
        "controller_h": "Controller",
        "controller_b": "Marc Neumann, Schwabenstraße 47, 71101 Schönaich, Germany\nEmail: marc.neumann.neu@gmail.com",
        "photos_h": "Photos",
        "photos_b": "Photos are processed only when you actively select the feature. They are stored in the app's private storage area on your device. The app uses the Android system photo picker or system camera dialog and has no access to the rest of your media library.",
        "notifications_h": "Notifications",
        "notifications_b": "Reminders are scheduled and triggered entirely locally on your device. No push or notification server is used for this. You can revoke the permission at any time in Android settings.",
        "sync_h": "Fetching and updating the legal texts",
        "sync_b": "To keep the legal notice and privacy policy current, the app fetches the public legal texts from GitHub Pages or raw.githubusercontent.com at most once every 24 hours. This technically transmits your IP address to GitHub. No app content or usage profile is transmitted to us. Without an internet connection, the versions bundled with the app are shown. The fetch is based on our legitimate interest in keeping mandatory information current (Art. 6(1)(f) GDPR).",
        "rights_h": "Your rights",
        "rights_b": "Under the GDPR you have, in particular, the rights of access, rectification, erasure, restriction of processing, data portability and objection, as well as the right to lodge a complaint with a data protection supervisory authority. App data is generally stored locally under your control, so you can inspect, change or delete it there. For data in a Google account used voluntarily, Google is the relevant contact.",
        "changes_h": "Changes to this policy",
        "changes_b": "This privacy policy is updated when the app, the services used or the data processing changes. The current version is available in the app and at the linked address.",
    },
    "es": {
        "controller_h": "Responsable del tratamiento",
        "controller_b": "Marc Neumann, Schwabenstraße 47, 71101 Schönaich, Alemania\nCorreo electrónico: marc.neumann.neu@gmail.com",
        "photos_h": "Fotos",
        "photos_b": "Las fotos solo se procesan cuando eliges activamente esta función. Se guardan en el área de almacenamiento propia de la aplicación en tu dispositivo. La aplicación utiliza el selector de fotos o el diálogo de cámara del sistema Android y no accede al resto de tu biblioteca multimedia.",
        "notifications_h": "Notificaciones",
        "notifications_b": "Los recordatorios se programan y activan íntegramente en tu dispositivo. No se utiliza ningún servidor de notificaciones o push. Puedes retirar el permiso en cualquier momento en los ajustes de Android.",
        "sync_h": "Consulta y actualización de los textos legales",
        "sync_b": "Para mantener actualizado el aviso legal y la política de privacidad, la aplicación consulta los textos legales públicos de GitHub Pages o raw.githubusercontent.com como máximo una vez cada 24 horas. Esto transmite técnicamente tu dirección IP a GitHub. No nos envías contenido de la aplicación ni un perfil de uso. Sin conexión a Internet se muestran las versiones incluidas en la aplicación. La consulta se basa en nuestro interés legítimo por mantener actualizada la información obligatoria (art. 6, apdo. 1, letra f del RGPD).",
        "rights_h": "Tus derechos",
        "rights_b": "Conforme al RGPD tienes, en particular, derecho de acceso, rectificación, supresión, limitación del tratamiento, portabilidad y oposición, así como derecho a presentar una reclamación ante una autoridad de control. Los datos de la aplicación se guardan normalmente de forma local bajo tu control, por lo que puedes consultarlos, modificarlos o eliminarlos allí. Para los datos de una cuenta de Google utilizada voluntariamente, el contacto competente es Google.",
        "changes_h": "Cambios de esta política",
        "changes_b": "Esta política se actualizará cuando cambien la aplicación, los servicios utilizados o el tratamiento de datos. La versión actual está disponible en la aplicación y en la dirección enlazada.",
    },
    "fr": {
        "controller_h": "Responsable du traitement",
        "controller_b": "Marc Neumann, Schwabenstraße 47, 71101 Schönaich, Allemagne\nE-mail : marc.neumann.neu@gmail.com",
        "photos_h": "Photos",
        "photos_b": "Les photos ne sont traitées que lorsque tu sélectionnes activement la fonction. Elles sont conservées dans l'espace de stockage propre à l'application sur ton appareil. L'application utilise le sélecteur de photos ou la boîte de dialogue de caméra du système Android et n'accède pas au reste de ta photothèque.",
        "notifications_h": "Notifications",
        "notifications_b": "Les rappels sont planifiés et déclenchés entièrement en local sur ton appareil. Aucun serveur push ou de notifications n'est utilisé. Tu peux retirer l'autorisation à tout moment dans les paramètres Android.",
        "sync_h": "Consultation et mise à jour des textes légaux",
        "sync_b": "Pour maintenir à jour les mentions légales et la politique de confidentialité, l'application consulte les textes légaux publics de GitHub Pages ou raw.githubusercontent.com au maximum une fois toutes les 24 heures. Cette opération transmet techniquement ton adresse IP à GitHub. Aucun contenu de l'application ni profil d'utilisation ne nous est transmis. Sans connexion Internet, les versions intégrées à l'application sont affichées. La consultation repose sur notre intérêt légitime à maintenir à jour les informations obligatoires (art. 6, par. 1, point f du RGPD).",
        "rights_h": "Tes droits",
        "rights_b": "En vertu du RGPD, tu disposes notamment des droits d'accès, de rectification, d'effacement, de limitation du traitement, de portabilité et d'opposition, ainsi que du droit d'introduire une réclamation auprès d'une autorité de contrôle. Les données de l'application sont généralement conservées localement sous ton contrôle ; tu peux donc les consulter, les modifier ou les supprimer. Pour les données d'un compte Google utilisé volontairement, Google est l'interlocuteur compétent.",
        "changes_h": "Modifications de cette politique",
        "changes_b": "Cette politique est mise à jour lorsque l'application, les services utilisés ou le traitement des données changent. La version actuelle est disponible dans l'application et à l'adresse indiquée.",
    },
    "it": {
        "controller_h": "Titolare del trattamento",
        "controller_b": "Marc Neumann, Schwabenstraße 47, 71101 Schönaich, Germania\nE-mail: marc.neumann.neu@gmail.com",
        "photos_h": "Foto",
        "photos_b": "Le foto vengono trattate solo quando selezioni attivamente la funzione. Sono conservate nell'area di archiviazione dell'app sul tuo dispositivo. L'app utilizza il selettore foto o il dialogo della fotocamera di sistema di Android e non accede al resto della tua libreria multimediale.",
        "notifications_h": "Notifiche",
        "notifications_b": "I promemoria vengono pianificati e attivati interamente in locale sul tuo dispositivo. Non viene utilizzato alcun server push o per le notifiche. Puoi revocare l'autorizzazione in qualsiasi momento nelle impostazioni di Android.",
        "sync_h": "Recupero e aggiornamento dei testi legali",
        "sync_b": "Per mantenere aggiornati le note legali e l'informativa sulla privacy, l'app recupera i testi legali pubblici da GitHub Pages o raw.githubusercontent.com al massimo una volta ogni 24 ore. Tecnicamente ciò trasmette il tuo indirizzo IP a GitHub. A noi non vengono trasmessi contenuti dell'app né profili di utilizzo. Senza connessione Internet vengono mostrate le versioni incluse nell'app. Il recupero si basa sul nostro legittimo interesse a mantenere aggiornate le informazioni obbligatorie (art. 6, par. 1, lett. f GDPR).",
        "rights_h": "I tuoi diritti",
        "rights_b": "Ai sensi del GDPR hai in particolare diritto di accesso, rettifica, cancellazione, limitazione del trattamento, portabilità e opposizione, nonché il diritto di proporre reclamo a un'autorità di controllo. I dati dell'app sono generalmente conservati localmente sotto il tuo controllo, quindi puoi consultarli, modificarli o eliminarli lì. Per i dati di un account Google utilizzato volontariamente, il referente competente è Google.",
        "changes_h": "Modifiche alla presente informativa",
        "changes_b": "La presente informativa viene aggiornata quando cambiano l'app, i servizi utilizzati o il trattamento dei dati. La versione attuale è disponibile nell'app e all'indirizzo indicato.",
    },
    "pt": {
        "controller_h": "Responsável pelo tratamento",
        "controller_b": "Marc Neumann, Schwabenstraße 47, 71101 Schönaich, Alemanha\nE-mail: marc.neumann.neu@gmail.com",
        "photos_h": "Fotografias",
        "photos_b": "As fotografias só são tratadas quando selecionas ativamente a função. São guardadas na área de armazenamento própria da aplicação no teu dispositivo. A aplicação utiliza o seletor de fotografias ou o diálogo da câmara do sistema Android e não acede ao resto da tua biblioteca multimédia.",
        "notifications_h": "Notificações",
        "notifications_b": "Os lembretes são agendados e acionados integralmente no teu dispositivo. Não é utilizado qualquer servidor push ou de notificações. Podes retirar a permissão a qualquer momento nas definições do Android.",
        "sync_h": "Consulta e atualização dos textos legais",
        "sync_b": "Para manter atualizados o aviso legal e a política de privacidade, a aplicação consulta os textos legais públicos do GitHub Pages ou raw.githubusercontent.com no máximo uma vez a cada 24 horas. Tecnicamente, isto transmite o teu endereço IP ao GitHub. Não nos são enviados conteúdos da aplicação nem um perfil de utilização. Sem ligação à Internet são apresentadas as versões incluídas na aplicação. A consulta baseia-se no nosso interesse legítimo em manter atualizada a informação obrigatória (art. 6.º, n.º 1, alínea f, do RGPD).",
        "rights_h": "Os teus direitos",
        "rights_b": "Nos termos do RGPD tens, em particular, direito de acesso, retificação, apagamento, limitação do tratamento, portabilidade e oposição, bem como o direito de apresentar uma reclamação junto de uma autoridade de controlo. Os dados da aplicação são geralmente guardados localmente sob o teu controlo, pelo que podes consultá-los, alterá-los ou eliminá-los aí. Para os dados de uma conta Google utilizada voluntariamente, o contacto competente é o Google.",
        "changes_h": "Alterações a esta política",
        "changes_b": "Esta política é atualizada quando mudam a aplicação, os serviços utilizados ou o tratamento de dados. A versão atual está disponível na aplicação e no endereço indicado.",
    },
}


APP_DATA = {
    "bonsafe": {
        "de": ("Grundprinzip: Deine Daten bleiben auf deinem Gerät", "BonSafe ist eine Offline-App zur Verwaltung von Kassenbons und Garantien. Händler, Kaufdatum, Betrag, Artikelbezeichnung, Kategorien, Notizen, Garantie- und Rückgabefristen sowie Belegfotos werden ausschließlich lokal gespeichert. Es ist kein Nutzerkonto erforderlich. Wir betreiben keinen eigenen Server und verwenden keine Analyse-, Tracking- oder Werbe-SDKs."),
        "en": ("Core principle: your data stays on your device", "BonSafe is an offline app for receipts and warranties. Retailer, purchase date, amount, item name, categories, notes, warranty and return deadlines, and receipt photos are stored exclusively locally. No user account is required. We operate no own server and use no analytics, tracking or advertising SDKs."),
        "es": ("Principio básico: tus datos permanecen en tu dispositivo", "BonSafe es una aplicación sin conexión para recibos y garantías. El comercio, la fecha de compra, el importe, el artículo, las categorías, las notas, los plazos de garantía y devolución y las fotos de los recibos se guardan únicamente de forma local. No se necesita una cuenta. No operamos un servidor propio ni utilizamos SDK de análisis, seguimiento o publicidad."),
        "fr": ("Principe de base : tes données restent sur ton appareil", "BonSafe est une application hors ligne pour les tickets et les garanties. Le commerçant, la date d'achat, le montant, l'article, les catégories, les notes, les délais de garantie et de retour ainsi que les photos des tickets sont conservés exclusivement en local. Aucun compte n'est nécessaire. Nous n'exploitons pas de serveur propre et n'utilisons aucun SDK d'analyse, de suivi ou de publicité."),
        "it": ("Principio di base: i tuoi dati restano sul dispositivo", "BonSafe è un'app offline per ricevute e garanzie. Esercente, data di acquisto, importo, articolo, categorie, note, scadenze di garanzia e reso e foto delle ricevute vengono salvati esclusivamente in locale. Non è necessario alcun account. Non gestiamo un nostro server e non utilizziamo SDK di analisi, tracciamento o pubblicità."),
        "pt": ("Princípio fundamental: os teus dados ficam no dispositivo", "BonSafe é uma aplicação offline para recibos e garantias. O comerciante, a data de compra, o valor, o artigo, as categorias, as notas, os prazos de garantia e devolução e as fotografias dos recibos são guardados exclusivamente localmente. Não é necessária uma conta. Não operamos um servidor próprio nem utilizamos SDK de análise, rastreio ou publicidade."),
    },
    "scootkeeper": {
        "de": ("Grundprinzip: Deine Daten bleiben auf deinem Gerät", "ScootKeeper ist eine Offline-App. Fahrzeugprofile, Rahmennummern, Wartungseinträge, Akku- und Kilometerdaten, Reifendruckwerte, Erinnerungen und Fotos werden ausschließlich lokal gespeichert. Wir betreiben keinen eigenen Server und verwenden keine Analyse-, Tracking- oder Werbe-SDKs."),
        "en": ("Core principle: your data stays on your device", "ScootKeeper is an offline app. Vehicle profiles, frame numbers, maintenance entries, battery and mileage data, tyre-pressure values, reminders and photos are stored exclusively locally. We operate no own server and use no analytics, tracking or advertising SDKs."),
        "es": ("Principio básico: tus datos permanecen en tu dispositivo", "ScootKeeper es una aplicación sin conexión. Los perfiles de vehículos, números de bastidor, mantenimientos, datos de batería y kilometraje, presiones de neumáticos, recordatorios y fotos se guardan únicamente de forma local. No operamos un servidor propio ni utilizamos SDK de análisis, seguimiento o publicidad."),
        "fr": ("Principe de base : tes données restent sur ton appareil", "ScootKeeper est une application hors ligne. Les profils de véhicules, numéros de cadre, opérations d'entretien, données de batterie et de kilométrage, pressions des pneus, rappels et photos sont conservés exclusivement en local. Nous n'exploitons pas de serveur propre et n'utilisons aucun SDK d'analyse, de suivi ou de publicité."),
        "it": ("Principio di base: i tuoi dati restano sul dispositivo", "ScootKeeper è un'app offline. Profili dei veicoli, numeri di telaio, interventi di manutenzione, dati di batteria e chilometraggio, pressioni degli pneumatici, promemoria e foto vengono salvati esclusivamente in locale. Non gestiamo un nostro server e non utilizziamo SDK di analisi, tracciamento o pubblicità."),
        "pt": ("Princípio fundamental: os teus dados ficam no dispositivo", "ScootKeeper é uma aplicação offline. Perfis de veículos, números de quadro, registos de manutenção, dados da bateria e quilometragem, pressão dos pneus, lembretes e fotografias são guardados exclusivamente localmente. Não operamos um servidor próprio nem utilizamos SDK de análise, rastreio ou publicidade."),
    },
    "plakettenalarm": {
        "de": ("Grundprinzip: Deine Daten bleiben auf deinem Gerät", "PlakettenAlarm funktioniert ohne Konto und ohne eigenen Server. Fahrzeuge, Versicherer, eVB- oder Versicherungsschein-Nummern, Dokumentfotos und Checklistenstand werden ausschließlich lokal gespeichert und nicht an uns übertragen."),
        "en": ("Core principle: your data stays on your device", "PlakettenAlarm works without an account and without its own server. Vehicles, insurers, eVB or insurance-certificate numbers, document photos and checklist status are stored exclusively locally and are not transmitted to us."),
        "es": ("Principio básico: tus datos permanecen en tu dispositivo", "PlakettenAlarm funciona sin cuenta y sin servidor propio. Los vehículos, aseguradoras, números eVB o de póliza, fotos de documentos y el estado de las listas se guardan únicamente de forma local y no se nos transmiten."),
        "fr": ("Principe de base : tes données restent sur ton appareil", "PlakettenAlarm fonctionne sans compte et sans serveur propre. Les véhicules, assureurs, numéros eVB ou de certificat d'assurance, photos de documents et état des listes sont conservés exclusivement en local et ne nous sont pas transmis."),
        "it": ("Principio di base: i tuoi dati restano sul dispositivo", "PlakettenAlarm funziona senza account e senza un proprio server. Veicoli, assicuratori, numeri eVB o di polizza, foto dei documenti e stato delle checklist vengono salvati esclusivamente in locale e non ci vengono trasmessi."),
        "pt": ("Princípio fundamental: os teus dados ficam no dispositivo", "PlakettenAlarm funciona sem conta e sem servidor próprio. Veículos, seguradoras, números eVB ou da apólice, fotografias de documentos e estado das listas são guardados exclusivamente localmente e não nos são transmitidos."),
    },
    "zahntagebuch": {
        "de": ("Grundprinzip: lokale Speicherung und optionale Übertragungen", "ZahnTagebuch ist eine Offline-App zur Dokumentation von Milchzähnen und Zahnwechsel. Namen und Geburtsdaten der Kinder, Profilfotos, Zahnereignisse mit Datum, Notizen, optionale Zahnfee-Beträge, Zahnfotos und Erinnerungen werden zunächst lokal gespeichert. Es ist kein Nutzerkonto erforderlich. Nur wenn du eine lokale Sicherungsdatei über den System-Teilen-Dialog teilst oder ein Google-Drive-Backup bewusst auslöst, verlassen diese Daten das Gerät. Die Einträge können personenbezogene und gesundheitsnahe Informationen über Kinder enthalten."),
        "en": ("Core principle: local storage and optional transfers", "ZahnTagebuch is an offline app for documenting baby teeth and the change of teeth. Children's names and birth dates, profile photos, dated tooth events, notes, optional tooth-fairy amounts, tooth photos and reminders are initially stored locally. No user account is required. Data leaves the device only when you share a local backup through the system share dialog or explicitly start a Google Drive backup. Entries may contain personal and health-related information about children."),
        "es": ("Principio básico: almacenamiento local y transferencias opcionales", "ZahnTagebuch es una aplicación sin conexión para documentar los dientes de leche y el cambio dental. Los nombres y fechas de nacimiento de los niños, fotos de perfil, eventos dentales con fecha, notas, cantidades opcionales del ratoncito Pérez, fotos dentales y recordatorios se guardan inicialmente de forma local. No se necesita una cuenta. Los datos solo salen del dispositivo cuando compartes una copia local mediante el diálogo del sistema o inicias conscientemente una copia en Google Drive. Las entradas pueden contener información personal y relacionada con la salud de los niños."),
        "fr": ("Principe de base : stockage local et transferts facultatifs", "ZahnTagebuch est une application hors ligne destinée à documenter les dents de lait et le changement de dentition. Les noms et dates de naissance des enfants, photos de profil, événements dentaires datés, notes, montants facultatifs de la petite souris, photos dentaires et rappels sont d'abord conservés en local. Aucun compte n'est nécessaire. Les données ne quittent l'appareil que lorsque tu partages une sauvegarde locale via la boîte de dialogue système ou que tu lances volontairement une sauvegarde Google Drive. Les saisies peuvent contenir des informations personnelles et liées à la santé des enfants."),
        "it": ("Principio di base: archiviazione locale e trasferimenti facoltativi", "ZahnTagebuch è un'app offline per documentare i denti da latte e il cambio della dentizione. Nomi e date di nascita dei bambini, foto del profilo, eventi dentali datati, note, importi facoltativi della fatina dei denti, foto dentali e promemoria vengono inizialmente salvati in locale. Non è necessario alcun account. I dati lasciano il dispositivo solo quando condividi un backup locale tramite il dialogo di sistema o avvii consapevolmente un backup Google Drive. Le registrazioni possono contenere informazioni personali e relative alla salute dei bambini."),
        "pt": ("Princípio fundamental: armazenamento local e transferências opcionais", "ZahnTagebuch é uma aplicação offline para documentar os dentes de leite e a mudança da dentição. Nomes e datas de nascimento das crianças, fotografias de perfil, eventos dentários com data, notas, valores opcionais da fada dos dentes, fotografias dentárias e lembretes são inicialmente guardados localmente. Não é necessária uma conta. Os dados só saem do dispositivo quando partilhas uma cópia local através do diálogo do sistema ou inicias conscientemente uma cópia no Google Drive. Os registos podem conter informações pessoais e relacionadas com a saúde das crianças."),
    },
    "babylog": {
        "de": ("Lokale Baby-Dokumentation", "BabyLog speichert Profile, Fütterungen, Schlaf, Windeln, Wachstum, Temperatur, Symptome, Medikamente, Impfungen, Notizen und Fotos ausschließlich lokal. Diese Einträge können Gesundheitsdaten eines Kindes enthalten; es gibt kein Nutzerkonto und keinen eigenen Server."),
        "en": ("Local baby records", "BabyLog stores profiles, feeding, sleep, nappies, growth, temperature, symptoms, medication, vaccinations, notes and photos locally only. These records may contain a child's health data; there is no user account and no own server."),
        "es": ("Registros locales del bebé", "BabyLog guarda solo localmente perfiles, alimentación, sueño, pañales, crecimiento, temperatura, síntomas, medicación, vacunas, notas y fotos. Estos registros pueden contener datos de salud de un niño; no hay cuenta ni servidor propio."),
        "fr": ("Données locales du bébé", "BabyLog conserve uniquement en local les profils, repas, sommeil, couches, croissance, température, symptômes, médicaments, vaccinations, notes et photos. Ces données peuvent contenir des données de santé d'un enfant ; aucun compte ni serveur propre n'est utilisé."),
        "it": ("Dati locali del bambino", "BabyLog salva solo localmente profili, alimentazione, sonno, pannolini, crescita, temperatura, sintomi, farmaci, vaccinazioni, note e foto. Questi dati possono contenere dati sanitari di un bambino; non esistono account o server propri."),
        "pt": ("Registos locais do bebé", "BabyLog guarda apenas localmente perfis, alimentação, sono, fraldas, crescimento, temperatura, sintomas, medicação, vacinas, notas e fotografias. Estes registos podem conter dados de saúde de uma criança; não existe conta nem servidor próprio."),
    },
    "familybash": {
        "de": ("Lokales Partyspiel", "FamilyBash verarbeitet Spielernamen, Altersgruppen, Spielstände und Einstellungen ausschließlich lokal auf einem Gerät. Die App ist für Familien und Kinder geeignet; es gibt kein Nutzerkonto und keine Analyse- oder Werbeprofile."),
        "en": ("Local party game", "FamilyBash processes player names, age groups, game state and settings locally on one device only. The app is designed for families and children; there is no user account and no analytics or advertising profile."),
        "es": ("Juego local para fiestas", "FamilyBash trata nombres de jugadores, grupos de edad, estado de juego y ajustes solo localmente en un dispositivo. La aplicación está pensada para familias y niños; no hay cuenta ni perfil de análisis o publicidad."),
        "fr": ("Jeu de fête local", "FamilyBash traite uniquement en local sur un appareil les noms des joueurs, groupes d'âge, état du jeu et réglages. L'application est destinée aux familles et aux enfants ; aucun compte ni profil d'analyse ou de publicité n'est utilisé."),
        "it": ("Gioco di gruppo locale", "FamilyBash tratta solo localmente su un dispositivo i nomi dei giocatori, le fasce d'età, lo stato del gioco e le impostazioni. L'app è pensata per famiglie e bambini; non esistono account o profili di analisi e pubblicità."),
        "pt": ("Jogo de festa local", "FamilyBash trata apenas localmente num dispositivo os nomes dos jogadores, grupos etários, estado do jogo e definições. A aplicação destina-se a famílias e crianças; não existe conta nem perfil de análise ou publicidade."),
    },
    "nametrends": {
        "de": ("Lokale Namensstatistiken", "NameTrends verarbeitet Suchanfragen, Favoriten und Einstellungen lokal. Die angezeigten Vornamenstatistiken stammen aus aggregierten, öffentlich verfügbaren Daten; es werden keine individuellen Geburts- oder Meldedaten erfasst und kein Nutzerkonto benötigt."),
        "en": ("Local name statistics", "NameTrends processes searches, favourites and settings locally. The displayed first-name statistics come from aggregated public data; no individual birth or registration data is collected and no user account is required."),
        "es": ("Estadísticas locales de nombres", "NameTrends procesa localmente búsquedas, favoritos y ajustes. Las estadísticas de nombres mostradas proceden de datos públicos agregados; no se recogen datos individuales de nacimiento o registro y no se necesita cuenta."),
        "fr": ("Statistiques locales de prénoms", "NameTrends traite localement les recherches, favoris et réglages. Les statistiques affichées proviennent de données publiques agrégées ; aucune donnée individuelle de naissance ou d'état civil n'est collectée et aucun compte n'est requis."),
        "it": ("Statistiche locali sui nomi", "NameTrends tratta localmente ricerche, preferiti e impostazioni. Le statistiche visualizzate provengono da dati pubblici aggregati; non vengono raccolti dati individuali di nascita o anagrafici e non serve un account."),
        "pt": ("Estatísticas locais de nomes", "NameTrends trata localmente pesquisas, favoritos e definições. As estatísticas apresentadas provêm de dados públicos agregados; não são recolhidos dados individuais de nascimento ou registo e não é necessária conta."),
    },
    "scootrules": {
        "de": ("Lokale Einstellungen und Standortsuche", "ScootRules speichert Sprache, Darstellung, die Bestätigung des Haftungshinweises sowie Inhalts- und Rechtstext-Caches lokal auf dem Gerät. Nach erteilter Standortberechtigung kann die App einen ungefähren Standort über die Android-Systemgeocodierung in ein Land umwandeln. Die App speichert weder die Koordinaten noch das erkannte Land dauerhaft."),
        "en": ("Local settings and location search", "ScootRules stores the language, appearance, confirmation of the disclaimer, and content and legal-text caches locally on the device. After location permission has been granted, the app may use Android system geocoding to turn an approximate location into a country. The app does not retain either the coordinates or the detected country."),
        "es": ("Ajustes locales y búsqueda de ubicación", "ScootRules guarda localmente en el dispositivo el idioma, la apariencia, la confirmación del aviso de responsabilidad y las cachés de contenidos y textos legales. Tras conceder el permiso de ubicación, la aplicación puede usar la geocodificación del sistema Android para convertir una ubicación aproximada en un país. La aplicación no conserva ni las coordenadas ni el país detectado."),
        "fr": ("Réglages locaux et recherche de localisation", "ScootRules conserve localement sur l'appareil la langue, l'apparence, la confirmation de l'avertissement de responsabilité ainsi que les caches de contenu et de textes juridiques. Après l'octroi de l'autorisation de localisation, l'application peut utiliser le géocodage du système Android pour convertir une position approximative en pays. L'application ne conserve ni les coordonnées ni le pays détecté."),
        "it": ("Impostazioni locali e ricerca della posizione", "ScootRules salva localmente sul dispositivo la lingua, l'aspetto, la conferma dell'avvertenza di responsabilità e le cache dei contenuti e dei testi legali. Dopo la concessione dell'autorizzazione alla posizione, l'app può usare la geocodifica di sistema Android per convertire una posizione approssimativa in un Paese. L'app non conserva né le coordinate né il Paese rilevato."),
        "pt": ("Definições locais e pesquisa de localização", "ScootRules guarda localmente no dispositivo o idioma, a aparência, a confirmação do aviso de responsabilidade e as caches de conteúdos e de textos legais. Depois de concedida a permissão de localização, a aplicação pode usar a geocodificação do sistema Android para converter uma localização aproximada num país. A aplicação não conserva nem as coordenadas nem o país detetado."),
    },
    "sleeplog": {
        "de": ("Lokales Schlafprotokoll", "SleepLog speichert Kinderprofile, Schlaf- und Wachzeiten, Fütterungen, Notizen und Erinnerungen ausschließlich lokal. Die Einträge können gesundheitsbezogene Informationen enthalten; es gibt kein Nutzerkonto und keinen eigenen Server."),
        "en": ("Local sleep log", "SleepLog stores child profiles, sleep and wake times, feeds, notes and reminders locally only. Records may contain health-related information; there is no user account and no own server."),
        "es": ("Registro local del sueño", "SleepLog guarda solo localmente perfiles infantiles, horas de sueño y vigilia, tomas, notas y recordatorios. Los registros pueden contener información relacionada con la salud; no hay cuenta ni servidor propio."),
        "fr": ("Journal de sommeil local", "SleepLog conserve uniquement en local les profils d'enfants, heures de sommeil et d'éveil, repas, notes et rappels. Les données peuvent contenir des informations liées à la santé ; aucun compte ni serveur propre n'est utilisé."),
        "it": ("Diario del sonno locale", "SleepLog salva solo localmente profili dei bambini, orari di sonno e veglia, poppate, note e promemoria. Le registrazioni possono contenere informazioni relative alla salute; non esistono account o server propri."),
        "pt": ("Registo local do sono", "SleepLog guarda apenas localmente perfis de crianças, horas de sono e vigília, alimentações, notas e lembretes. Os registos podem conter informação relacionada com a saúde; não existe conta nem servidor próprio."),
    },
}


FEATURES = {
    "bonsafe": {
        "de": [
            ("Optionales Google-Drive-Backup (Pro-Funktion)", "Wenn du die Backup-Funktion aktiv nutzt, werden deine Belege einschließlich Fotos als Sicherungsdatei in den versteckten, app-eigenen Bereich (\"appDataFolder\") deines Google-Drive-Kontos hochgeladen. Die Übertragung erfolgt verschlüsselt (TLS). Wir selbst erhalten keinen Zugriff. Google Ireland Limited verarbeitet Kontodaten als eigenständiger Verantwortlicher gemäß der Google-Datenschutzerklärung. Für die Anmeldung erhält die App deine E-Mail-Adresse zur Anzeige des verbundenen Kontos. Du kannst das Backup beenden, dich abmelden und die Sicherung löschen."),
            ("Käufe über Google Play", "BonSafe Pro ist ein einmaliger In-App-Kauf. Google wickelt Zahlung und Kontodaten als eigenständiger Verantwortlicher ab. Wir erhalten keine Zahlungs- oder Identitätsdaten, sondern nur den Kaufstatus; die Freischaltung wird lokal gespeichert."),
            ("Lokale Sicherung, Export und Teilen", "Sicherungsdateien und PDF-Exporte werden lokal erzeugt. Eine Weitergabe erfolgt nur, wenn du den System-Teilen-Dialog aktiv öffnest; du bestimmst den Empfänger."),
            ("Datenlöschung", "Einzelne Belege löschst du in der App. Alle lokalen Daten entfernst du durch Deinstallation oder über \"Speicher löschen\" in Android. Ein Drive-Backup löschst du in der App oder in deinem Google-Konto unter Google Drive → Einstellungen → Apps verwalten → BonSafe."),
            ("Hinweise auf weitere Apps", "In den Einstellungen kann ein Bereich \"Weitere Apps\" erscheinen. Die dafür verwendete Liste wird zusammen mit den Rechtstexten aus demselben öffentlichen Repository geladen, höchstens einmal alle 24 Stunden; es gilt derselbe Hinweis zur IP-Adresse wie beim Abruf der Rechtstexte. Es werden keine Angaben über dich oder deine Belege übertragen, und die Liste wird nicht personalisiert. Öffnest du einen Eintrag, wird der Google-Play-Store aufgerufen; dafür ist Google eigenständig verantwortlich. Rechtsgrundlage ist unser berechtigtes Interesse an der Information über eigene Apps (Art. 6 Abs. 1 lit. f DSGVO)."),
        ],
        "en": [
            ("Optional Google Drive backup (Pro feature)", "If you actively use the backup feature, receipts including photos are uploaded as a backup file to the hidden app-specific appDataFolder of your Google Drive account. The transfer is encrypted (TLS). We have no access to the backup. Google Ireland Limited processes account data as an independent controller under Google's privacy policy. The app receives your email address to display the connected account. You can stop the backup, sign out and delete the backup."),
            ("Purchases via Google Play", "BonSafe Pro is a one-time in-app purchase. Google handles payment and account data as an independent controller. We receive no payment or identity data, only the purchase status; the unlock is stored locally."),
            ("Local backup, export and sharing", "Backup files and PDF exports are created locally. They are shared only when you actively open the system share dialog; you choose the recipient."),
            ("Deleting data", "Delete individual receipts in the app. Remove all local data by uninstalling or using Android's Clear storage option. Delete a Drive backup in the app or in your Google account under Google Drive → Settings → Manage apps → BonSafe."),
            ("References to other apps", "Settings may show a \"More apps\" area. The list used for it is fetched together with the legal texts from the same public repository, at most once every 24 hours; the same note about your IP address applies as for fetching the legal texts. No information about you or your receipts is transmitted, and the list is not personalised. Opening an entry launches the Google Play Store, for which Google is independently responsible. The legal basis is our legitimate interest in informing you about our own apps (Art. 6(1)(f) GDPR)."),
        ],
        "es": [
            ("Copia opcional en Google Drive (función Pro)", "Si utilizas activamente la función de copia, los recibos, incluidas las fotos, se cargan como archivo de copia en el área oculta appDataFolder de tu cuenta de Google Drive. La transferencia está cifrada (TLS). No tenemos acceso a la copia. Google Ireland Limited trata los datos de la cuenta como responsable independiente según su política de privacidad. La aplicación recibe tu correo electrónico para mostrar la cuenta conectada. Puedes detener la copia, cerrar sesión y eliminarla."),
            ("Compras mediante Google Play", "BonSafe Pro es una compra única dentro de la aplicación. Google gestiona los datos de pago y de la cuenta como responsable independiente. Solo recibimos el estado de la compra; la activación se guarda localmente."),
            ("Copia local, exportación y uso compartido", "Los archivos de copia y los PDF se crean localmente. Solo se comparten cuando abres activamente el diálogo del sistema; tú eliges el destinatario."),
            ("Eliminación de datos", "Puedes eliminar recibos individuales en la aplicación. Elimina todos los datos locales desinstalando la aplicación o usando la opción de borrar almacenamiento de Android. Elimina la copia de Drive en la aplicación o en tu cuenta de Google, en Google Drive → Ajustes → Gestionar aplicaciones → BonSafe."),
            ("Referencias a otras aplicaciones", "En los ajustes puede aparecer una sección \"Más aplicaciones\". La lista utilizada se descarga junto con los textos legales desde el mismo repositorio público, como máximo una vez cada 24 horas; se aplica la misma indicación sobre tu dirección IP que en la descarga de los textos legales. No se transmite ningún dato sobre ti ni sobre tus recibos, y la lista no está personalizada. Si abres una entrada, se inicia Google Play Store, del que Google es responsable de forma independiente. La base jurídica es nuestro interés legítimo en informar sobre nuestras propias aplicaciones (art. 6(1)(f) RGPD)."),
        ],
        "fr": [
            ("Sauvegarde Google Drive facultative (fonction Pro)", "Si tu utilises activement la sauvegarde, les tickets, photos comprises, sont téléversés sous forme de fichier dans la zone masquée appDataFolder de ton compte Google Drive. Le transfert est chiffré (TLS). Nous n'avons pas accès à la sauvegarde. Google Ireland Limited traite les données du compte en tant que responsable indépendant selon sa politique de confidentialité. L'application reçoit ton adresse e-mail pour afficher le compte connecté. Tu peux arrêter la sauvegarde, te déconnecter et la supprimer."),
            ("Achats via Google Play", "BonSafe Pro est un achat intégré unique. Google traite les données de paiement et du compte en tant que responsable indépendant. Nous ne recevons que le statut de l'achat ; l'activation est conservée en local."),
            ("Sauvegarde locale, export et partage", "Les fichiers de sauvegarde et les PDF sont créés en local. Ils ne sont partagés que lorsque tu ouvres activement la boîte de dialogue système ; tu choisis le destinataire."),
            ("Suppression des données", "Supprime les tickets individuels dans l'application. Supprime toutes les données locales en désinstallant l'application ou via l'option d'effacement du stockage Android. Supprime une sauvegarde Drive dans l'application ou dans ton compte Google, sous Google Drive → Paramètres → Gérer les applications → BonSafe."),
            ("Références à d'autres applications", "Les paramètres peuvent afficher une rubrique \"Autres applications\". La liste utilisée est téléchargée avec les textes juridiques depuis le même dépôt public, au maximum une fois toutes les 24 heures ; la même remarque concernant ton adresse IP s'applique que pour le téléchargement des textes juridiques. Aucune information te concernant ou concernant tes tickets n'est transmise, et la liste n'est pas personnalisée. L'ouverture d'une entrée lance le Google Play Store, dont Google est responsable de manière indépendante. La base légale est notre intérêt légitime à informer sur nos propres applications (art. 6, § 1, point f, RGPD)."),
        ],
        "it": [
            ("Backup Google Drive facoltativo (funzione Pro)", "Se utilizzi attivamente il backup, le ricevute, comprese le foto, vengono caricate come file nell'area nascosta appDataFolder del tuo account Google Drive. Il trasferimento è crittografato (TLS). Non abbiamo accesso al backup. Google Ireland Limited tratta i dati dell'account come titolare autonomo secondo la propria informativa. L'app riceve il tuo indirizzo e-mail per mostrare l'account collegato. Puoi interrompere il backup, disconnetterti ed eliminarlo."),
            ("Acquisti tramite Google Play", "BonSafe Pro è un acquisto in-app una tantum. Google gestisce i dati di pagamento e dell'account come titolare autonomo. Riceviamo solo lo stato dell'acquisto; lo sblocco viene salvato localmente."),
            ("Backup locale, esportazione e condivisione", "I file di backup e i PDF vengono creati localmente. Vengono condivisi solo quando apri attivamente il dialogo di condivisione del sistema; scegli tu il destinatario."),
            ("Cancellazione dei dati", "Elimina le ricevute singole nell'app. Rimuovi tutti i dati locali disinstallando l'app o usando l'opzione per cancellare lo spazio di archiviazione di Android. Elimina un backup Drive nell'app o nel tuo account Google, in Google Drive → Impostazioni → Gestisci app → BonSafe."),
            ("Riferimenti ad altre app", "Nelle impostazioni può comparire una sezione \"Altre app\". L'elenco utilizzato viene scaricato insieme ai testi legali dallo stesso repository pubblico, al massimo una volta ogni 24 ore; vale la stessa indicazione sull'indirizzo IP prevista per il recupero dei testi legali. Non vengono trasmessi dati su di te o sulle tue ricevute e l'elenco non è personalizzato. Aprendo una voce si avvia il Google Play Store, di cui Google è titolare autonomo. La base giuridica è il nostro legittimo interesse a informare sulle nostre app (art. 6, par. 1, lett. f, GDPR)."),
        ],
        "pt": [
            ("Cópia opcional no Google Drive (função Pro)", "Se utilizares ativamente a função de cópia, os recibos, incluindo fotografias, são carregados como ficheiro para a área oculta appDataFolder da tua conta Google Drive. A transferência é cifrada (TLS). Não temos acesso à cópia. A Google Ireland Limited trata os dados da conta como responsável independente segundo a política de privacidade da Google. A aplicação recebe o teu e-mail para apresentar a conta ligada. Podes parar a cópia, terminar sessão e eliminá-la."),
            ("Compras através do Google Play", "BonSafe Pro é uma compra única na aplicação. A Google trata os dados de pagamento e da conta como responsável independente. Recebemos apenas o estado da compra; a ativação é guardada localmente."),
            ("Cópia local, exportação e partilha", "Os ficheiros de cópia e os PDF são criados localmente. Só são partilhados quando abres ativamente o diálogo de partilha do sistema; escolhes o destinatário."),
            ("Eliminação de dados", "Elimina recibos individuais na aplicação. Remove todos os dados locais desinstalando a aplicação ou usando a opção de limpar o armazenamento do Android. Elimina uma cópia do Drive na aplicação ou na tua conta Google, em Google Drive → Definições → Gerir aplicações → BonSafe."),
            ("Referências a outras aplicações", "Nas definições pode surgir uma secção \"Mais aplicações\". A lista utilizada é transferida juntamente com os textos legais a partir do mesmo repositório público, no máximo uma vez a cada 24 horas; aplica-se a mesma indicação sobre o teu endereço IP que na transferência dos textos legais. Não são transmitidos dados sobre ti nem sobre os teus recibos e a lista não é personalizada. Ao abrires uma entrada, é iniciada a Google Play Store, pela qual a Google é responsável de forma independente. A base jurídica é o nosso interesse legítimo em informar sobre as nossas aplicações (art. 6.º, n.º 1, al. f), RGPD)."),
        ],
    },
    "scootkeeper": {
        "de": [
            ("Optionales Google-Drive-Backup (Pro-Funktion)", "Wenn du die Backup-Funktion aktiv nutzt, werden deine App-Daten einschließlich Fotos als Sicherungsdatei in den versteckten, app-eigenen Bereich (\"appDataFolder\") deines Google-Drive-Kontos hochgeladen. Die Übertragung erfolgt verschlüsselt (TLS). Wir erhalten keinen Zugriff auf die Sicherung. Google Ireland Limited verarbeitet Kontodaten als eigenständiger Verantwortlicher. Für die Anmeldung nutzt du Google Sign-In; deine Google-E-Mail-Adresse wird nur zur Anzeige des verbundenen Kontos verwendet. Du kannst das Backup beenden und dich abmelden."),
            ("Exporte und Teilen", "PDF-, CSV- und Kalender-Exporte werden lokal erzeugt und nur geteilt, wenn du den System-Teilen-Dialog aktiv öffnest. Du bestimmst den Empfänger."),
            ("Google Play: Kauf und Bewertung", "Kostenpflichtige Pro-Funktionen werden über Google Play Billing abgewickelt. Google verarbeitet Zahlungs- und Kontodaten; wir erhalten nur den Kauf- beziehungsweise Abostatus. Nach mehreren erfassten Wartungseinträgen kann die App einmalig die von Google Play bereitgestellte Bewertungsfunktion öffnen. Darüber übermittelt die App keine Fahrzeug-, Wartungs- oder Backupdaten."),
            ("Datenlöschung", "Alle lokalen Daten löschst du durch Deinstallation oder über \"Speicher löschen\" in Android. Ein Drive-Backup löschst du in deinem Google-Konto unter Google Drive → Einstellungen → Apps verwalten → ScootKeeper."),
        ],
        "en": [
            ("Optional Google Drive backup (Pro feature)", "If you actively use the backup feature, app data including photos is uploaded as a backup file to the hidden app-specific appDataFolder of your Google Drive account. The transfer is encrypted (TLS). We have no access to the backup. Google Ireland Limited processes account data as an independent controller. You sign in with Google Sign-In; your Google email address is used only to display the connected account. You can stop the backup and sign out."),
            ("Exports and sharing", "PDF, CSV and calendar exports are created locally and shared only when you actively open the system share dialog. You choose the recipient."),
            ("Google Play: purchase and review", "Paid Pro features are processed through Google Play Billing. Google processes payment and account data; we receive only the purchase or subscription status. After several recorded maintenance entries, the app may open the review feature provided by Google Play once. The app does not transmit vehicle, maintenance or backup data through it."),
            ("Deleting data", "Remove all local data by uninstalling the app or using Android's Clear storage option. Delete a Drive backup in your Google account under Google Drive → Settings → Manage apps → ScootKeeper."),
        ],
        "es": [
            ("Copia opcional en Google Drive (función Pro)", "Si utilizas activamente la copia, los datos de la aplicación, incluidas las fotos, se cargan como archivo en el área oculta appDataFolder de tu cuenta de Google Drive. La transferencia está cifrada (TLS). No tenemos acceso a la copia. Google Ireland Limited trata los datos de la cuenta como responsable independiente. Inicias sesión con Google Sign-In; tu dirección de correo de Google se usa solo para mostrar la cuenta conectada. Puedes detener la copia y cerrar sesión."),
            ("Exportaciones y uso compartido", "Las exportaciones PDF, CSV y de calendario se crean localmente y solo se comparten cuando abres activamente el diálogo del sistema. Tú eliges el destinatario."),
            ("Google Play: compra y valoración", "Las funciones Pro de pago se procesan mediante Google Play Billing. Google trata los datos de pago y de la cuenta; solo recibimos el estado de compra o suscripción. Tras registrar varias entradas de mantenimiento, la aplicación puede abrir una vez la función de valoración proporcionada por Google Play. La aplicación no transmite datos de vehículo, mantenimiento ni copia de seguridad a través de ella."),
            ("Eliminación de datos", "Elimina todos los datos locales desinstalando la aplicación o usando la opción de borrar almacenamiento de Android. Elimina una copia de Drive en tu cuenta de Google, en Google Drive → Ajustes → Gestionar aplicaciones → ScootKeeper."),
        ],
        "fr": [
            ("Sauvegarde Google Drive facultative (fonction Pro)", "Si tu utilises activement la sauvegarde, les données de l'application, photos comprises, sont téléversées dans la zone masquée appDataFolder de ton compte Google Drive. Le transfert est chiffré (TLS). Nous n'avons pas accès à la sauvegarde. Google Ireland Limited traite les données du compte en tant que responsable indépendant. Tu te connectes avec Google Sign-In ; ton adresse e-mail Google sert uniquement à afficher le compte connecté. Tu peux arrêter la sauvegarde et te déconnecter."),
            ("Exports et partage", "Les exports PDF, CSV et calendrier sont créés en local et partagés uniquement lorsque tu ouvres activement la boîte de dialogue système. Tu choisis le destinataire."),
            ("Google Play : achat et évaluation", "Les fonctions Pro payantes sont traitées via Google Play Billing. Google traite les données de paiement et du compte ; nous recevons uniquement le statut d'achat ou d'abonnement. Après plusieurs entrées d'entretien enregistrées, l'application peut ouvrir une fois la fonction d'évaluation fournie par Google Play. L'application ne transmet aucune donnée de véhicule, d'entretien ou de sauvegarde par ce biais."),
            ("Suppression des données", "Supprime toutes les données locales en désinstallant l'application ou via l'option d'effacement du stockage Android. Supprime une sauvegarde Drive dans ton compte Google, sous Google Drive → Paramètres → Gérer les applications → ScootKeeper."),
        ],
        "it": [
            ("Backup Google Drive facoltativo (funzione Pro)", "Se utilizzi attivamente il backup, i dati dell'app, comprese le foto, vengono caricati nell'area nascosta appDataFolder del tuo account Google Drive. Il trasferimento è crittografato (TLS). Non abbiamo accesso al backup. Google Ireland Limited tratta i dati dell'account come titolare autonomo. Accedi con Google Sign-In; il tuo indirizzo email Google viene usato solo per mostrare l'account collegato. Puoi interrompere il backup e disconnetterti."),
            ("Esportazioni e condivisione", "Le esportazioni PDF, CSV e calendario vengono create localmente e condivise solo quando apri attivamente il dialogo di condivisione del sistema. Scegli tu il destinatario."),
            ("Google Play: acquisto e valutazione", "Le funzioni Pro a pagamento sono gestite tramite Google Play Billing. Google tratta i dati di pagamento e dell'account; riceviamo solo lo stato dell'acquisto o dell'abbonamento. Dopo diverse voci di manutenzione registrate, l'app può aprire una volta la funzione di valutazione fornita da Google Play. L'app non trasmette dati di veicolo, manutenzione o backup tramite tale funzione."),
            ("Cancellazione dei dati", "Rimuovi tutti i dati locali disinstallando l'app o usando l'opzione per cancellare lo spazio di archiviazione di Android. Elimina un backup Drive nel tuo account Google, in Google Drive → Impostazioni → Gestisci app → ScootKeeper."),
        ],
        "pt": [
            ("Cópia opcional no Google Drive (função Pro)", "Se utilizares ativamente a cópia, os dados da aplicação, incluindo fotografias, são carregados para a área oculta appDataFolder da tua conta Google Drive. A transferência é cifrada (TLS). Não temos acesso à cópia. A Google Ireland Limited trata os dados da conta como responsável independente. Inicias sessão com o Google Sign-In; o teu endereço de email Google é usado apenas para mostrar a conta associada. Podes parar a cópia e terminar sessão."),
            ("Exportações e partilha", "As exportações PDF, CSV e de calendário são criadas localmente e só são partilhadas quando abres ativamente o diálogo de partilha do sistema. Escolhes o destinatário."),
            ("Google Play: compra e avaliação", "As funções Pro pagas são processadas através do Google Play Billing. A Google trata os dados de pagamento e da conta; recebemos apenas o estado da compra ou da subscrição. Após vários registos de manutenção, a aplicação pode abrir uma vez a função de avaliação fornecida pelo Google Play. A aplicação não transmite dados de veículo, manutenção ou cópia de segurança através dela."),
            ("Eliminação de dados", "Remove todos os dados locais desinstalando a aplicação ou usando a opção de limpar o armazenamento do Android. Elimina uma cópia do Drive na tua conta Google, em Google Drive → Definições → Gerir aplicações → ScootKeeper."),
        ],
    },
    "plakettenalarm": {
        "de": [
            ("Abruf der Anbieterliste, Rechtstexte und App-Liste", "Beim Start lädt die App aktuelle Anbieterinformationen, die Rechtstexte und die Liste unserer weiteren Apps von GitHub Pages beziehungsweise raw.githubusercontent.com. Technisch bedingt wird dabei deine IP-Adresse an GitHub übertragen. Es werden keine App-Daten oder Nutzungsprofile an uns gesendet. Alle Inhalte sind auch offline aus dem App-Fallback verfügbar."),
            ("Externe Links und Partner-Kennungen", "Wenn du ein Angebot öffnest, verlässt du die App und es gilt die Datenschutzerklärung des jeweiligen Anbieters. Die Links können eine Partner-Kennung (Affiliate-Kennung) enthalten. Sie dient der Zuordnung des Aufrufs; wir übermitteln dem Anbieter keine zusätzlichen App-Daten."),
            ("Google Play: Bewertungsfunktion", "Wenn du die Saison-Checkliste vollständig abgehakt hast, kann die App einmal pro Verkehrsjahr die von Google Play bereitgestellte Bewertungsfunktion öffnen. Ob der Dialog tatsächlich erscheint, entscheidet Google Play. Die App übermittelt dabei keine Fahrzeug-, Versicherungs- oder Nutzungsdaten."),
            ("Keine Analyse- oder Werbe-Tracker", "Die App verwendet keine Analyse-Tools, keine Werbenetzwerke und kein Tracking. Es werden keine Werbe-IDs verarbeitet."),
            ("Datenlöschung", "Einzelne Fahrzeuge und Dokumentfotos kannst du in der App löschen. Alle lokalen Daten entfernst du durch Deinstallation oder über \"Speicher löschen\" in Android."),
        ],
        "en": [
            ("Fetching the provider list, legal texts and app list", "At startup the app fetches current provider information, the legal texts and the list of our other apps from GitHub Pages or raw.githubusercontent.com. This technically transmits your IP address to GitHub. No app data or usage profile is sent to us. All content is also available offline from the bundled fallback."),
            ("External links and partner identifiers", "When you open an offer, you leave the app and the provider's privacy policy applies. Links may contain a partner identifier used to attribute the visit; we do not send the provider additional app data."),
            ("Google Play: review prompt", "Once you have fully completed the season checklist, the app may open the review function provided by Google Play once per insurance year. Google Play decides whether the dialog actually appears. The app transmits no vehicle, insurance or usage data in the process."),
            ("No analytics or advertising trackers", "The app uses no analytics tools, advertising networks or tracking and processes no advertising IDs."),
            ("Deleting data", "Delete individual vehicles and document photos in the app. Remove all local data by uninstalling the app or using Android's Clear storage option."),
        ],
        "es": [
            ("Consulta de la lista de proveedores, los textos legales y la lista de aplicaciones", "Al iniciar, la aplicación consulta información actual de proveedores, los textos legales y la lista de nuestras otras aplicaciones desde GitHub Pages o raw.githubusercontent.com. Esto transmite técnicamente tu dirección IP a GitHub. No nos envías datos de la aplicación ni un perfil de uso. Todo el contenido también está disponible sin conexión mediante la copia incluida."),
            ("Enlaces externos e identificadores de socios", "Al abrir una oferta sales de la aplicación y se aplica la política de privacidad del proveedor. Los enlaces pueden contener un identificador de socio para atribuir la visita; no enviamos al proveedor datos adicionales de la aplicación."),
            ("Google Play: función de valoración", "Cuando hayas completado por entero la lista de comprobación de la temporada, la aplicación puede abrir una vez por año de seguro la función de valoración proporcionada por Google Play. Google Play decide si el diálogo aparece realmente. La aplicación no transmite datos del vehículo, del seguro ni de uso."),
            ("Sin análisis ni rastreadores publicitarios", "La aplicación no utiliza herramientas de análisis, redes publicitarias ni seguimiento y no procesa identificadores publicitarios."),
            ("Eliminación de datos", "Puedes eliminar vehículos y fotos de documentos individuales en la aplicación. Elimina todos los datos locales desinstalando la aplicación o usando la opción de borrar almacenamiento de Android."),
        ],
        "fr": [
            ("Consultation de la liste des fournisseurs, des textes légaux et de la liste des applications", "Au démarrage, l'application consulte les informations actuelles sur les fournisseurs, les textes légaux et la liste de nos autres applications depuis GitHub Pages ou raw.githubusercontent.com. Cette opération transmet techniquement ton adresse IP à GitHub. Aucune donnée de l'application ni profil d'utilisation ne nous est envoyé. Tous les contenus sont aussi disponibles hors ligne grâce à la copie intégrée."),
            ("Liens externes et identifiants partenaires", "Lorsque tu ouvres une offre, tu quittes l'application et la politique du fournisseur s'applique. Les liens peuvent contenir un identifiant partenaire pour attribuer la visite ; nous n'envoyons pas au fournisseur d'autres données de l'application."),
            ("Google Play : fonction d'évaluation", "Une fois la liste de contrôle de la saison entièrement cochée, l'application peut ouvrir une fois par année d'assurance la fonction d'évaluation fournie par Google Play. C'est Google Play qui décide si la boîte de dialogue s'affiche réellement. L'application ne transmet aucune donnée de véhicule, d'assurance ou d'utilisation."),
            ("Aucun outil d'analyse ni traceur publicitaire", "L'application n'utilise aucun outil d'analyse, réseau publicitaire ou suivi et ne traite aucun identifiant publicitaire."),
            ("Suppression des données", "Supprime les véhicules et photos de documents individuellement dans l'application. Supprime toutes les données locales en désinstallant l'application ou via l'effacement du stockage Android."),
        ],
        "it": [
            ("Recupero dell'elenco dei fornitori, dei testi legali e dell'elenco delle app", "All'avvio l'app recupera le informazioni aggiornate sui fornitori, i testi legali e l'elenco delle nostre altre app da GitHub Pages o raw.githubusercontent.com. Tecnicamente ciò trasmette il tuo indirizzo IP a GitHub. A noi non vengono inviati dati dell'app né profili di utilizzo. Tutti i contenuti sono disponibili anche offline tramite la copia inclusa."),
            ("Link esterni e identificativi dei partner", "Quando apri un'offerta lasci l'app e si applica l'informativa del fornitore. I link possono contenere un identificativo del partner per attribuire la visita; non inviamo al fornitore altri dati dell'app."),
            ("Google Play: funzione di valutazione", "Quando hai completato interamente la lista di controllo stagionale, l'app può aprire una volta per anno assicurativo la funzione di valutazione fornita da Google Play. È Google Play a decidere se la finestra viene effettivamente mostrata. L'app non trasmette dati del veicolo, dell'assicurazione o di utilizzo."),
            ("Nessuna analisi o pubblicità tracciante", "L'app non utilizza strumenti di analisi, reti pubblicitarie o tracciamento e non tratta identificativi pubblicitari."),
            ("Cancellazione dei dati", "Elimina singolarmente veicoli e foto dei documenti nell'app. Rimuovi tutti i dati locali disinstallando l'app o usando l'opzione per cancellare lo spazio di archiviazione di Android."),
        ],
        "pt": [
            ("Consulta da lista de fornecedores, dos textos legais e da lista de aplicações", "No arranque, a aplicação consulta informações atualizadas dos fornecedores, os textos legais e a lista das nossas outras aplicações no GitHub Pages ou raw.githubusercontent.com. Tecnicamente, isto transmite o teu endereço IP ao GitHub. Não nos são enviados dados da aplicação nem um perfil de utilização. Todos os conteúdos também estão disponíveis offline através da cópia incluída."),
            ("Ligações externas e identificadores de parceiros", "Quando abres uma oferta, sais da aplicação e aplica-se a política de privacidade do fornecedor. As ligações podem conter um identificador de parceiro para atribuir a visita; não enviamos ao fornecedor outros dados da aplicação."),
            ("Google Play: função de avaliação", "Depois de concluíres integralmente a lista de verificação da época, a aplicação pode abrir uma vez por ano de seguro a função de avaliação disponibilizada pelo Google Play. É o Google Play que decide se a caixa de diálogo é efetivamente apresentada. A aplicação não transmite dados do veículo, do seguro ou de utilização."),
            ("Sem análise nem rastreadores publicitários", "A aplicação não utiliza ferramentas de análise, redes publicitárias ou rastreio e não trata identificadores publicitários."),
            ("Eliminação de dados", "Elimina veículos e fotografias de documentos individualmente na aplicação. Remove todos os dados locais desinstalando a aplicação ou usando a opção de limpar o armazenamento do Android."),
        ],
    },
    "zahntagebuch": {
        "de": [
            ("Lokale Sicherung, Teilen und Google Drive", "Du kannst deine Daten einschließlich Fotos als lokale Sicherungsdatei exportieren und importieren oder das Zahnschema als Bild erzeugen. Eine Weitergabe erfolgt nur über den von dir aktiv geöffneten System-Teilen-Dialog. Wenn du ein Google-Drive-Backup bewusst auslöst, werden die Daten in den versteckten, app-eigenen Bereich (appDataFolder) deines Google-Drive-Kontos übertragen. Die App erhält keinen Zugriff auf andere Drive-Dateien. Das Drive-Backup kannst du jederzeit in der App löschen."),
            ("Google Play: Kauf und Bewertung", "ZahnTagebuch Pro ist ein einmaliger In-App-Kauf. Google Play verarbeitet Zahlungs- und Kontodaten; die App speichert nur den Kaufstatus. Nach dem dritten erfassten Zahn kann die App einmalig die von Google Play bereitgestellte Bewertungsfunktion öffnen. Darüber übermittelt die App keine Zahn-, Profil- oder Backupdaten."),
            ("Datenlöschung", "Lösche einzelne Einträge oder Kinderprofile in der App. Alle lokalen Daten entfernst du durch Deinstallation oder über \"Speicher löschen\" in Android. Ein Drive-Backup löschst du in der App oder in deinem Google-Konto."),
        ],
        "en": [
            ("Local backup, sharing and Google Drive", "You can export and import your data including photos as a local backup file or generate the tooth chart as an image. Sharing occurs only through the system share dialog that you actively open. When you explicitly start a Google Drive backup, the data is transferred to the hidden app-specific appDataFolder of your Google Drive account. The app cannot access other Drive files. You can delete the Drive backup in the app at any time."),
            ("Google Play: purchase and review", "ZahnTagebuch Pro is a one-time in-app purchase. Google Play processes payment and account data; the app stores only the purchase status. After the third recorded tooth, the app may open the review feature provided by Google Play once. The app does not transmit tooth, profile or backup data through it."),
            ("Deleting data", "Delete individual entries or child profiles in the app. Remove all local data by uninstalling the app or using Android's Clear storage option. Delete a Drive backup in the app or in your Google account."),
        ],
        "es": [
            ("Copia local, uso compartido y Google Drive", "Puedes exportar e importar tus datos, incluidas las fotos, como archivo de copia local o generar el esquema dental como imagen. Solo se comparte mediante el diálogo del sistema que abres activamente. Cuando inicias conscientemente una copia en Google Drive, los datos se transfieren al área oculta appDataFolder de tu cuenta de Google Drive. La aplicación no puede acceder a otros archivos de Drive. Puedes eliminar la copia de Drive en la aplicación en cualquier momento."),
            ("Google Play: compra y valoración", "ZahnTagebuch Pro es una compra única dentro de la aplicación. Google Play trata los datos de pago y de la cuenta; la aplicación solo guarda el estado de la compra. Tras el tercer diente registrado, la aplicación puede abrir una vez la función de valoración proporcionada por Google Play. La aplicación no transmite datos dentales, de perfiles ni de copias mediante ella."),
            ("Eliminación de datos", "Elimina entradas individuales o perfiles de niños en la aplicación. Elimina todos los datos locales desinstalando la aplicación o usando la opción de borrar almacenamiento de Android. Elimina una copia de Drive en la aplicación o en tu cuenta de Google."),
        ],
        "fr": [
            ("Sauvegarde locale, partage et Google Drive", "Tu peux exporter et importer tes données, photos comprises, dans un fichier de sauvegarde local ou générer le schéma dentaire comme image. Le partage ne se fait que par la boîte de dialogue système que tu ouvres activement. Lorsque tu lances volontairement une sauvegarde Google Drive, les données sont transférées dans la zone masquée appDataFolder de ton compte Google Drive. L'application ne peut pas accéder aux autres fichiers Drive. Tu peux supprimer la sauvegarde Drive dans l'application à tout moment."),
            ("Google Play : achat et évaluation", "ZahnTagebuch Pro est un achat intégré unique. Google Play traite les données de paiement et du compte ; l'application ne conserve que le statut de l'achat. Après la troisième dent enregistrée, l'application peut ouvrir une fois la fonction d'évaluation fournie par Google Play. L'application ne transmet aucune donnée dentaire, de profil ou de sauvegarde par cette fonction."),
            ("Suppression des données", "Supprime les entrées ou profils d'enfants individuels dans l'application. Supprime toutes les données locales en désinstallant l'application ou via l'effacement du stockage Android. Supprime une sauvegarde Drive dans l'application ou dans ton compte Google."),
        ],
        "it": [
            ("Backup locale, condivisione e Google Drive", "Puoi esportare e importare i dati, comprese le foto, come file di backup locale o generare lo schema dentale come immagine. La condivisione avviene solo tramite il dialogo di sistema che apri attivamente. Quando avvii consapevolmente un backup Google Drive, i dati vengono trasferiti nell'area nascosta appDataFolder del tuo account Google Drive. L'app non può accedere ad altri file Drive. Puoi eliminare il backup Drive nell'app in qualsiasi momento."),
            ("Google Play: acquisto e valutazione", "ZahnTagebuch Pro è un acquisto in-app una tantum. Google Play tratta i dati di pagamento e dell'account; l'app memorizza solo lo stato dell'acquisto. Dopo il terzo dente registrato, l'app può aprire una volta la funzione di valutazione fornita da Google Play. L'app non trasmette dati dentali, di profilo o di backup tramite tale funzione."),
            ("Cancellazione dei dati", "Elimina singole registrazioni o profili dei bambini nell'app. Rimuovi tutti i dati locali disinstallando l'app o usando l'opzione per cancellare lo spazio di archiviazione di Android. Elimina un backup Drive nell'app o nel tuo account Google."),
        ],
        "pt": [
            ("Cópia local, partilha e Google Drive", "Podes exportar e importar os teus dados, incluindo fotografias, como ficheiro de cópia local ou gerar o esquema dentário como imagem. A partilha ocorre apenas através do diálogo do sistema que abres ativamente. Quando inicias conscientemente uma cópia no Google Drive, os dados são transferidos para a área oculta appDataFolder da tua conta Google Drive. A aplicação não pode aceder a outros ficheiros do Drive. Podes eliminar a cópia do Drive na aplicação a qualquer momento."),
            ("Google Play: compra e avaliação", "ZahnTagebuch Pro é uma compra única na aplicação. O Google Play trata os dados de pagamento e da conta; a aplicação guarda apenas o estado da compra. Após o terceiro dente registado, a aplicação pode abrir uma vez a função de avaliação fornecida pelo Google Play. A aplicação não transmite dados dentários, de perfil ou de cópia através dessa função."),
            ("Eliminação de dados", "Elimina registos individuais ou perfis de crianças na aplicação. Remove todos os dados locais desinstalando a aplicação ou usando a opção de limpar o armazenamento do Android. Elimina uma cópia do Drive na aplicação ou na tua conta Google."),
        ],
    },
    "babylog": {
        "de": [("Pro, Sicherung und Löschung", "BabyLog Pro wird einmalig über Google Play gekauft; Google verarbeitet Zahlungs- und Kontodaten. CSV/PDF-Exporte, lokale Sicherungen und das Teilen erfolgen nur auf deine aktive Auswahl. Lösche Einträge in der App oder alle lokalen Daten über Android." )],
        "en": [("Pro, backup and deletion", "BabyLog Pro is a one-time Google Play purchase; Google processes payment and account data. CSV/PDF exports, local backups and sharing occur only after your active choice. Delete records in the app or all local data through Android.")],
        "es": [("Pro, copias y eliminación", "BabyLog Pro se compra una sola vez mediante Google Play; Google trata los datos de pago y cuenta. Las exportaciones CSV/PDF, copias locales y el uso compartido solo se realizan tras tu elección activa. Elimina registros en la aplicación o todos los datos mediante Android.")],
        "fr": [("Pro, sauvegarde et suppression", "BabyLog Pro est un achat unique via Google Play ; Google traite les données de paiement et du compte. Les exports CSV/PDF, sauvegardes locales et partages ne sont effectués qu'après ton choix actif. Supprime les données dans l'application ou via Android.")],
        "it": [("Pro, backup e cancellazione", "BabyLog Pro è un acquisto una tantum tramite Google Play; Google tratta i dati di pagamento e dell'account. Esportazioni CSV/PDF, backup locali e condivisione avvengono solo dopo una tua scelta attiva. Elimina i dati nell'app o tramite Android.")],
        "pt": [("Pro, cópia e eliminação", "BabyLog Pro é uma compra única no Google Play; a Google trata os dados de pagamento e da conta. Exportações CSV/PDF, cópias locais e partilhas só ocorrem após a tua escolha ativa. Elimina registos na aplicação ou todos os dados através do Android.")],
    },
    "familybash": {
        "de": [("Spielinhalte, Drive und Löschung", "Neue Spielinhalte können höchstens täglich von GitHub abgerufen werden; dabei wird die IP-Adresse an GitHub übertragen. Die optionale Pro-Sicherung nutzt den appDataFolder deines Google-Drive-Kontos; Google verarbeitet Konto- und Zahlungsdaten. Lokale Daten und Sicherungen kannst du in der App beziehungsweise im Google-Konto löschen.")],
        "en": [("Game content, Drive and deletion", "New game content may be fetched from GitHub at most daily; GitHub receives the IP address. The optional Pro backup uses your Google Drive appDataFolder; Google processes account and payment data. Delete local data and backups in the app or Google account.")],
        "es": [("Contenido, Drive y eliminación", "El contenido nuevo puede consultarse en GitHub como máximo una vez al día; GitHub recibe la dirección IP. La copia Pro opcional utiliza el appDataFolder de Google Drive; Google trata datos de cuenta y pago. Elimina datos locales y copias en la aplicación o en tu cuenta de Google.")],
        "fr": [("Contenu, Drive et suppression", "Les nouveaux contenus peuvent être récupérés sur GitHub au maximum une fois par jour ; GitHub reçoit l'adresse IP. La sauvegarde Pro facultative utilise l'appDataFolder de Google Drive ; Google traite les données de compte et de paiement. Supprime les données dans l'application ou le compte Google.")],
        "it": [("Contenuti, Drive e cancellazione", "I nuovi contenuti possono essere recuperati da GitHub al massimo una volta al giorno; GitHub riceve l'indirizzo IP. Il backup Pro facoltativo usa l'appDataFolder di Google Drive; Google tratta dati dell'account e di pagamento. Elimina i dati nell'app o nell'account Google.")],
        "pt": [("Conteúdo, Drive e eliminação", "Novos conteúdos podem ser obtidos do GitHub no máximo uma vez por dia; o GitHub recebe o endereço IP. A cópia Pro opcional usa o appDataFolder do Google Drive; a Google trata dados de conta e pagamento. Elimina dados na aplicação ou na conta Google.")],
    },
    "nametrends": {
        "de": [("Datenupdate, Kauf und Löschung", "Aggregierte Namensdaten und Rechtstexte können höchstens täglich von GitHub aktualisiert werden; dabei wird die IP-Adresse an GitHub übertragen. NameTrends Pro ist ein einmaliger Google-Play-Kauf. Favoriten und Einstellungen löschst du in der App oder durch Deinstallation.")],
        "en": [("Data updates, purchase and deletion", "Aggregated name data and legal texts may be updated from GitHub at most daily; GitHub receives the IP address. NameTrends Pro is a one-time Google Play purchase. Delete favourites and settings in the app or by uninstalling.")],
        "es": [("Actualizaciones, compra y eliminación", "Los datos agregados de nombres y los textos legales pueden actualizarse desde GitHub como máximo una vez al día; GitHub recibe la IP. NameTrends Pro es una compra única en Google Play. Elimina favoritos y ajustes en la aplicación o desinstalándola.")],
        "fr": [("Mises à jour, achat et suppression", "Les données agrégées de prénoms et les textes légaux peuvent être mis à jour depuis GitHub au maximum une fois par jour ; GitHub reçoit l'adresse IP. NameTrends Pro est un achat unique Google Play. Supprime favoris et réglages dans l'application ou en la désinstallant.")],
        "it": [("Aggiornamenti, acquisto e cancellazione", "I dati aggregati sui nomi e i testi legali possono essere aggiornati da GitHub al massimo una volta al giorno; GitHub riceve l'indirizzo IP. NameTrends Pro è un acquisto una tantum su Google Play. Elimina preferiti e impostazioni nell'app o disinstallandola.")],
        "pt": [("Atualizações, compra e eliminação", "Os dados agregados de nomes e os textos legais podem ser atualizados a partir do GitHub no máximo uma vez por dia; o GitHub recebe o IP. NameTrends Pro é uma compra única no Google Play. Elimina favoritos e definições na aplicação ou desinstalando-a.")],
    },
    "scootrules": {
        "de": [("GitHub-Abrufe, externe Links und keine weiteren Datenfunktionen", "Länderregeln und Rechtstexte werden höchstens einmal innerhalb von 24 Stunden per HTTPS von öffentlichen GitHub-Quellen aktualisiert. Dabei erhält GitHub technisch bedingt die IP-Adresse. Öffnest du eine Quelle, einen Hinweis zu einer anderen App oder einen Rechtstext im Browser, startet die App nur auf deine Aktion eine externe Anwendung; ab dann gelten deren Datenschutzhinweise. Im aktuellen Funktionsumfang verarbeitet ScootRules keine Kinder- oder Gesundheitsdaten, keine Fotos oder Dateien, keine Benachrichtigungen, keine Google-Play-Käufe und keine Cloud-Backups. Es gibt kein Nutzerkonto sowie keine Analyse-, Werbe- oder Tracking-Dienste.")],
        "en": [("GitHub requests, external links and no further data functions", "Country rules and legal texts are updated via HTTPS from public GitHub sources at most once within 24 hours. GitHub receives the IP address for technical reasons. If you open a source, a reference to another app or a legal text in the browser, the app starts an external application only following your action; its privacy information then applies. In its current functionality, ScootRules does not process children's or health data, photos or files, notifications, Google Play purchases or cloud backups. There is no user account and no analytics, advertising or tracking services.")],
        "es": [("Consultas a GitHub, enlaces externos y ninguna otra función de datos", "Las normas de los países y los textos legales se actualizan mediante HTTPS desde fuentes públicas de GitHub como máximo una vez cada 24 horas. Por motivos técnicos, GitHub recibe la dirección IP. Si abres una fuente, una referencia a otra aplicación o un texto legal en el navegador, la aplicación solo inicia una aplicación externa tras tu acción; entonces se aplica su información de privacidad. En su funcionalidad actual, ScootRules no trata datos de menores ni de salud, fotos o archivos, notificaciones, compras de Google Play ni copias en la nube. No hay cuenta de usuario ni servicios de análisis, publicidad o seguimiento.")],
        "fr": [("Requêtes GitHub, liens externes et absence d'autres fonctions de données", "Les règles par pays et les textes juridiques sont mis à jour via HTTPS depuis des sources GitHub publiques au plus une fois toutes les 24 heures. GitHub reçoit l'adresse IP pour des raisons techniques. Si tu ouvres une source, une référence à une autre application ou un texte juridique dans le navigateur, l'application ne démarre une application externe qu'après ton action ; ses informations de confidentialité s'appliquent alors. Dans ses fonctions actuelles, ScootRules ne traite pas de données d'enfants ou de santé, de photos ou de fichiers, de notifications, d'achats Google Play ni de sauvegardes cloud. Il n'y a ni compte utilisateur ni service d'analyse, de publicité ou de suivi.")],
        "it": [("Richieste GitHub, link esterni e nessun'altra funzione sui dati", "Le regole per Paese e i testi legali vengono aggiornati tramite HTTPS da fonti GitHub pubbliche al massimo una volta ogni 24 ore. Per motivi tecnici GitHub riceve l'indirizzo IP. Se apri una fonte, un riferimento a un'altra app o un testo legale nel browser, l'app avvia un'applicazione esterna solo dopo la tua azione; si applicano quindi le relative informazioni sulla privacy. Nelle funzioni attuali ScootRules non tratta dati di minori o sanitari, foto o file, notifiche, acquisti Google Play o backup cloud. Non esistono account utente né servizi di analisi, pubblicità o tracciamento.")],
        "pt": [("Pedidos ao GitHub, links externos e ausência de outras funções de dados", "As regras por país e os textos legais são atualizados por HTTPS a partir de fontes públicas do GitHub no máximo uma vez a cada 24 horas. Por motivos técnicos, o GitHub recebe o endereço IP. Se abrires uma fonte, uma referência a outra aplicação ou um texto legal no navegador, a aplicação só inicia uma aplicação externa após a tua ação; aplicam-se então as respetivas informações de privacidade. Nas funções atuais, o ScootRules não trata dados de crianças ou de saúde, fotografias ou ficheiros, notificações, compras Google Play nem cópias na nuvem. Não existe conta de utilizador nem serviços de análise, publicidade ou rastreio.")],
    },
    "sleeplog": {
        "de": [("Export, Pro und Löschung", "PDF-, Druck- und JSON-Exporte werden lokal erstellt und nur über den von dir geöffneten Systemdialog geteilt. SleepLog Pro ist ein einmaliger Google-Play-Kauf; Google verarbeitet Zahlungs- und Kontodaten. Lösche Einträge in der App oder alle lokalen Daten über Android.")],
        "en": [("Export, Pro and deletion", "PDF, print and JSON exports are created locally and shared only through the system dialog you open. SleepLog Pro is a one-time Google Play purchase; Google processes payment and account data. Delete records in the app or all local data through Android.")],
        "es": [("Exportación, Pro y eliminación", "Las exportaciones PDF, impresión y JSON se crean localmente y solo se comparten mediante el diálogo del sistema que abres. SleepLog Pro es una compra única en Google Play; Google trata datos de pago y cuenta. Elimina registros en la aplicación o todos los datos mediante Android.")],
        "fr": [("Export, Pro et suppression", "Les exports PDF, impression et JSON sont créés en local et partagés uniquement via la boîte de dialogue système que tu ouvres. SleepLog Pro est un achat unique Google Play ; Google traite les données de paiement et du compte. Supprime les données dans l'application ou via Android.")],
        "it": [("Esportazione, Pro e cancellazione", "Le esportazioni PDF, stampa e JSON vengono create localmente e condivise solo tramite il dialogo di sistema che apri. SleepLog Pro è un acquisto una tantum su Google Play; Google tratta dati di pagamento e account. Elimina i dati nell'app o tramite Android.")],
        "pt": [("Exportação, Pro e eliminação", "As exportações PDF, impressão e JSON são criadas localmente e partilhadas apenas através do diálogo do sistema que abres. SleepLog Pro é uma compra única no Google Play; a Google trata dados de pagamento e conta. Elimina registos na aplicação ou todos os dados através do Android.")],
    },
}


SNACKBLOCKER_DATA = {
    "de": ("Lokale Gewohnheitsdaten", "SnackBlocker speichert den aktivierten Abend-Reminder und dessen Uhrzeit, Abend-Check-ins, Streaks, Kostenwerte, gewaehlte Ausloeser und einen freiwillig eingegebenen persoenlichen Grund ausschliesslich lokal auf deinem Geraet. Der freie Text und die Angaben koennen Rueckschluesse auf Essverhalten oder Wohlbefinden zulassen. Es gibt kein Nutzerkonto, keinen eigenen Server sowie keine Analyse-, Tracking- oder Werbe-SDKs."),
    "en": ("Local habit data", "SnackBlocker stores the enabled evening reminder and its time, evening check-ins, streaks, cost values, selected triggers and an optionally entered personal reason exclusively locally on your device. The free text and entries may allow conclusions about eating behaviour or well-being. There is no user account, no own server and no analytics, tracking or advertising SDKs."),
    "es": ("Datos locales de hábitos", "SnackBlocker guarda exclusivamente de forma local en tu dispositivo el recordatorio nocturno activado y su hora, los registros nocturnos, las rachas, los valores de coste, los desencadenantes seleccionados y un motivo personal introducido voluntariamente. El texto libre y las entradas pueden permitir deducir el comportamiento alimentario o el bienestar. No hay cuenta de usuario, servidor propio ni SDK de análisis, seguimiento o publicidad."),
    "fr": ("Données locales d'habitudes", "SnackBlocker conserve exclusivement en local sur ton appareil le rappel du soir activé et son heure, les bilans du soir, les séries, les valeurs de coût, les déclencheurs sélectionnés et un motif personnel saisi volontairement. Le texte libre et les saisies peuvent permettre de tirer des conclusions sur le comportement alimentaire ou le bien-être. Il n'y a pas de compte utilisateur, de serveur propre ni de SDK d'analyse, de suivi ou de publicité."),
    "it": ("Dati locali sulle abitudini", "SnackBlocker salva esclusivamente in locale sul tuo dispositivo il promemoria serale attivato e il relativo orario, i check-in serali, le serie, i valori di costo, i fattori scatenanti selezionati e un motivo personale inserito facoltativamente. Il testo libero e le voci possono consentire deduzioni sul comportamento alimentare o sul benessere. Non esistono account utente, server propri o SDK di analisi, tracciamento o pubblicità."),
    "pt": ("Dados locais de hábitos", "SnackBlocker guarda exclusivamente no teu dispositivo o lembrete noturno ativado e a respetiva hora, os registos noturnos, as sequências, os valores de custo, os gatilhos selecionados e um motivo pessoal introduzido voluntariamente. O texto livre e os registos podem permitir conclusões sobre o comportamento alimentar ou o bem-estar. Não existe conta de utilizador, servidor próprio nem SDK de análise, rastreio ou publicidade."),
}

SNACKBLOCKER_FEATURES = {
    "de": [("Benachrichtigungen", "Der Abend-Reminder wird vollständig lokal auf deinem Gerät geplant und ausgelöst. Es wird kein Push- oder Benachrichtigungsserver verwendet. Die Berechtigung kannst du jederzeit in den Android-Einstellungen widerrufen."), ("Löschung", "Unter Einstellungen > Deine Daten > Daten löschen kannst du Reminder, Check-ins, Auslöser, Kostenwerte, den persönlichen Grund und die lokal gespeicherten Rechtstexte entfernen. Die Deinstallation entfernt die App-Daten ebenfalls, soweit das Betriebssystem keine Sicherung wiederherstellt."), ("Abruf von Rechtstexten und externe Links", "Die App ruft zur Hintergrundaktualisierung der Rechtstexte höchstens einmal alle 24 Stunden JSON-Dateien von raw.githubusercontent.com ab. Dabei wird technisch bedingt deine IP-Adresse an GitHub übertragen. Es werden keine App-Inhalte oder Nutzungsprofile übermittelt. Ohne Internetverbindung bleiben Cache oder die mitgelieferten Fassungen verfügbar. Wenn du Im Browser öffnen wählst, wird die passende GitHub-Pages-Seite von scorparc.github.io in deinem Browser geöffnet.")],
    "en": [("Notifications", "The evening reminder is scheduled and triggered entirely locally on your device. No push or notification server is used. You can revoke the permission at any time in Android settings."), ("Deletion", "Under Settings > Your data > Delete data, you can remove reminders, check-ins, triggers, cost values, your personal reason and locally stored legal texts. Uninstalling also removes app data unless the operating system restores a backup."), ("Fetching legal texts and external links", "To update legal texts in the background, the app fetches JSON files from raw.githubusercontent.com at most once every 24 hours. This technically transmits your IP address to GitHub. No app content or usage profile is transmitted. Without an internet connection, the cache or bundled versions remain available. When you select Open in browser, the matching GitHub Pages page at scorparc.github.io opens in your browser.")],
    "es": [("Notificaciones", "El recordatorio nocturno se programa y activa completamente de forma local en tu dispositivo. No se utiliza ningún servidor push o de notificaciones. Puedes retirar el permiso en cualquier momento en los ajustes de Android."), ("Eliminación", "En Ajustes > Tus datos > Eliminar datos puedes eliminar recordatorios, registros, desencadenantes, valores de coste, tu motivo personal y los textos legales almacenados localmente. La desinstalación también elimina los datos de la aplicación, salvo que el sistema operativo restaure una copia."), ("Consulta de textos legales y enlaces externos", "Para actualizar los textos legales en segundo plano, la aplicación consulta archivos JSON de raw.githubusercontent.com como máximo una vez cada 24 horas. Esto transmite técnicamente tu dirección IP a GitHub. No se transmiten contenidos de la aplicación ni perfiles de uso. Sin conexión a Internet siguen disponibles la caché o las versiones incluidas. Al seleccionar Abrir en el navegador, se abre en tu navegador la página correspondiente de GitHub Pages en scorparc.github.io.")],
    "fr": [("Notifications", "Le rappel du soir est planifié et déclenché entièrement en local sur ton appareil. Aucun serveur push ou de notifications n'est utilisé. Tu peux retirer l'autorisation à tout moment dans les paramètres Android."), ("Suppression", "Sous Paramètres > Tes données > Supprimer les données, tu peux supprimer les rappels, bilans, déclencheurs, valeurs de coût, ton motif personnel et les textes légaux stockés localement. La désinstallation supprime également les données de l'application, sauf si le système restaure une sauvegarde."), ("Consultation des textes légaux et liens externes", "Pour mettre à jour les textes légaux en arrière-plan, l'application consulte des fichiers JSON sur raw.githubusercontent.com au maximum une fois toutes les 24 heures. Cette opération transmet techniquement ton adresse IP à GitHub. Aucun contenu de l'application ni profil d'utilisation n'est transmis. Sans connexion Internet, le cache ou les versions intégrées restent disponibles. Lorsque tu choisis Ouvrir dans le navigateur, la page GitHub Pages correspondante de scorparc.github.io s'ouvre dans ton navigateur.")],
    "it": [("Notifiche", "Il promemoria serale viene pianificato e attivato interamente in locale sul tuo dispositivo. Non viene utilizzato alcun server push o di notifiche. Puoi revocare l'autorizzazione in qualsiasi momento nelle impostazioni Android."), ("Cancellazione", "In Impostazioni > I tuoi dati > Elimina dati puoi rimuovere promemoria, check-in, fattori scatenanti, valori di costo, il tuo motivo personale e i testi legali memorizzati localmente. La disinstallazione rimuove a sua volta i dati dell'app, salvo il ripristino di un backup da parte del sistema operativo."), ("Recupero dei testi legali e link esterni", "Per aggiornare i testi legali in background, l'app recupera file JSON da raw.githubusercontent.com al massimo una volta ogni 24 ore. Ciò trasmette tecnicamente il tuo indirizzo IP a GitHub. Non vengono trasmessi contenuti dell'app né profili di utilizzo. Senza connessione Internet rimangono disponibili la cache o le versioni incluse. Quando selezioni Apri nel browser, nel browser si apre la pagina GitHub Pages corrispondente su scorparc.github.io.")],
    "pt": [("Notificações", "O lembrete noturno é agendado e acionado integralmente no teu dispositivo. Não é utilizado qualquer servidor push ou de notificações. Podes retirar a permissão a qualquer momento nas definições do Android."), ("Eliminação", "Em Definições > Os teus dados > Eliminar dados podes remover lembretes, registos, gatilhos, valores de custo, o teu motivo pessoal e os textos legais guardados localmente. A desinstalação também remove os dados da aplicação, salvo se o sistema operativo restaurar uma cópia."), ("Consulta dos textos legais e ligações externas", "Para atualizar os textos legais em segundo plano, a aplicação consulta ficheiros JSON de raw.githubusercontent.com no máximo uma vez a cada 24 horas. Isto transmite tecnicamente o teu endereço IP ao GitHub. Não são transmitidos conteúdos da aplicação nem perfis de utilização. Sem ligação à Internet, a cache ou as versões incluídas permanecem disponíveis. Ao selecionares Abrir no navegador, a página GitHub Pages correspondente em scorparc.github.io abre no teu navegador.")],
}

SNACKBLOCKER_RIGHTS = {
    "de": "Du hast nach der DSGVO insbesondere das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch sowie das Recht auf Beschwerde bei einer Datenschutzaufsichtsbehörde. Da die App-Daten grundsätzlich lokal bei dir liegen, kannst du sie in der App oder durch Löschen der App-Daten selbst entfernen.",
    "en": "Under the GDPR you have, in particular, the rights of access, rectification, erasure, restriction of processing, data portability and objection, as well as the right to lodge a complaint with a data protection supervisory authority. As app data is generally stored locally under your control, you can remove it in the app or by deleting the app data yourself.",
    "es": "Conforme al RGPD tienes, en particular, derecho de acceso, rectificación, supresión, limitación del tratamiento, portabilidad y oposición, así como derecho a presentar una reclamación ante una autoridad de control. Como los datos de la aplicación se guardan normalmente de forma local bajo tu control, puedes eliminarlos en la aplicación o borrando sus datos.",
    "fr": "Conformément au RGPD, tu disposes notamment des droits d'accès, de rectification, d'effacement, de limitation du traitement, de portabilité et d'opposition, ainsi que du droit d'introduire une réclamation auprès d'une autorité de contrôle. Les données de l'application étant généralement stockées localement sous ton contrôle, tu peux les supprimer dans l'application ou en effaçant ses données.",
    "it": "Ai sensi del GDPR hai in particolare diritto di accesso, rettifica, cancellazione, limitazione del trattamento, portabilità e opposizione, nonché il diritto di proporre reclamo a un'autorità di controllo. Poiché i dati dell'app sono generalmente memorizzati localmente sotto il tuo controllo, puoi rimuoverli nell'app o cancellandone i dati.",
    "pt": "Nos termos do RGPD tens, em particular, direito de acesso, retificação, apagamento, limitação do tratamento, portabilidade e oposição, bem como o direito de apresentar uma reclamação junto de uma autoridade de controlo. Como os dados da aplicação são geralmente guardados localmente sob o teu controlo, podes removê-los na aplicação ou eliminando os respetivos dados.",
}


PRIVACY_TITLES = {
    "de": "Datenschutzerklärung",
    "en": "Privacy Policy",
    "es": "Política de privacidad",
    "fr": "Politique de confidentialité",
    "it": "Informativa sulla privacy",
    "pt": "Política de privacidade",
}

STANDS = {
    "de": "8. August 2026",
    "en": "8 August 2026",
    "es": "8 de agosto de 2026",
    "fr": "8 août 2026",
    "it": "8 agosto 2026",
    "pt": "8 de agosto de 2026",
}

TRANSLATION_NOTES = {
    "de": "Die deutsche Fassung ist die rechtliche Masterfassung.",
    "en": "The German version is the legal master version.",
    "es": "La versión alemana es la versión jurídica principal.",
    "fr": "La version allemande est la version juridique de référence.",
    "it": "La versione tedesca è la versione giuridica di riferimento.",
    "pt": "A versão alemã é a versão jurídica de referência.",
}


def make_imprint(language: str) -> dict:
    item = IMPRINT[language]
    return {
        "schemaVersion": 1,
        "version": VERSION,
        "language": language,
        "title": item["title"],
        "updated": "2026-08-07",
        "sections": [
            {"heading": heading, "body": body}
            for heading, body in zip(item["headings"], item["bodies"])
        ],
    }


SCOOTRULES_SYNC = {
    "de": "Damit Impressum und Datenschutzerklärung aktuell bleiben, lädt die App die JSON-Fassungen ausschließlich von raw.githubusercontent.com höchstens einmal alle 24 Stunden und speichert sie lokal. Dabei wird technisch bedingt deine IP-Adresse an GitHub übertragen. Ohne Internetverbindung zeigt die App die mitgelieferten Fassungen. Wenn du „Im Browser öffnen“ auswählst, wird die entsprechende HTML-Fassung über GitHub Pages in einer externen Anwendung geöffnet. Der Abruf erfolgt in unserem berechtigten Interesse an aktuellen Pflichtinformationen (Art. 6 Abs. 1 lit. f DSGVO).",
    "en": "To keep the legal notice and privacy policy current, the app fetches the JSON versions only from raw.githubusercontent.com at most once every 24 hours and stores them locally. This technically transmits your IP address to GitHub. Without an internet connection, the versions bundled with the app are shown. If you select “Open in browser”, the matching HTML version is opened through GitHub Pages in an external application. The fetch is based on our legitimate interest in keeping mandatory information current (Art. 6(1)(f) GDPR).",
    "es": "Para mantener actualizado el aviso legal y la política de privacidad, la aplicación descarga las versiones JSON únicamente de raw.githubusercontent.com como máximo una vez cada 24 horas y las guarda localmente. Esto transmite técnicamente tu dirección IP a GitHub. Sin conexión a Internet se muestran las versiones incluidas en la aplicación. Si seleccionas «Abrir en el navegador», la versión HTML correspondiente se abre mediante GitHub Pages en una aplicación externa. La consulta se basa en nuestro interés legítimo por mantener actualizada la información obligatoria (art. 6, apdo. 1, letra f del RGPD).",
    "fr": "Pour maintenir à jour les mentions légales et la politique de confidentialité, l'application télécharge les versions JSON uniquement depuis raw.githubusercontent.com au maximum une fois toutes les 24 heures et les conserve localement. Cette opération transmet techniquement ton adresse IP à GitHub. Sans connexion Internet, les versions intégrées à l'application sont affichées. Si tu sélectionnes « Ouvrir dans le navigateur », la version HTML correspondante est ouverte via GitHub Pages dans une application externe. La consultation repose sur notre intérêt légitime à maintenir à jour les informations obligatoires (art. 6, par. 1, point f du RGPD).",
    "it": "Per mantenere aggiornati le note legali e l'informativa sulla privacy, l'app scarica le versioni JSON esclusivamente da raw.githubusercontent.com al massimo una volta ogni 24 ore e le conserva in locale. Tecnicamente ciò trasmette il tuo indirizzo IP a GitHub. Senza connessione Internet vengono mostrate le versioni incluse nell'app. Se selezioni « Apri nel browser », la corrispondente versione HTML viene aperta tramite GitHub Pages in un'applicazione esterna. Il recupero si basa sul nostro legittimo interesse a mantenere aggiornate le informazioni obbligatorie (art. 6, par. 1, lett. f GDPR).",
    "pt": "Para manter atualizados o aviso legal e a política de privacidade, a aplicação transfere as versões JSON apenas de raw.githubusercontent.com no máximo uma vez a cada 24 horas e guarda-as localmente. Tecnicamente, isto transmite o teu endereço IP ao GitHub. Sem ligação à Internet são apresentadas as versões incluídas na aplicação. Se selecionares « Abrir no navegador », a versão HTML correspondente é aberta através do GitHub Pages numa aplicação externa. A consulta baseia-se no nosso interesse legítimo em manter atualizada a informação obrigatória (art. 6.º, n.º 1, alínea f, do RGPD).",
}

# Rechte-Text für Apps ohne Google-Konto-/Backup-Funktion: statt eines Hinweises
# auf ein Google-Konto (den diese Apps gar nicht nutzen) verweist er auf die
# Anbieter freiwillig geöffneter externer Links. Genutzt von ScootRules und
# PlakettenAlarm.
LINK_ONLY_RIGHTS = {
    "de": "Du hast nach der DSGVO insbesondere das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch sowie das Recht auf Beschwerde bei einer Datenschutzaufsichtsbehörde. Da die App-Daten grundsätzlich lokal bei dir liegen, kannst du sie dort selbst einsehen, ändern oder löschen. Soweit externe Anbieter bei freiwillig geöffneten Links Daten verarbeiten, gelten deren Datenschutzhinweise.",
    "en": "Under the GDPR you have, in particular, the rights of access, rectification, erasure, restriction of processing, data portability and objection, as well as the right to lodge a complaint with a data protection supervisory authority. App data is generally stored locally under your control, so you can inspect, change or delete it there. Where external providers process data after you voluntarily open links, their privacy information applies.",
    "es": "Conforme al RGPD tienes, en particular, derecho de acceso, rectificación, supresión, limitación del tratamiento, portabilidad y oposición, así como derecho a presentar una reclamación ante una autoridad de control. Los datos de la aplicación se guardan normalmente de forma local bajo tu control, por lo que puedes consultarlos, modificarlos o eliminarlos allí. Cuando proveedores externos tratan datos tras abrir voluntariamente enlaces, se aplica su información de privacidad.",
    "fr": "En vertu du RGPD, tu disposes notamment des droits d'accès, de rectification, d'effacement, de limitation du traitement, de portabilité et d'opposition, ainsi que du droit d'introduire une réclamation auprès d'une autorité de contrôle. Les données de l'application sont généralement conservées localement sous ton contrôle ; tu peux donc les consulter, les modifier ou les supprimer. Lorsque des fournisseurs externes traitent des données après l'ouverture volontaire de liens, leurs informations de confidentialité s'appliquent.",
    "it": "Ai sensi del GDPR hai in particolare diritto di accesso, rettifica, cancellazione, limitazione del trattamento, portabilità e opposizione, nonché il diritto di proporre reclamo a un'autorità di controllo. I dati dell'app sono generalmente conservati localmente sotto il tuo controllo, quindi puoi consultarli, modificarli o eliminarli lì. Se fornitori esterni trattano dati dopo l'apertura volontaria di link, si applicano le loro informazioni sulla privacy.",
    "pt": "Nos termos do RGPD tens, em particular, direito de acesso, retificação, apagamento, limitação do tratamento, portabilidade e oposição, bem como o direito de apresentar uma reclamação junto de uma autoridade de controlo. Os dados da aplicação são geralmente guardados localmente sob o teu controlo, pelo que podes consultá-los, alterá-los ou eliminá-los aí. Quando fornecedores externos tratam dados depois de abrires links voluntariamente, aplicam-se as respetivas informações de privacidade.",
}


def make_privacy(app_slug: str, language: str) -> dict:
    # SleepLog's data flows require a reviewed, app-specific policy. Its JSON
    # is canonical; this builder only turns it into HTML and optional assets.
    if app_slug == "sleeplog":
        source = LEGAL / app_slug / f"datenschutz{suffix(language)}.json"
        document = json.loads(source.read_text(encoding="utf-8"))
        if document.get("language") != language:
            raise ValueError(f"{source}: unexpected language")
        return document
    common = COMMON[language]
    app_heading, app_body = (
        SNACKBLOCKER_DATA[language]
        if app_slug == "snackblocker"
        else APP_DATA[app_slug][language]
    )
    sections = [
        {"number": 1, "heading": common["controller_h"], "body": common["controller_b"]},
        {"number": 2, "heading": app_heading, "body": app_body},
    ]
    if app_slug == "snackblocker":
        sections.append(
            {"number": 3, "heading": common["notifications_h"], "body": common["notifications_b"]}
        )
    elif app_slug not in {"babylog", "familybash", "nametrends", "scootrules", "sleeplog"}:
        sections.extend(
            [
                {"number": 3, "heading": common["photos_h"], "body": common["photos_b"]},
                {"number": 4, "heading": common["notifications_h"], "body": common["notifications_b"]},
            ]
        )
    features = SNACKBLOCKER_FEATURES[language] if app_slug == "snackblocker" else FEATURES[app_slug][language]
    for number, (heading, body) in enumerate(features, len(sections) + 1):
        sections.append({"number": number, "heading": heading, "body": body})
    if app_slug not in {"plakettenalarm", "snackblocker"}:
        sync_body = SCOOTRULES_SYNC[language] if app_slug == "scootrules" else common["sync_b"]
        sections.append({"number": len(sections) + 1, "heading": common["sync_h"], "body": sync_body})
    rights_body = (
        SNACKBLOCKER_RIGHTS[language] if app_slug == "snackblocker"
        else LINK_ONLY_RIGHTS[language] if app_slug in {"scootrules", "plakettenalarm"}
        else common["rights_b"]
    )
    sections.extend(
        [
            {"number": len(sections) + 1, "heading": common["rights_h"], "body": rights_body},
            {"number": len(sections) + 2, "heading": common["changes_h"], "body": common["changes_b"]},
        ]
    )
    for index, item in enumerate(sections, 1):
        item["number"] = index
    return {
        "schemaVersion": 1,
        "version": APP_VERSIONS.get(app_slug, VERSION),
        "language": language,
        "title": PRIVACY_TITLES[language],
        "app": APPS[app_slug],
        "stand": STANDS[language],
        "sections": sections,
    }


def write_json(path: Path, document: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_html(path: Path, document: dict, kind: str) -> None:
    lang = document["language"]
    title = html.escape(document["title"])
    app = html.escape(document.get("app", ""))
    meta = f"{app} · " if app else ""
    meta += f"Stand: {html.escape(document.get('stand', document.get('updated', '')))}"
    rows = []
    for item in document["sections"]:
        heading = html.escape(item["heading"])
        body = html.escape(item["body"]).replace("\n", "<br>\n")
        rows.append(f"<h2>{heading}</h2>\n<p>{body}</p>")
    body = "\n".join(rows)
    stylesheet = "style.css" if path.parent == LEGAL else "../style.css"
    path.write_text(
        "<!doctype html>\n"
        f'<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="robots" content="index, follow">\n'
        f"<title>{title}</title>\n<link rel=\"stylesheet\" href=\"{stylesheet}\">\n"
        "</head>\n<body>\n"
        f"<h1>{title}</h1>\n<p class=\"meta\">{meta}</p>\n{body}\n"
        f'<p class="meta">{html.escape(TRANSLATION_NOTES[lang])}</p>\n'
        "</body>\n</html>\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", choices=APPS, help="Build one app's privacy texts only.")
    parser.add_argument(
        "--assets-dir",
        type=Path,
        help="Optional app assets/legal directory to receive the selected app's fallbacks.",
    )
    args = parser.parse_args()
    if args.assets_dir and not args.app:
        parser.error("--assets-dir requires --app")
    app_slugs = (args.app,) if args.app else APPS

    for language in LANGUAGES:
        if not args.app:
            imprint = make_imprint(language)
            imprint_name = f"impressum{suffix(language)}"
            write_json(LEGAL / f"{imprint_name}.json", imprint)
            write_html(LEGAL / f"{imprint_name}.html", imprint, "impressum")
        for app_slug in app_slugs:
            privacy = make_privacy(app_slug, language)
            folder = LEGAL / app_slug
            filename = f"datenschutz{suffix(language)}"
            write_json(folder / f"{filename}.json", privacy)
            write_html(folder / f"{filename}.html", privacy, "datenschutz")

    if args.assets_dir:
        args.assets_dir.mkdir(parents=True, exist_ok=True)
        for language in LANGUAGES:
            privacy_name = f"datenschutz{suffix(language)}.json"
            imprint_name = f"impressum{suffix(language)}.json"
            shutil.copy2(LEGAL / imprint_name, args.assets_dir / imprint_name)
            shutil.copy2(LEGAL / args.app / privacy_name, args.assets_dir / privacy_name)


if __name__ == "__main__":
    main()
