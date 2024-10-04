/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', "./src/**/*.{vue,html,js}"],
  theme: {
    extend: {
      colors:{
        "bg-color":"#080808",
        "nav-text-color":"#A1A1A1",
        "nav-menu-bg":"#1F1F1F",
        "nav-border-color":"#5D5D62",
        "nav-item-hovered-bg":"#1F1F1F",
        "description-color":"#7F7F7F"
      }
    },
  },
  plugins: [],
}

