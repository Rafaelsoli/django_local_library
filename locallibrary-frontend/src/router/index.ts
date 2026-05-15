import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/books',
      name: 'Books',
      component: () => import('../views/BooksView.vue')
    },
    {
      path: '/books/:id',
      name: 'BookDetail',
      component: () => import('../views/BookDetailView.vue')
    },
    {
      path: '/authors',
      name: 'Authors',
      component: () => import('../views/AuthorView.vue')
    },
    {
      path: '/authors/:id',
      name: 'AuthorDetail',
      component: () => import('../views/AuthorDetailView.vue')
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/Borrowed',
      name: 'Borrowed',
      component: () => import('../views/BorrowedView.vue')
    },
    {
      path: '/AllBorrowed',
      name: 'AllBorrowed',
      component: () => import('../views/AllBorrowedView.vue')
    }
  ],
})

export default router
