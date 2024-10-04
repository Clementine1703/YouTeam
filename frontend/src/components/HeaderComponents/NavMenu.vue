<script setup>
    defineProps({
        title:String,
        imageUrl:String
    })
</script>

<template>
    <div class="m-4 flex items-center gap-2 cursor-pointer group">
        <div class="border-2 border-nav-border-color rounded-xl group-hover:bg-white group-hover:border-white px-2 py-2 transition">
            <img :src="imageUrl" alt="">
        </div>
        <p class="text-white text-[18px]">{{title}}</p>
    </div>
</template>