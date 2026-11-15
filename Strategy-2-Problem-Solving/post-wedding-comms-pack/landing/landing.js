(function () {
  var pub = window.PWCP_LANDING || {};
  var loc = window.PWCP_LANDING_LOCAL || {};
  var cfg = {
    CONTACT_URL: String(loc.CONTACT_URL || pub.CONTACT_URL || "").trim(),
    WHATSAPP_E164: String(loc.WHATSAPP_E164 || pub.WHATSAPP_E164 || "").replace(/\D/g, ""),
    APP_URL: String(loc.APP_URL || pub.APP_URL || "").trim(),
  };

  var text = encodeURIComponent("ACCESS — Post-Wedding Comms Pack");
  var waHref = cfg.WHATSAPP_E164
    ? "https://wa.me/" + cfg.WHATSAPP_E164 + "?text=" + text
    : "";

  // Prefer non-phone public contact (Form / mailto / IG) over WhatsApp number in repo.
  var accessHref = cfg.CONTACT_URL || waHref || "";

  var waLink = document.getElementById("ctaWhatsApp");
  var primary = document.getElementById("ctaPrimary");
  var appLink = document.getElementById("ctaApp");
  var hint = document.getElementById("waHint");

  if (primary) {
    if (accessHref) {
      primary.href = accessHref;
    } else {
      primary.href = "#access";
    }
  }

  if (waLink) {
    if (cfg.CONTACT_URL) {
      waLink.href = cfg.CONTACT_URL;
      waLink.textContent = "Request access";
    } else if (waHref) {
      waLink.href = waHref;
      waLink.textContent = "DM WhatsApp — ACCESS";
    } else {
      waLink.href = "#access";
      waLink.classList.add("is-disabled");
      waLink.setAttribute("aria-disabled", "true");
      waLink.textContent = "Set CONTACT_URL (no phone in repo)";
    }
  }

  if (hint) {
    if (cfg.CONTACT_URL || cfg.WHATSAPP_E164) {
      hint.hidden = true;
    } else {
      hint.hidden = false;
      hint.innerHTML =
        "Do <strong>not</strong> put your phone in git. Set <code>CONTACT_URL</code> in <code>config.js</code> " +
        "(Google Form / mailto / IG), or use gitignored <code>config.local.js</code> for local WhatsApp tests only.";
    }
  }

  if (appLink) {
    if (cfg.APP_URL) {
      appLink.href = cfg.APP_URL;
      appLink.textContent = "Open the app";
      appLink.classList.remove("is-disabled");
      appLink.removeAttribute("aria-disabled");
      appLink.removeAttribute("title");
    } else {
      appLink.href = "#access";
      appLink.classList.add("is-disabled");
      appLink.setAttribute("aria-disabled", "true");
      appLink.title = "Set APP_URL after Streamlit Cloud deploy (still no phone needed)";
    }
  }
})();
