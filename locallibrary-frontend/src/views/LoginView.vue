<script setup lang="ts">
import SidebarComponent from '../components/SidebarComponent.vue';
</script>

<style scoped lang="ts"></style>
<template>
<SidebarComponent/>
<div class="page">
    <div class="page-wrapper">
        <div class="container-fluid d-flex align-items-center justify-content-center" style="height: 100vh;">
            <div class="card">
                <div class="card-body">
                    <h1 class="card-title">Login</h1>
                    <p class="card-text">Faça login para acessar sua conta.</p>
                    <form>
                        <div class="mb-3">
                            <label for="email" class="form-label">Email</label>
                            <input type="email" class="form-control" id="email" placeholder="Digite seu email">
                        </div>
                        <div class="mb-3">
                            <label for="password" class="form-label">Senha</label>
                            <input type="password" class="form-control" id="password" placeholder="Digite sua senha">
                        </div>
                        <button type="submit" class="btn btn-primary">Entrar</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
</template>
<style scoped></style>