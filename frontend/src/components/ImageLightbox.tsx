import { useEffect } from "react";

/**
 * Vollbild-Overlay für ein einzelnes Bild in groß. Schließt per Klick auf den
 * Hintergrund, den Schließen-Button oder Escape.
 */
export default function ImageLightbox({
  src,
  alt,
  onClose,
}: {
  src: string;
  alt: string;
  onClose: () => void;
}) {
  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [onClose]);

  return (
    <div className="image-lightbox-backdrop" onClick={onClose}>
      <button
        type="button"
        className="image-lightbox-close"
        onClick={onClose}
        aria-label="Bild schließen"
      >
        ×
      </button>
      <img
        src={src}
        alt={alt}
        className="image-lightbox-image"
        onClick={(event) => event.stopPropagation()}
      />
    </div>
  );
}
