<script setup>
import { ref } from 'vue';
import Header from './views/Header.vue';
import JoinTheTeam from './components/JoinTheTeam.vue';
import OurCom from './components/OurCom.vue';
import AboutCom from './components/AboutCom.vue';
import FooterCom from './components/FooterCom.vue';
import Registration from './components/Registration.vue';

const language = ref('ru');

const registrationRef = ref(null);

const components = {
  Header,
  JoinTheTeam,
  Registration
};

const openRegistrationMenu = () => {
  if (registrationRef.value) {
    registrationRef.value.showMenu();
  }
};
</script>

<template>
  <div class="wrapper bg-bg-color w-full flex justify-center  py-8">
    <div class="container w-4/5">
      <Header />
      <JoinTheTeam @registration="openRegistrationMenu" :language="language" />
      <OurCom @registration="openRegistrationMenu" :language="language" />
      <AboutCom @registration="openRegistrationMenu" :language="language" />
      <FooterCom @registration="openRegistrationMenu" :language="language" />
      <Registration ref="registrationRef" :language="language" />
      <!--  other components here-->
    </div>
  </div>
</template>