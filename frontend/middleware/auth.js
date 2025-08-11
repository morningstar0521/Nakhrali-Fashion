export default defineNuxtRouteMiddleware((to, from) => {
  const { isAuthenticated } = useAuth()
  
  // If user is not authenticated and trying to access protected route
  if (!isAuthenticated.value) {
    // Redirect to login with the intended destination
    return navigateTo({
      path: '/auth/login',
      query: { redirect: to.fullPath }
    })
  }
}) 