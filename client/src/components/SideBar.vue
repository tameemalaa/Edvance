<template>
  <aside>
    <div class="logo-container">
      <img class="logo" src="/logo.jpg" />
    </div>
    <div class="profile-container">
      <img
        class="profile-picture"
        src="https://static.vecteezy.com/system/resources/previews/007/113/275/non_2x/avatar-man-face-silhouette-user-sign-person-profile-picture-male-icon-in-circle-round-black-color-illustration-image-outline-contour-line-thin-style-vector.jpg"
      />
    </div>
    <div class="menu">
      <router-link to="/" class="button">
        <span class="material-icons">home</span>
        <span class="text">Home</span>
      </router-link>
      <router-link to="/about" class="button">
        <span class="material-symbols-outlined"> library_books </span>
        <span class="text">Courses</span>
      </router-link>

      <router-link to="/team" class="button">
        <span class="material-symbols-outlined"> assignment </span>
        <span class="text">Assignments</span>
      </router-link>

      <router-link to="/contact" class="button">
        <span class="material-symbols-outlined"> event_note </span>
        <span class="text">Attendance</span>
      </router-link>
    </div>
    <div class="flex"></div>
    <div class="menu">
      <router-link to="/logout" class="button">
        <span class="material-symbols-outlined"> logout </span>
        <span class="text">Logout</span>
      </router-link>
    </div>
  </aside>
</template>

<style lang="scss" scoped>
aside {
  --primary: #4ade80;
  --primary-alt: #22c55e;
  --grey: #64748b;
  --dark: #1e293b;
  --dark-alt: #334155;
  --light: #f1f5f9;
  --sidebar-width: 300px;

  background-color: var(--grey);
  display: flex;

  flex-direction: column;
  color: var(--dark);
  height: 100%;
  width: var(--sidebar-width);

  padding-top: 20px;
  min-height: 100vh;
  padding: 1rem;

  transition: 0.2 ease-in-out;

  .logo-container {
    margin-bottom: 1rem;
  }

  .logo {
    width: 5rem;
  }

  .profile-container {
    width: 60%;
    overflow: hidden;
    border-radius: 50%;
    margin: auto;
    margin-bottom: 2rem;
    margin-top: 2rem; 
  }

  .profile-picture {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .menu {
    margin-right:  -1rem;
    margin-top: 4rem; 
    .button {
      display: flex;
      align-items: center;
      text-decoration: none;

      transition: 0.2s ease-in-out;
      padding: 0.5rem 1rem;

      .material-icons,
      .material-symbols-outlined {
        font-size: 2rem;
        color: var(--light);
        transition: 0.2s ease-in-out;
        margin-right: 1rem;
      }
      .text {
        color: var(--light);
        transition: 0.2s ease-in-out;
        font-size: 1rem;
        font-weight: bold;
      }

      &:hover {
        background-color: var(--dark-alt);

        .material-icons,
        .materials-symbols-outlined,
        .text {
          color: var(--primary);
        }
      }

      &.router-link-exact-active {
        background-color: var(--dark-alt);
        border-right: 5px solid var(--primary);

        .material-icons,
        .text {
          color: var(--primary);
        }
      }
    }
  }

  .flex {
    flex: 1 1 0%;
  }

  @media (max-width: 1024px) {
    position: absolute;
    z-index: 99;
  }
}
</style>


