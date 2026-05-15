<script setup lang="ts">
import { RouterLink } from 'vue-router'
import axios from 'axios';
import { onMounted, ref } from 'vue';
const name = ref("");
const isAdmin = ref("");
const estaAutenticado = async () => {
  try {
    const response = await axios.get('/me');
    if (response.data.authenticated) {
      name.value = response.data.username;
      isAdmin.value = response.data.is_admin;
    } else {
      name.value = "";
      isAdmin.value = "";
    }
  } catch (error) {
    name.value = "";
    isAdmin.value = "";
    console.error('Usuário não autenticado');
  }
}

const logout = async () => {
  try {
    await axios.post('/logout');
    name.value = "";
    isAdmin.value = "";
  } catch (error) {
    console.error('Erro ao fazer logout:', error);
  }
};

onMounted(estaAutenticado);
</script>

<template>
<!-- Sidebar -->
  <aside class="navbar navbar-vertical navbar-expand-xl position-fixed" data-bs-theme="dark">
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
        <ul class="navbar-nav pt-lg-3 h-100 d-flex flex-column">
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
          <li class="nav-item mt-auto" v-if="!name">
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
          <li class="nav-item" v-if="name">
            <RouterLink class="nav-link" :to="{ name: 'Borrowed' }">  
              <span class="nav-link-title"> 
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-file-sad">
                  <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                  <path d="M14 3v4a1 1 0 0 0 1 1h4" />
                  <path d="M17 21h-10a2 2 0 0 1 -2 -2v-14a2 2 0 0 1 2 -2h7l5 5v11a2 2 0 0 1 -2 2m-7 -7h.01m3.99 0h.01" />
                  <path d="M10 18a3.5 3.5 0 0 1 4 0" />
                </svg>
                  Meus Alugados
                </span>
            </RouterLink>
          </li>
          <li class="nav-item" v-if="name && isAdmin">
            <RouterLink class="nav-link" :to="{ name: 'AllBorrowed' }">  
              <span class="nav-link-title"> 
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-calendar-sad">
                  <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                  <path d="M4 7a2 2 0 0 1 2 -2h12a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-12a2 2 0 0 1 -2 -2v-12m12 -4v4m-8 -4v4m-4 4h16m-9.995 3h.01m3.99 0h.01" />
                  <path d="M10 18a3.5 3.5 0 0 1 4 0" />
                </svg>  
                Todos Alugados
              </span>
            </RouterLink>
          </li>
          <!-- queria adicionar um espaço aq -->
          <li class="nav-item mt-auto" v-if="name">
            <div class="nav-link">  
              <span class="nav-link-title"> 
                <svg v-if="!isAdmin" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor" class="icon icon-tabler icons-tabler-filled icon-tabler-user">
                  <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                  <path d="M12 2a5 5 0 1 1 -5 5l.005 -.217a5 5 0 0 1 4.995 -4.783z" />
                  <path d="M14 14a5 5 0 0 1 5 5v1a2 2 0 0 1 -2 2h-10a2 2 0 0 1 -2 -2v-1a5 5 0 0 1 5 -5h4z" />
                </svg>
                <svg v-if="isAdmin" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-user-key">
                  <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                  <path d="M8 7a4 4 0 1 0 8 0a4 4 0 0 0 -8 0" />
                  <path d="M6 21v-2a4 4 0 0 1 4 -4h5" />
                  <path d="M18.5 18.5l-3.5 3.5l-1.5 -1.5" />
                  <path d="M18.554 18.414a2 2 0 1 1 2.828 -2.828a2 2 0 0 1 -2.828 2.828" />
                  <path d="M16 19l1 1" />
                </svg>
                  {{name}} ({{isAdmin ? "Admin" : "User"}})
              </span>
            </div>
          </li>
          <li class="nav-item" v-if="name">
            <RouterLink class="nav-link" @click="logout" :to="{ name: 'Home' }">  
              <span class="nav-link-title"> 
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-logout">
                  <path stroke="none" d="M0 0h24v24H0z" fill="none" />
                  <path d="M14 8v-2a2 2 0 0 0 -2 -2h-7a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h7a2 2 0 0 0 2 -2v-2" />
                  <path d="M9 12h12l-3 -3" />
                  <path d="M18 15l3 -3" />
                </svg> 
                Logout
              </span>
            </RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </aside>
</template>

<style scoped>

</style>

