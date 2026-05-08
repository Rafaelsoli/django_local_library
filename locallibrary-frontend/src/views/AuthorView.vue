<script setup lang="ts">
import SidebarComponent from '../components/SidebarComponent.vue';

</script>

<template>
<SidebarComponent/>
<div class="page">
    <div class="page-wrapper">
        <div class="page-header d-print-none">
            <div class="container-xl">
                <div class="row g-2 align-items-center">
                    <div class="col">
                        <h1 class="page-title">Autores</h1>
                        <h4 class="page-subtitle">Autores existentes da biblioteca:</h4>
                    </div>
                </div>
            </div>
        </div>
        <div class="page-body">
            <div class="container-xl">
                <ul>
                    <li>Nome Sobrenome (data)</li>
                </ul>
            </div>
        </div>
    </div>
</div>
</template>

<style scoped></style>