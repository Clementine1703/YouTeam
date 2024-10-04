<script setup>
import NavMenu from "../components/HeaderComponents/NavMenu.vue";

import { ref } from "vue";
const itDomains = ref([
  {
    title: "Frontend Development",
    imageUrl: "/domain-icons/domain-icon-front.png",
  },

  {
    title: "Backend Development",
    imageUrl: "/domain-icons/domain-icon-backend.png",
  },
  {
    title: "Machine Learning",
    imageUrl: "/domain-icons/domain-icon-brain.png",
  },
  {
    title: "Data Science",
    imageUrl: "/domain-icons/domain-icon-datasience.png",
  },
  {
    title: "Cybersecurity",
    imageUrl: "/domain-icons/domain-icon-cyber.png",
  },
  {
    title: "IoT",
    imageUrl: "/domain-icons/domain-icon-systemdev.png",
  },
  {
    title: "Cloud computing",
    imageUrl: "/domain-icons/domain-icon-cloud.png",
  },
  {
    title: "Mobile Development",
    imageUrl: "/domain-icons/domain-icon-mobile.png",
  },
  {
    title: "DevOps",
    imageUrl: "/domain-icons/domain-icon-devops.png",
  },
  {
    title: "Blockchain",
    imageUrl: "/domain-icons/domain-icon-blockchain.png",
  },
  {
    title: "System Developments",
    imageUrl: "/domain-icons/domain-icon-systemdev.png",
  },
  {
    title: "Design",
    imageUrl: "/domain-icons/domain-icon-desing.png",
  },
]);
const projectPan = ref([
  {
    title: "All Projects",
    imageUrl: "/projectsIcons/folder.png",
  },
  {
    title: "Featured Projects",
    imageUrl: "/projectsIcons/star.png",
  },
  {
    title: "Create Project",
    imageUrl: "/projectsIcons/idea.png",
  },
  {
    title: "Upcoming Projects",
    imageUrl: "/projectsIcons/date.png",
  },
  {
    title: "My Project",
    imageUrl: "/projectsIcons/back.png",
  },
  {
    title: "Project Managment",
    imageUrl: "/projectsIcons/managment.png",
  },
]);
const communityPan = ref([
  {
    title: "Announcements",
    imageUrl: "/comunityIcons/communiti-icon1.png",
  },
  {
    title: "Mentorship",
    imageUrl: "/comunityIcons/communiti-icon2.png",
  },
  {
    title: "Events",
    imageUrl: "/comunityIcons/communiti-icon3.png",
  },
  {
    title: "Forums",
    imageUrl: "/comunityIcons/communiti-icon4.png",
  },
]);
const startupHubPan = ref([
  {
    title: "Incubator Programs",
    imageUrl: "/startupHubIcons/startuphub-icon1.png",
  },
  {
    title: "About",
    imageUrl: "/startupHubIcons/startuphub-icon2.png",
  },
  {
    title: "Funding",
    imageUrl: "/startupHubIcons/startuphub-icon3.png",
  },
]);
const isOpen = ref(false);
const isOpen2 = ref(false);
const isOpen3 = ref(false);
const isOpen4 = ref(false);
const isOpen5 = ref(false);

const menus = [isOpen, isOpen2, isOpen3, isOpen4, isOpen5];
const openMenu = (index) => {
  menus.forEach((menu, i) => {
    menu.value = i === index ? !menu.value : false;
  });
};


</script>

<template>
  <header
    class="border border-nav-border-color py-8 mt-8 flex justify-around items-center rounded-2xl"
  >
    <div>
      <h1 class="text-white text-3xl max-xl:text-xl">YouTeam</h1>
    </div>
    <div>
      <ul class="text-nav-text-color list-none flex gap-8 max-[1370px]:gap-3">
        <li
          class="flex items-center px-4 py-1 rounded-2xl cursor-pointer text-[18px] hover:bg-nav-item-hovered-bg hover:text-white"
        >
          Home
        </li>
        <div>
          <li
            @click="openMenu(0)"
            class="relative flex flex-col items-center px-4 py-1 rounded-2xl cursor-pointer text-[18px] hover:bg-nav-item-hovered-bg"
          >
            <p class="flex hover:text-white">
              It Domains
              <img
                :src="isOpen ? '/Icon-scaled-up.png' : '/icon-scaled.png'"
                class="hover:icon-white"
                alt="icon"
              />
            </p>
          </li>
          <div
            v-if="isOpen"
            class="absolute bg-nav-menu-bg rounded-xl px-6 py-4 grid grid-cols-2 gap-x-8 mt-4"
          >
            <NavMenu
              v-for="item in itDomains"
              :key="item"
              :title="item.title"
              :imageUrl="item.imageUrl"
            />
          </div>
        </div>

        <div>
          <li
            @click="openMenu(1)"
            class="relative flex flex-col items-center px-4 py-1 rounded-2xl cursor-pointer text-[18px] hover:bg-nav-item-hovered-bg"
          >
            <p class="flex hover:text-white">
              Projects
              <img
                :src="isOpen2 ? '/Icon-scaled-up.png' : '/icon-scaled.png'"
                class="hover:icon-white"
                alt="icon"
              />
            </p>
          </li>
          <div
            v-if="isOpen2"
            class="absolute bg-nav-menu-bg rounded-xl px-6 py-4 grid  gap-x-8 mt-4"
          >
            <NavMenu
              v-for="item in projectPan"
              :key="item"
              :title="item.title"
              :imageUrl="item.imageUrl"
            />
          </div>
        </div>

        <div>
          <li
            @click="openMenu(2)"
            class="relative flex flex-col items-center px-4 py-1 rounded-2xl cursor-pointer text-[18px] hover:bg-nav-item-hovered-bg"
          >
            <p class="flex hover:text-white">
              Community
              <img
                :src="isOpen3 ? '/Icon-scaled-up.png' : '/icon-scaled.png'"
                class="hover:icon-white"
                alt="icon"
              />
            </p>
          </li>
          <div
            v-if="isOpen3"
            class="absolute bg-nav-menu-bg rounded-xl px-6 py-4 grid gap-x-8 mt-4"
          >
            <NavMenu
              v-for="item in communityPan"
              :key="item"
              :title="item.title"
              :imageUrl="item.imageUrl"
            />
          </div>
        </div>

        <div>
          <li
            @click="openMenu(3)"
            class="relative flex flex-col items-center px-4 py-1 rounded-2xl cursor-pointer text-[18px] hover:bg-nav-item-hovered-bg"
          >
            <p class="flex hover:text-white">
              Startup Hub
              <img
                :src="isOpen4 ? '/Icon-scaled-up.png' : '/icon-scaled.png'"
                class="hover:icon-white"
                alt="icon"
              />
            </p>
          </li>
          <div
            v-if="isOpen4"
            class="absolute bg-nav-menu-bg rounded-xl px-6 py-4 grid gap-x-8 mt-4"
          >
            <NavMenu
              v-for="item in startupHubPan"
              :key="item"
              :title="item.title"
              :imageUrl="item.imageUrl"
            />
          </div>
        </div>
      </ul>
    </div>
    <div class="flex items-center gap-4">
      <select class="bg-bg-color text-white border-2  border-nav-text-color rounded-[7px] py-1 px-1 outline-none">
        <option>EN</option>
        <option>RU</option>

      </select>
      <div class="cursor-pointer" ><img src="/icon-coll.png" alt="nav-icon-btn" /></div>
      <div class="cursor-pointer" ><img src="/icon-search.png" alt="nav-icon-btn" /></div>
      <div class="cursor-pointer" ><img src="/icon-user.png" alt="nav-icon-btn" /></div>
    </div>
  </header>
</template>

<style >
.icon-white {
  filter: invert(100%) brightness(100%) contrast(100%);
}
</style>