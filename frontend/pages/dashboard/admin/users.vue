<template>
  <div class="min-h-screen bg-white dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 shadow">
      <div class="container mx-auto px-4 py-6">
        <h1 class="text-3xl font-display text-deep-maroon dark:text-rose-gold">User Management</h1>
        <p class="text-gray-600 dark:text-gray-400 mt-2">Manage user accounts and permissions</p>
      </div>
    </div>

    <!-- Content -->
    <div class="container mx-auto px-4 py-8">
      <!-- Actions Bar -->
      <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-6 gap-4">
        <div class="flex items-center space-x-2">
          <div class="relative">
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Search users..."
              class="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              @input="handleSearch"
            />
            <div class="absolute left-3 top-2.5">
              <Icon name="ph:magnifying-glass" class="h-5 w-5 text-gray-400 dark:text-gray-500" />
            </div>
          </div>

          <select
            v-model="filters.role"
            class="px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
          >
            <option value="">All Roles</option>
            <option value="admin">Admin</option>
            <option value="customer">Customer</option>
            <option value="staff">Staff</option>
          </select>

          <select
            v-model="filters.status"
            class="px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
          >
            <option value="">All Status</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
            <option value="suspended">Suspended</option>
          </select>
        </div>

        <button
          @click="showAddUserModal = true"
          class="px-4 py-2 bg-rose-gold hover:bg-deep-maroon text-white rounded-lg flex items-center justify-center transition-colors"
        >
          <Icon name="ph:plus" class="mr-2 h-5 w-5" />
          Add New User
        </button>
      </div>

      <!-- Users Table -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead>
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">User</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Email</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Role</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Joined</th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-for="user in filteredUsers" :key="user.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="h-10 w-10 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center text-gray-700 dark:text-gray-300 overflow-hidden">
                      <img v-if="user.avatar" :src="user.avatar" :alt="user.name" class="h-10 w-10 object-cover" />
                      <span v-else>{{ getUserInitials(user.name) }}</span>
                    </div>
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900 dark:text-white">{{ user.name }}</div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ user.email }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="getRoleBadgeClass(user.role)">
                    {{ user.role }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="getStatusBadgeClass(user.status)">
                    {{ user.status }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ formatDate(user.joinedDate) }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button @click="editUser(user)" class="text-rose-gold hover:text-deep-maroon dark:hover:text-rose-gold/80 mr-3">
                    <Icon name="ph:pencil" class="h-5 w-5" />
                  </button>
                  <button @click="confirmDeleteUser(user)" class="text-rose-gold hover:text-deep-maroon dark:hover:text-rose-gold/80">
                    <Icon name="ph:trash" class="h-5 w-5" />
                  </button>
                </td>
              </tr>
              <tr v-if="filteredUsers.length === 0">
                <td colspan="6" class="px-6 py-4 text-center text-gray-500 dark:text-gray-400">
                  No users found
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Pagination -->
        <div class="px-6 py-4 border-t border-gray-200 dark:border-gray-700 flex items-center justify-between">
          <div class="text-sm text-gray-500 dark:text-gray-400">
            Showing <span class="font-medium">{{ paginationStart }}</span> to <span class="font-medium">{{ paginationEnd }}</span> of <span class="font-medium">{{ totalUsers }}</span> users
          </div>
          <div class="flex space-x-2">
            <button 
              @click="currentPage--" 
              :disabled="currentPage === 1" 
              class="px-3 py-1 rounded-md border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Previous
            </button>
            <button 
              @click="currentPage++" 
              :disabled="paginationEnd >= totalUsers" 
              class="px-3 py-1 rounded-md border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit User Modal -->
    <div v-if="showAddUserModal || showEditUserModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
          <h3 class="text-xl font-display text-deep-maroon dark:text-rose-gold">
            {{ showEditUserModal ? 'Edit User' : 'Add New User' }}
          </h3>
          <button @click="closeUserModal" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
            <Icon name="ph:x" class="h-5 w-5" />
          </button>
        </div>
        <div class="p-6">
          <form @submit.prevent="showEditUserModal ? updateUser() : addUser()">
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Full Name</label>
                <input 
                  type="text" 
                  v-model="userForm.name" 
                  required
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email</label>
                <input 
                  type="email" 
                  v-model="userForm.email" 
                  required
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                />
              </div>
              
              <div v-if="!showEditUserModal">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Password</label>
                <input 
                  type="password" 
                  v-model="userForm.password" 
                  required
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Role</label>
                <select 
                  v-model="userForm.role" 
                  required
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                >
                  <option value="admin">Admin</option>
                  <option value="customer">Customer</option>
                  <option value="staff">Staff</option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Status</label>
                <select 
                  v-model="userForm.status" 
                  required
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                >
                  <option value="active">Active</option>
                  <option value="inactive">Inactive</option>
                  <option value="suspended">Suspended</option>
                </select>
              </div>
            </div>
            
            <div class="mt-6 flex justify-end space-x-3">
              <button 
                type="button" 
                @click="closeUserModal" 
                class="px-4 py-2 border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700"
              >
                Cancel
              </button>
              <button 
                type="submit" 
                class="px-4 py-2 bg-rose-gold hover:bg-deep-maroon text-white rounded-lg"
              >
                {{ showEditUserModal ? 'Update User' : 'Add User' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-xl font-display text-deep-maroon dark:text-rose-gold">Confirm Delete</h3>
        </div>
        <div class="p-6">
          <p class="text-gray-700 dark:text-gray-300">Are you sure you want to delete the user <span class="font-medium">{{ userToDelete?.name }}</span>? This action cannot be undone.</p>
          
          <div class="mt-6 flex justify-end space-x-3">
            <button 
              @click="showDeleteModal = false" 
              class="px-4 py-2 border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              Cancel
            </button>
            <button 
              @click="deleteUser()" 
              class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg"
            >
              Delete User
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// SEO
useHead({
  title: 'User Management - Nakhrali Fashion Admin',
  meta: [
    {
      name: 'description',
      content: 'Manage user accounts and permissions for Nakhrali Fashion.'
    }
  ]
})

// Auth
const { isAdmin } = useAuth()

// Apply admin middleware
definePageMeta({
  middleware: 'admin'
})

// State
const searchQuery = ref('')
const filters = ref({
  role: '',
  status: ''
})
const currentPage = ref(1)
const itemsPerPage = 10
const showAddUserModal = ref(false)
const showEditUserModal = ref(false)
const showDeleteModal = ref(false)
const userToDelete = ref(null)
const userForm = ref({
  id: null,
  name: '',
  email: '',
  password: '',
  role: 'customer',
  status: 'active',
  joinedDate: null
})

// Mock data for users
const users = ref([
  {
    id: 1,
    name: 'Admin User',
    email: 'admin@nakhrali.com',
    role: 'admin',
    status: 'active',
    joinedDate: '2023-01-01',
    avatar: null
  },
  {
    id: 2,
    name: 'Priya Sharma',
    email: 'priya@example.com',
    role: 'customer',
    status: 'active',
    joinedDate: '2023-02-15',
    avatar: null
  },
  {
    id: 3,
    name: 'Rahul Patel',
    email: 'rahul@example.com',
    role: 'customer',
    status: 'active',
    joinedDate: '2023-03-10',
    avatar: null
  },
  {
    id: 4,
    name: 'Ananya Singh',
    email: 'ananya@example.com',
    role: 'staff',
    status: 'active',
    joinedDate: '2023-04-05',
    avatar: null
  },
  {
    id: 5,
    name: 'Vikram Malhotra',
    email: 'vikram@example.com',
    role: 'customer',
    status: 'inactive',
    joinedDate: '2023-05-20',
    avatar: null
  }
])

// Computed properties
const filteredUsers = computed(() => {
  let result = [...users.value]
  
  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(user => 
      user.name.toLowerCase().includes(query) || 
      user.email.toLowerCase().includes(query)
    )
  }
  
  // Apply role filter
  if (filters.value.role) {
    result = result.filter(user => user.role === filters.value.role)
  }
  
  // Apply status filter
  if (filters.value.status) {
    result = result.filter(user => user.status === filters.value.status)
  }
  
  return result
})

const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredUsers.value.slice(start, end)
})

const totalUsers = computed(() => filteredUsers.value.length)

const paginationStart = computed(() => {
  if (totalUsers.value === 0) return 0
  return (currentPage.value - 1) * itemsPerPage + 1
})

const paginationEnd = computed(() => {
  return Math.min(currentPage.value * itemsPerPage, totalUsers.value)
})

// Methods
const handleSearch = () => {
  currentPage.value = 1 // Reset to first page on search
}

const getUserInitials = (name) => {
  if (!name) return ''
  return name
    .split(' ')
    .map(part => part.charAt(0))
    .join('')
    .toUpperCase()
    .substring(0, 2)
}

const getRoleBadgeClass = (role) => {
  const roleClasses = {
    'admin': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300',
    'customer': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
    'staff': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
  }
  return roleClasses[role] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
}

const getStatusBadgeClass = (status) => {
  const statusClasses = {
    'active': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
    'inactive': 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
    'suspended': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
  }
  return statusClasses[status] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
}

const editUser = (user) => {
  userForm.value = { ...user }
  showEditUserModal.value = true
}

const confirmDeleteUser = (user) => {
  userToDelete.value = user
  showDeleteModal.value = true
}

const closeUserModal = () => {
  showAddUserModal.value = false
  showEditUserModal.value = false
  userForm.value = {
    id: null,
    name: '',
    email: '',
    password: '',
    role: 'customer',
    status: 'active',
    joinedDate: null
  }
}

const addUser = () => {
  // In a real application, this would be an API call
  const newUser = {
    ...userForm.value,
    id: users.value.length + 1,
    joinedDate: new Date().toISOString().split('T')[0],
    avatar: null
  }
  
  users.value.push(newUser)
  closeUserModal()
}

const updateUser = () => {
  // In a real application, this would be an API call
  const index = users.value.findIndex(u => u.id === userForm.value.id)
  if (index !== -1) {
    users.value[index] = { ...userForm.value }
  }
  closeUserModal()
}

const deleteUser = () => {
  // In a real application, this would be an API call
  if (userToDelete.value) {
    users.value = users.value.filter(u => u.id !== userToDelete.value.id)
    showDeleteModal.value = false
    userToDelete.value = null
  }
}
</script>