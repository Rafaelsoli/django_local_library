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
                        <h1>Nome: (nome do autor aq)</h1>
                        <h4 class="page-subtitle">Data de nascimento: (data de nascimento do autor aq)</h4>
                        <h4 class="page-subtitle">Data de falecimento: (data de falecimento do autor aq)</h4>
                    </div>
                </div>
            </div>
        </div>
        <div class="page-body">
            <div class="container-xl">
                <div>
                    <h2>Livros</h2>
                    <ul>
                        <h3>Título: (titulo do livro aq)</h3>
                        <p>Descrição: (descrição do livro aq)</p>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<style scoped></style>