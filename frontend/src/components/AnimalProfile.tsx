import { useEffect, useState } from "react";
import { markAnimalSeen } from "../api/animals";
import ImageLightbox from "./ImageLightbox";
import type { Animal, RelationshipStatus } from "../types";

const REPRODUCTION_LABELS: Record<Animal["reproduction_mode"], string> = {
  egg_laying: "Eier legend",
  live_bearing: "Lebendgebärend",
};

const SOCIAL_LABELS: Record<Animal["social_life"], string> = {
  solitary: "Einzelgänger",
  herd: "Herdentier",
};

const RELATIONSHIP_STATUS_LABELS: Record<RelationshipStatus, string> = {
  monogam: "Monogam",
  wechselnde_liebhaber: "Wechselnde Liebhaber",
  harem: "Harem",
};

const UNBEKANNT = "Noch unbekannt";

/**
 * Zeigt den Steckbrief eines Tiers und markiert es beim Anzeigen als gesehen.
 * Einziger Ort im Frontend, der POST /animals/{id}/seen auslöst ("Sehen = Sammeln",
 * siehe CONTEXT.md und ADR 0003) — genutzt von AnimalDetailPage, DailyAnimalPage
 * und DiscoverPage.
 */
export default function AnimalProfile({ animal }: { animal: Animal }) {
  const [lightboxOpen, setLightboxOpen] = useState(false);

  useEffect(() => {
    markAnimalSeen(animal.id).catch(() => {
      // Best-effort: schlägt der Aufruf fehl, bleibt der Steckbrief trotzdem lesbar.
    });
  }, [animal.id]);

  return (
    <article className="animal-profile">
      <img
        src={animal.image_url}
        alt={animal.name_de}
        className="animal-profile-image"
        onClick={() => setLightboxOpen(true)}
      />
      {lightboxOpen && (
        <ImageLightbox
          src={animal.image_url}
          alt={animal.name_de}
          onClose={() => setLightboxOpen(false)}
        />
      )}
      <h2>{animal.name_de}</h2>
      <p className="animal-profile-scientific">{animal.name_scientific}</p>

      <dl className="animal-profile-facts">
        <dt>Zuhause</dt>
        <dd>{animal.home_turf}</dd>

        <dt>Gefährdungsstatus</dt>
        <dd>{animal.conservation_status}</dd>

        <dt>Fortpflanzung</dt>
        <dd>{REPRODUCTION_LABELS[animal.reproduction_mode]}</dd>

        <dt>Wartezeit aufs Baby</dt>
        <dd>{animal.baby_wait_time}</dd>

        <dt>Kinderschar</dt>
        <dd>{animal.offspring_brood}</dd>

        <dt>Lieblingsspeise</dt>
        <dd>{animal.favorite_food}</dd>

        <dt>Erzfeinde</dt>
        <dd>{animal.arch_enemies}</dd>

        <dt>Gesellschaftsleben</dt>
        <dd>
          {SOCIAL_LABELS[animal.social_life]}
          {animal.group_size ? ` (Gruppengröße: ${animal.group_size})` : ""}
        </dd>

        <dt>Persönlichkeit</dt>
        <dd>{animal.personality}</dd>

        <dt>Superkraft</dt>
        <dd>{animal.superpower ?? UNBEKANNT}</dd>

        <dt>Funfakt</dt>
        <dd>{animal.fun_fact ?? UNBEKANNT}</dd>

        <dt>Balzzeit</dt>
        <dd>{animal.mating_season ?? UNBEKANNT}</dd>

        <dt>Nestbau</dt>
        <dd>{animal.nest_building ?? UNBEKANNT}</dd>

        <dt>Tanz der Liebe</dt>
        <dd>{animal.courtship_dance ?? UNBEKANNT}</dd>

        <dt>Beziehungsstatus</dt>
        <dd>
          {animal.relationship_status
            ? RELATIONSHIP_STATUS_LABELS[animal.relationship_status]
            : UNBEKANNT}
        </dd>
      </dl>
    </article>
  );
}
