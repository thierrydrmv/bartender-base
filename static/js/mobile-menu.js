const menuButton = document.querySelector("#mobile-menu-button");
const mobileMenu = document.querySelector("#mobile-menu");
const openIcon = document.querySelector("#menu-open-icon");
const closeIcon = document.querySelector("#menu-close-icon");

if (menuButton && mobileMenu && openIcon && closeIcon) {
  const closeMenu = () => {
    mobileMenu.classList.add("hidden");
    openIcon.classList.remove("hidden");
    closeIcon.classList.add("hidden");

    menuButton.setAttribute("aria-expanded", "false");
    menuButton.setAttribute("aria-label", "Abrir menu");
  };

  const openMenu = () => {
    mobileMenu.classList.remove("hidden");
    openIcon.classList.add("hidden");
    closeIcon.classList.remove("hidden");

    menuButton.setAttribute("aria-expanded", "true");
    menuButton.setAttribute("aria-label", "Fechar menu");

    const firstLink = mobileMenu.querySelector("a");
    firstLink?.focus();
  };

  menuButton.addEventListener("click", () => {
    const isOpen = menuButton.getAttribute("aria-expanded") === "true";

    if (isOpen) {
      closeMenu();
    } else {
      openMenu();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeMenu();
      menuButton.focus();
    }
  });

  mobileMenu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeMenu);
  });
}