<script setup>
import { ref } from "vue";
const comFeatures = [
  {
    imageUrl: "/ourComIcons/peoples-icon.png",
    title: "Fostering Teamwork",
    description:
      "Our platform fosters collaboration, creating a vibrant IT community where individuals connect through shared interests and skills. Diverse teams collaborate, share knowledge, and achieve better results.",
  },
  {
    imageUrl: "/ourComIcons/rochette.png",
    title: "Creating an Environment of Innovation",
    description:
      "Our community connects experienced professionals with aspiring entrepreneurs, fostering an innovative culture supporting groundbreaking projects and startups.",
  },
  {
    imageUrl: "/ourComIcons/featur-icon.png",
    title: "Accelerating Skill Development",
    description:
      "We provide resources for continuous learning, enabling users to enhance skills and expertise. Through workshops, discussions, and projects, members gain practical experience and accelerate professional growth.",
  },
];
</script>


<template>
  <div
    class="our_comynity flex items-center justify-center mt-[150px] flex-col"
  >
    <div class="join__title">
      <h1 class="join__title-text">Our Community Impact</h1>
      <p class="join__text">
        Fostering Collaboration, Accelerating Growth, and Inspiring Innovation
      </p>x
    </div>
    <div class="our_commynity_features grid grid-cols-2 pt-12">
      <div v-for="item in comFeatures" :key="item" class="py-8 border px-6 rounded-tl-[10px] border-description-color">
        <img :src="item.imageUrl" alt="featur-icon" />
        <h3 class="text-white text-xl mt-4 mb-4">{{item.title}}</h3>
        <p class="text-description-color text-sm">{{item.description}}</p>
      </div>
      <div class="py-8 border flex items-center gap-5 justify-center cursor-pointer px-6  border-description-color">
            <h3 class="text-white text-2xl mt-4 mb-4">Become a Member Today</h3>
            <img src="/ourComIcons/arrow-up.png" alt="featur-icon">
      </div>
    </div>
  </div>
</template>