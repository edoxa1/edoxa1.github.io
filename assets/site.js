const content = {
  en: {
    pageTitle: "Yedil Sarseke | Engineering Portfolio",
    pageDescription:
      "Engineering portfolio showcasing hardware, Python, C++, embedded systems, automation, and software projects.",
    profile: {
      name: "Yedil Sarseke",
      initials: "YS",
      headline: "Building practical hardware, software, and automation projects.",
      summary:
        "Engineer focused on practical systems across hardware, embedded firmware, Python tools, C++ applications, and automation. I like building projects that are useful, testable, and well documented.",
      location: "Kazakhstan",
      focus: "Hardware, Python, C++, embedded systems",
      email: "yedil.sarseke@nu.edu.kz"
    },
    contacts: [
      { label: "Email", value: "yedil.sarseke@nu.edu.kz", href: "mailto:yedil.sarseke@nu.edu.kz" },
      { label: "GitHub", value: "github.com/edoxa1", href: "https://github.com/edoxa1" }
    ],
    experience: [
      {
        role: "Firmware Engineer",
        company: "Artisan Education",
        period: "Jan. 2026 - May 2026",
        details:
          "Developed a modular, beginner-friendly library for custom PCB sensors, enabling middle and high school students to build and integrate hardware projects easily."
      },
      {
        role: "Hardware Engineer",
        company: "Kashgari.kz",
        period: "Aug. 2025 - Oct. 2025",
        details:
          "R&D of hardware-based projects. Manufactured 3 prototypes of smart watches based on ESP32 with custom 3D printed enclosure. Developed firmware for wireless data extraction from internal sensors."
      }
    ],
    skills: [
      {
        title: "Engineering",
        items: ["3D printing", "Rapid prototyping", "PCB layout", "Power electronics", "Signal measurement"]
      },
      {
        title: "Software",
        items: ["Python", "C++ development", "Automation tools", "Data processing", "Testing"]
      },
      {
        title: "Embedded",
        items: ["C/C++ firmware", "ESP32/RP2040", "PlatformIO", "I2C/SPI/UART", "Debugging"]
      }
    ]
  },
  ru: {
    pageTitle: "Yedil Sarseke | Инженерное портфолио",
    pageDescription:
      "Инженерное портфолио с проектами по железу, Python, C++, встраиваемым системам, автоматизации и разработке ПО.",
    profile: {
      name: "Yedil Sarseke",
      initials: "YS",
      headline: "Создаю практичные проекты в железе, софте и автоматизации.",
      summary:
        "Инженер, сфокусированный на практических системах: железо, встроенная прошивка, инструменты на Python, приложения на C++ и автоматизация. Мне нравятся проекты, которые полезны, проверяемы и хорошо задокументированы.",
      location: "Казахстан",
      focus: "Железо, Python, C++, встроенные системы",
      email: "yedil.sarseke@nu.edu.kz"
    },
    contacts: [
      { label: "Почта", value: "yedil.sarseke@nu.edu.kz", href: "mailto:yedil.sarseke@nu.edu.kz" },
      { label: "GitHub", value: "github.com/edoxa1", href: "https://github.com/edoxa1" }
    ],
    experience: [
      {
        role: "Firmware Engineer",
        company: "Artisan Education",
        period: "янв. 2026 - май 2026",
        details:
          "Разработал модульную и понятную библиотеку для кастомных PCB-сенсоров, чтобы ученики средней и старшей школы могли проще собирать и интегрировать аппаратные проекты."
      },
      {
        role: "Hardware Engineer",
        company: "Kashgari.kz",
        period: "авг. 2025 - окт. 2025",
        details:
          "Занимался R&D аппаратных проектов. Изготовил 3 прототипа умных часов на базе ESP32 с кастомным 3D-печатным корпусом. Разработал прошивку для беспроводного снятия данных со встроенных сенсоров."
      }
    ],
    skills: [
      {
        title: "Инженерия",
        items: ["3D-печать", "Быстрое прототипирование", "Разводка PCB", "Измерение сигналов"]
      },
      {
        title: "Software",
        items: ["Python", "Разработка на C++", "Инструменты автоматизации", "Обработка данных"]
      },
      {
        title: "Embedded",
        items: ["Прошивка на C/C++", "ESP32/RP2040", "PlatformIO", "I2C/SPI/UART", "Отладка"]
      }
    ]
  }
};

const supportedLanguages = ["en", "ru"];
const storageKey = "site-language";

function getStoredLanguage() {
  try {
    const stored = window.localStorage.getItem(storageKey);
    if (supportedLanguages.includes(stored)) {
      return stored;
    }
  } catch (error) {
    return null;
  }

  return null;
}

function persistLanguage(language) {
  try {
    window.localStorage.setItem(storageKey, language);
  } catch (error) {
    return;
  }
}

function updateLocalizedText(language) {
  document.querySelectorAll("[data-i18n-en]").forEach((element) => {
    const value = language === "ru" ? element.dataset.i18nRu : element.dataset.i18nEn;
    if (typeof value === "string") {
      element.textContent = value;
    }
  });

  document.querySelectorAll("[data-i18n-aria-label-en]").forEach((element) => {
    const value = language === "ru" ? element.dataset.i18nAriaLabelRu : element.dataset.i18nAriaLabelEn;
    if (typeof value === "string") {
      element.setAttribute("aria-label", value);
    }
  });

  document.querySelectorAll("[data-i18n-alt-en]").forEach((element) => {
    const value = language === "ru" ? element.dataset.i18nAltRu : element.dataset.i18nAltEn;
    if (typeof value === "string") {
      element.setAttribute("alt", value);
    }
  });
}

function updatePageMeta(language) {
  const body = document.body;
  const title = language === "ru" ? body.dataset.pageTitleRu : body.dataset.pageTitleEn;
  const description = language === "ru" ? body.dataset.pageDescriptionRu : body.dataset.pageDescriptionEn;

  if (title) {
    document.title = title;
  }

  const metaDescription = document.querySelector('meta[name="description"]');
  if (metaDescription && description) {
    metaDescription.setAttribute("content", description);
  }
}

function updateProfile(language) {
  const profile = content[language].profile;

  document.querySelectorAll("[data-profile]").forEach((element) => {
    const key = element.dataset.profile;
    if (profile[key]) {
      element.textContent = profile[key];
    }
  });

  const emailLink = document.querySelector("[data-profile-link='email']");
  if (emailLink) {
    emailLink.href = `mailto:${profile.email}`;
    emailLink.textContent = profile.email;
  }

  const photoInitials = document.querySelector(".profile-photo span");
  if (photoInitials) {
    photoInitials.textContent = profile.initials;
  }
}

function renderExperience(language) {
  const experienceList = document.querySelector("[data-experience-list]");
  if (!experienceList) {
    return;
  }

  experienceList.innerHTML = content[language].experience
    .map(
      (item) => `
        <article class="timeline-item">
          <div class="timeline-meta">${item.period}</div>
          <div class="timeline-body">
            <h3>${item.role} · ${item.company}</h3>
            <p>${item.details}</p>
          </div>
        </article>
      `
    )
    .join("");
}

function renderSkills(language) {
  const skillsList = document.querySelector("[data-skills-list]");
  if (!skillsList) {
    return;
  }

  skillsList.innerHTML = content[language].skills
    .map(
      (group) => `
        <article class="skill-group">
          <h3>${group.title}</h3>
          <ul>
            ${group.items.map((item) => `<li>${item}</li>`).join("")}
          </ul>
        </article>
      `
    )
    .join("");
}

function renderContacts(language) {
  const contactList = document.querySelector("[data-contact-list]");
  if (!contactList) {
    return;
  }

  contactList.innerHTML = content[language].contacts
    .map(
      (contact) => `
        <a href="${contact.href}" target="${contact.href.startsWith("mailto:") ? "_self" : "_blank"}" rel="noreferrer">
          ${contact.value}
          <span>${contact.label}</span>
        </a>
      `
    )
    .join("");
}

function updateLanguageContent(language) {
  document.querySelectorAll("[data-lang-content]").forEach((element) => {
    element.hidden = element.dataset.langContent !== language;
  });
}

function syncLanguageControls(language) {
  document.querySelectorAll("[data-language-select]").forEach((select) => {
    if (select.value !== language) {
      select.value = language;
    }
  });
}

function applyLanguage(language) {
  const selectedLanguage = supportedLanguages.includes(language) ? language : "en";

  document.documentElement.lang = selectedLanguage;
  persistLanguage(selectedLanguage);
  syncLanguageControls(selectedLanguage);
  updatePageMeta(selectedLanguage);
  updateLocalizedText(selectedLanguage);
  updateProfile(selectedLanguage);
  renderExperience(selectedLanguage);
  renderSkills(selectedLanguage);
  renderContacts(selectedLanguage);
  updateLanguageContent(selectedLanguage);
}

const initialLanguage = getStoredLanguage() || "en";

document.querySelectorAll("[data-language-select]").forEach((select) => {
  select.addEventListener("change", (event) => {
    applyLanguage(event.target.value);
  });
});

applyLanguage(initialLanguage);
