<template>
	<aside :class="`${is_expanded ? 'is-expanded' : ''}`">
		<div class="logo">
			<img :src="logoURL" alt="Vue" /> 
			<h3 class="logo-heading">Edvance</h3>
		</div>
		<div class="profile-container">
			<img
			class="profile-picture"
			src="https://static.vecteezy.com/system/resources/previews/007/113/275/non_2x/avatar-man-face-silhouette-user-sign-person-profile-picture-male-icon-in-circle-round-black-color-illustration-image-outline-contour-line-thin-style-vector.jpg"/>
		</div>
		<div class="menu-toggle-wrap">
			<button class="menu-toggle" @click="ToggleMenu">
				<span class="material-icons">keyboard_double_arrow_right</span>
			</button>
		</div>

		<div class="menu">
			<router-link to="/" class="button">
				<span class="material-icons">home</span>
				<span class="text">Home</span>
			</router-link>
			<router-link to="/about" class="button">
				<span class="material-icons">school</span>
				<span class="text">Courses</span>
			</router-link>
			<router-link to="/team" class="button">
				<span class="material-icons">assignment</span>
				<span class="text">Assignments</span>
			</router-link>
			<router-link to="/contact" class="button">
				<span class="material-icons">event</span>
				<span class="text">Attendance</span>
			</router-link>
		</div>

		<div class="flex"></div>
		
		<div class="menu">
			<router-link to="/settings" class="button">
				<span class="material-icons">settings</span>
				<span class="text">Settings</span>
			</router-link>
		</div>
		<div class="menu">
			<router-link to="/logout" class="button">
				<span class="material-icons"> logout </span>
				<span class="text">Logout</span>
			</router-link>
		</div>
	</aside>
</template>

<script setup>
import { ref } from 'vue'
import logoURL from '../assets/logo.png'

const is_expanded = ref(localStorage.getItem("is_expanded") === "true")

const ToggleMenu = () => {
	is_expanded.value = !is_expanded.value
	localStorage.setItem("is_expanded", is_expanded.value)
}
</script>

<style lang="scss" scoped>
aside {
	--primary: #4ade80;
  	--primary-alt: #22c55e;
	--grey: #64748b;
	--dark: #1e293b;
	--dark-alt: #334155;
	--light: #f1f5f9;
	// --sidebar-width: 300px;

	background-color: var(--grey);
	display: flex;
	width: calc(2rem + 32px);
	overflow: hidden;
	min-height: 100vh;
	padding: 1rem;

	flex-direction: column;
	color: var(--dark);
	// height: 100%;
	// width: var(--sidebar-width);

	padding-top: 20px;
	min-height: 100vh;
	padding: 1rem;

	transition: 0.2s ease-in-out;
	// display: flex;
	// flex-direction: column;

	// background-color: var(--dark);
	// color: var(--light);

	// width: calc(2rem + 32px);
	// overflow: hidden;
	// min-height: 100vh;
	// padding: 1rem;

	// transition: 0.2s ease-in-out;

	.logo {
		margin-bottom: 1rem;
		display: flex;

		img {
			width: 2rem;
			margin-right: 1rem;
		}
		.logo-heading {
			font-size: 1.5rem; /* Adjust the font size as needed */
			color: var(--light);
			margin: 0; /* Remove margin to avoid extra space */
		}
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

	

	.flex {
		flex: 1 1 0%;
	}

	// @media (max-width: 1024px) {
	// 	position: absolute;
	// 	z-index: 99;
	// }
	// .logo {
	// 	margin-bottom: 1rem;

	// 	img {
	// 		width: 2rem;
	// 	}
	// }

	.menu-toggle-wrap {
		display: flex;
		justify-content: flex-end;
		margin-bottom: 1rem;

		position: relative;
		top: 0;
		transition: 0.2s ease-in-out;

		.menu-toggle {
			transition: 0.2s ease-in-out;
			.material-icons {
				font-size: 2rem;
				color: var(--light);
				transition: 0.2s ease-out;
			}
			
			&:hover {
				.material-icons {
					color: var(--primary);
					transform: translateX(0.5rem);
				}
			}
		}
	}

	h3, .button .text {
		opacity: 0;
		transition: opacity 0.3s ease-in-out;
	}

	h3 {
		color: var(--grey);
		font-size: 0.875rem;
		margin-bottom: 0.5rem;
		text-transform: uppercase;
	}

	.menu {
		margin: 0 -1rem;

		.button {
			display: flex;
			align-items: center;
			text-decoration: none;

			transition: 0.2s ease-in-out;
			padding: 0.5rem 1rem;

			.material-icons {
				font-size: 2rem;
				color: var(--light);
				transition: 0.2s ease-in-out;
			}
			.text {
				color: var(--light);
				transition: 0.2s ease-in-out;
			}

			&:hover {
				background-color: var(--dark-alt);

				.material-icons, .text {
					color: var(--primary);
				}
			}

			&.router-link-exact-active {
				background-color: var(--dark-alt);
				border-right: 5px solid var(--primary);

				.material-icons, .text {
					color: var(--primary);
				}
			}
		}
	}

	.footer {
		opacity: 0;
		transition: opacity 0.3s ease-in-out;

		p {
			font-size: 0.875rem;
			color: var(--grey);
		}
	}

	&.is-expanded {
		width: var(--sidebar-width);

		.menu-toggle-wrap {
			top: -3rem;
			
			.menu-toggle {
				transform: rotate(-180deg);
			}
		}

		h3, .button .text {
			opacity: 1;
		}

		.button {
			.material-icons {
				margin-right: 1rem;
			}
		}

		.footer {
			opacity: 0;
		}
	}

	@media (max-width: 1024px) {
		position: absolute;
		z-index: 99;
	}
}
</style>