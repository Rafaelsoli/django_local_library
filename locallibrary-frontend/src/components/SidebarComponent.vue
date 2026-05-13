<script setup lang="ts">
import { RouterLink } from 'vue-router'
import axios from 'axios';
import { ref } from 'vue';
const name = ref("");

// const isAuthenticated = async () => {
//   try {
//     const response = await axios.get('/me')
//     name.value = response.data.username;
//   } catch (error) {
//     console.error('Erro ao verificar status de autenticação:', error);
//     return false;
//   }
// }
</script>

<template>
<!-- Sidebar -->
  <aside class="navbar navbar-vertical navbar-expand-sm position-absolute" data-bs-theme="dark">
    <div class="container-fluid">
      <button class="navbar-toggler" type="button">
        <span class="navbar-toggler-icon"></span>
      </button>
      <h1 class="navbar-brand navbar-brand-autodark">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-book">
            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
            <path d="M3 19a9 9 0 0 1 9 0a9 9 0 0 1 9 0" />
            <path d="M3 6a9 9 0 0 1 9 0a9 9 0 0 1 9 0" />
            <path d="M3 6l0 13" />
            <path d="M12 6l0 13" />
            <path d="M21 6l0 13" />
        </svg>
        Local Library
      </h1>
      <div class="collapse navbar-collapse" id="sidebar-menu">
        <ul class="navbar-nav pt-lg-3">
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'Home' }">
              <span class="nav-link-title"> 
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-home">
                    <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                    <path d="M5 12l-2 0l9 -9l9 9l-2 0" />
                    <path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-7" />
                    <path d="M9 21v-6a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v6" />
                </svg>
                Home 
              </span>
            </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'Books' }">
              <span class="nav-link-title">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-books">    
                    <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                    <path d="M5 5a1 1 0 0 1 1 -1h2a1 1 0 0 1 1 1v14a1 1 0 0 1 -1 1h-2a1 1 0 0 1 -1 -1l0 -14" />
                    <path d="M9 5a1 1 0 0 1 1 -1h2a1 1 0 0 1 1 1v14a1 1 0 0 1 -1 1h-2a1 1 0 0 1 -1 -1l0 -14" />
                    <path d="M5 8h4" />
                    <path d="M9 16h4" />
                    <path d="M13.803 4.56l2.184 -.53c.562 -.135 1.133 .19 1.282 .732l3.695 13.418a1.02 1.02 0 0 1 -.634 1.219l-.133 .041l-2.184 .53c-.562 .135 -1.133 -.19 -1.282 -.732l-3.695 -13.418a1.02 1.02 0 0 1 .634 -1.219l.133 -.041" />
                    <path d="M14 9l4 -1" />
                    <path d="M16 16l3.923 -.98" />
                </svg> 
                Livros
              </span>
            </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'Authors' }">
              <span class="nav-link-title">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-feather">
                    <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                    <path d="M4 20l10 -10m0 -5v5h5m-9 -1v5h5m-9 -1v5h5m-5 -5l4 -4l4 -4" />
                    <path d="M19 10c.638 -.636 1 -1.515 1 -2.486a3.515 3.515 0 0 0 -3.517 -3.514c-.97 0 -1.847 .367 -2.483 1m-3 13l4 -4l4 -4" />
                </svg> 
                Autores 
              </span>
            </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'Login' }">
              <span class="nav-link-title"> 
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-login">
                    <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                    <path d="M15 8v-2a2 2 0 0 0 -2 -2h-7a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h7a2 2 0 0 0 2 -2v-2" />
                    <path d="M21 12h-13l3 -3" />
                    <path d="M11 15l-3 -3" />
                </svg>
                Login 
              </span>
            </RouterLink>
          </li>

     <!-- <li class="nav-item" v-if="!isAuthenticated">
            <RouterLink class="nav-link" :to="{ name: 'Alugados' }">
              <span class="nav-link-title"> 
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-login">
                    <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                    <path d="M15 8v-2a2 2 0 0 0 -2 -2h-7a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h7a2 2 0 0 0 2 -2v-2" />
                    <path d="M21 12h-13l3 -3" />
                    <path d="M11 15l-3 -3" />
                </svg>
                Meus Alugados 
              </span>
            </RouterLink>
          </li> 
          <li class="nav-item">
            <RouterLink class="nav-link" :to="{ name: 'TodosAlugados' }">
              <span class="nav-link-title"> 
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-login">
                    <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                    <path d="M15 8v-2a2 2 0 0 0 -2 -2h-7a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h7a2 2 0 0 0 2 -2v-2" />
                    <path d="M21 12h-13l3 -3" />
                    <path d="M11 15l-3 -3" />
                </svg>
                Todos Alugados 
              </span>
            </RouterLink>
          </li> -->
        </ul>
      </div>
    </div>
  </aside>
</template>

<style scoped>

</style>

