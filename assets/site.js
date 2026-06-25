const profile = {
  name: "Yedil Sarseke",
  initials: "YS",
  headline: "Building practical hardware, software, and automation projects.",
  summary:
    "Engineer focused on practical systems across hardware, embedded firmware, Python tools, C++ applications, and automation. I like building projects that are useful, testable, and well documented.",
  location: "Kazakhstan",
  focus: "Hardware, Python, C++, embedded systems",
  email: "yedil.sarseke@nu.edu.kz",
  contacts: [
    { label: "Email", value: "yedil.sarseke@nu.edu.kz", href: "mailto:yedil.sarseke@nu.edu.kz" },
    { label: "GitHub", value: "github.com/edoxa1", href: "https://github.com/edoxa1" },
    //{ label: "LinkedIn", value: "linkedin.com/in/your-profile", href: "https://www.linkedin.com/in/your-profile" }
  ]
};

const experience = [
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
];

const skills = [
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
];

const textTargets = document.querySelectorAll("[data-profile]");
textTargets.forEach((element) => {
  const key = element.dataset.profile;
  element.textContent = profile[key] || element.textContent;
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

const experienceList = document.querySelector("[data-experience-list]");
if (experienceList) {
  experienceList.innerHTML = experience
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

const skillsList = document.querySelector("[data-skills-list]");
if (skillsList) {
  skillsList.innerHTML = skills
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

const contactList = document.querySelector("[data-contact-list]");
if (contactList) {
  contactList.innerHTML = profile.contacts
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
