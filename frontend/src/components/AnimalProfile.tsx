import { useEffect } from "react";
import { markAnimalSeen } from "../api/animals";
import type { Animal } from "../types";

const REPRODUCTION_LABELS: Record<Animal["reproduction_mode"], string> = {
  egg_laying: "Eier legend",
  live_bearing: "Lebendgebärend",
};

const SOCIAL_LABELS: Record<Animal["social_behavior"], string> = {
  solitary: "Einzelgänger",
  herd: "Herdentier",
};

/**
 * Zeigt den Steckbrief eines Tiers und markiert es beim Anzeigen als gesehen.
 * Einziger Ort im Frontend, der POST /animals/{id}/seen auslöst ("Sehen = Sammeln",
 * siehe CONTEXT.md und ADR 0003) — genutzt von AnimalDetailPage, DailyAnimalPage
 * und DiscoverPage.
 */
export default function AnimalProfile({ animal }: { animal: Animal }) {
  useEffect(() => {
    markAnimalSeen(animal.id).catch(() => {
      // Best-effort: schlägt der Aufruf fehl, bleibt der Steckbrief trotzdem lesbar.
    });
  }, [animal.id]);

  return (
    <article className="animal-profile">
      <img src={animal.image_url} alt={animal.name_de} className="animal-profile-image" />
      <h2>{animal.name_de}</h2>
      <p className="animal-profile-scientific">{animal.name_scientific}</p>

      <dl className="animal-profile-facts">
        <dt>Lebensraum</dt>
        <dd>{animal.habitat}</dd>

        <dt>Gefährdungsstatus</dt>
        <dd>{animal.conservation_status}</dd>

        <dt>Fortpflanzung</dt>
        <dd>
          {REPRODUCTION_LABELS[animal.reproduction_mode]}, {animal.gestation_period}
        </dd>

        <dt>Nachkommen</dt>
        <dd>{animal.offspring_count}</dd>

        <dt>Ernährung</dt>
        <dd>{animal.diet}</dd>

        <dt>Natürliche Feinde</dt>
        <dd>{animal.natural_enemies}</dd>

        <dt>Sozialverhalten</dt>
        <dd>
          {SOCIAL_LABELS[animal.social_behavior]}
          {animal.group_size ? ` (Gruppengröße: ${animal.group_size})` : ""}
        </dd>

        <dt>Charakter</dt>
        <dd>{animal.character_traits}</dd>
      </dl>
    </article>
  );
}
