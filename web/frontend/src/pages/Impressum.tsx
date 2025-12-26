import React from 'react';
import Card from '../components/Card';

const Impressum: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <h1 className="text-h1 font-bold text-neutral-900 mb-8">Impressum</h1>

      <Card>
        <div className="space-y-8">
          {/* Responsible Person */}
          <section>
            <h2 className="text-h2 font-bold text-neutral-900 mb-4">Verantwortlich für den Inhalt</h2>
            <p className="text-body text-neutral-700">
              Dr. Gernot Starke<br />
              Willi-Lauf Allee 43<br />
              50858 Köln<br />
              Deutschland
            </p>
          </section>

          {/* Educational Purpose */}
          <section>
            <h2 className="text-h2 font-bold text-neutral-900 mb-4">Zweck dieser Website</h2>
            <p className="text-body text-neutral-700">
              Diese Website ist eine <strong>Fallstudie zu didaktischen Zwecken bei der Ausbildung im Bereich Software-Architektur</strong>. 
              Sie dient ausschließlich zu Demonstrations- und Lehrzwecken und ist nicht für den produktiven Einsatz bestimmt.
            </p>
          </section>

          {/* GDPR Compliance - Data Processing */}
          <section>
            <h2 className="text-h2 font-bold text-neutral-900 mb-4">Datenschutzhinweise (DSGVO)</h2>
            
            <h3 className="text-h3 font-semibold text-neutral-800 mt-4 mb-2">Hosting und Auslieferung</h3>
            <p className="text-body text-neutral-700 mb-4">
              Diese Website wird über <strong>GitHub Pages</strong> und ggf. ein <strong>Content Delivery Network (CDN)</strong> ausgeliefert. 
              Beim Aufruf der Website werden folgende Daten automatisch erfasst und gespeichert:
            </p>
            <ul className="list-disc list-inside text-body text-neutral-700 space-y-2 ml-4">
              <li>IP-Adresse des zugreifenden Rechners</li>
              <li>Datum und Uhrzeit des Zugriffs</li>
              <li>Name und URL der abgerufenen Datei</li>
              <li>Übertragene Datenmenge</li>
              <li>Meldung über erfolgreichen Abruf</li>
              <li>Browsertyp und Browserversion</li>
              <li>Betriebssystem des Nutzers</li>
              <li>Referrer URL (zuvor besuchte Seite)</li>
            </ul>
            <p className="text-body text-neutral-700 mt-4">
              Diese Daten werden in den <strong>Server-Logs von GitHub</strong> gespeichert und dienen der Systemsicherheit, 
              der technischen Administration sowie der Optimierung des Angebots. Eine Zusammenführung dieser Daten mit anderen 
              Datenquellen wird nicht vorgenommen. Die Rechtsgrundlage für die Verarbeitung ist Art. 6 Abs. 1 lit. f DSGVO 
              (berechtigtes Interesse an der technischen Bereitstellung der Website).
            </p>

            <h3 className="text-h3 font-semibold text-neutral-800 mt-6 mb-2">Cookies</h3>
            <p className="text-body text-neutral-700">
              Diese Website kann <strong>Cookies</strong> verwenden, um die Funktionalität zu gewährleisten und das Nutzererlebnis zu verbessern. 
              Cookies sind kleine Textdateien, die auf Ihrem Endgerät gespeichert werden. Sie können Ihren Browser so einstellen, 
              dass er Sie über das Setzen von Cookies informiert und Sie dies im Einzelfall erlauben oder Cookies generell ausschließen können.
            </p>

            <h3 className="text-h3 font-semibold text-neutral-800 mt-6 mb-2">Ihre Rechte</h3>
            <p className="text-body text-neutral-700">
              Sie haben gemäß DSGVO folgende Rechte:
            </p>
            <ul className="list-disc list-inside text-body text-neutral-700 space-y-2 ml-4 mt-2">
              <li>Recht auf Auskunft über Ihre gespeicherten Daten (Art. 15 DSGVO)</li>
              <li>Recht auf Berichtigung unrichtiger Daten (Art. 16 DSGVO)</li>
              <li>Recht auf Löschung (Art. 17 DSGVO)</li>
              <li>Recht auf Einschränkung der Verarbeitung (Art. 18 DSGVO)</li>
              <li>Recht auf Datenübertragbarkeit (Art. 20 DSGVO)</li>
              <li>Recht auf Widerspruch (Art. 21 DSGVO)</li>
            </ul>
          </section>

          {/* Disclaimer */}
          <section>
            <h2 className="text-h2 font-bold text-neutral-900 mb-4">Haftungsausschluss</h2>
            
            <h3 className="text-h3 font-semibold text-neutral-800 mb-2">Keine Gewährleistung</h3>
            <p className="text-body text-neutral-700 mb-4">
              Der Autor übernimmt keinerlei Gewähr für die Aktualität, Korrektheit, Vollständigkeit oder Qualität 
              der bereitgestellten Informationen. Haftungsansprüche gegen den Autor, welche sich auf Schäden materieller 
              oder ideeller Art beziehen, die durch die Nutzung oder Nichtnutzung der dargebotenen Informationen bzw. 
              durch die Nutzung fehlerhafter und unvollständiger Informationen verursacht wurden, sind grundsätzlich 
              ausgeschlossen, sofern seitens des Autors kein nachweislich vorsätzliches oder grob fahrlässiges Verschulden vorliegt.
            </p>

            <h3 className="text-h3 font-semibold text-neutral-800 mb-2">Haftung für Links</h3>
            <p className="text-body text-neutral-700">
              Unser Angebot enthält Links zu externen Webseiten Dritter, auf deren Inhalte wir keinen Einfluss haben. 
              Deshalb können wir für diese fremden Inhalte auch keine Gewähr übernehmen. Für die Inhalte der verlinkten 
              Seiten ist stets der jeweilige Anbieter oder Betreiber der Seiten verantwortlich.
            </p>
          </section>

          {/* Copyright */}
          <section>
            <h2 className="text-h2 font-bold text-neutral-900 mb-4">Urheberrecht</h2>
            <p className="text-body text-neutral-700">
              Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen dem deutschen Urheberrecht. 
              Die Vervielfältigung, Bearbeitung, Verbreitung und jede Art der Verwertung außerhalb der Grenzen des Urheberrechtes 
              bedürfen der schriftlichen Zustimmung des jeweiligen Autors bzw. Erstellers.
            </p>
          </section>
        </div>
      </Card>
    </div>
  );
};

export default Impressum;
